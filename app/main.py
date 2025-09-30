import requests
from collections import defaultdict
from datetime import datetime
import boto3
import io
import json
import logging

# Config
from modules.config import Settings

BUCKET_NAME = 'one-bite-pizza'


def convert_str_to_datetime(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str.replace('Z', '+00:00'))


def get_review_offset(url: str, offset: int, limit: int) -> list[dict]:
    """Fetch reviews from the API"""
    try:
        response = requests.get(url, params={'offset': offset, 'limit': limit})
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f'Error fetching reviews: {e}')
        return []


def get_all_reviews(settings: Settings) -> list[dict]:
    """Get all reviews from the API for specified date range"""
    reviews_list = []
    # Start at the first page
    page = 0

    # Loop through pages until we've passed the date we want
    while True:
        offset = page * settings.limit
        reviews = get_review_offset(settings.api_url, offset, settings.limit)
        reviews_list.extend(reviews)

        # Check the last review's date of the page to determine if we've
        # passed the date we want to load
        last_ts_of_page = convert_str_to_datetime(reviews[-1]['date'])

        # Break loop if we've passed the date we want to load
        if last_ts_of_page.date() < settings.start_date_dt.date():
            break
        else:
            page += 1

    # Partition data for load to s3
    reviews_by_date = defaultdict(list)

    # Partition reviews by date
    for review in reviews_list:
        dt = datetime.fromisoformat(review['date'].replace('Z', '+00:00'))
        reviews_by_date[dt.strftime('%Y-%m-%d')].append(review)

    filtered_reviews_by_date = {
        k: v for k, v in reviews_by_date.items() if k in settings.date_range
    }

    logging.info(f'Loaded {len(filtered_reviews_by_date)} reviews for {settings.date_range}')

    # Print the number of reviews for each day
    for date, reviews in filtered_reviews_by_date.items():
        logging.info(f'{date}: {len(reviews)}')

    return filtered_reviews_by_date


def main() -> None:
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Get settings from environment variables and command line arguments
    settings = Settings()

    # Log the environment
    logging.info(f'Running for {settings.env} environment')

    # Get reviews filtered by the provided the date range in setings
    filtered_reviews_by_date = get_all_reviews(settings)

    # Load data to s3
    s3 = boto3.client('s3')

    logging.info(f'Uploading reviews to {BUCKET_NAME}...')
    for date, reviews in filtered_reviews_by_date.items():
        buffer = io.StringIO()
        buffer.write(json.dumps(reviews))
        # Create the file name
        file_name = f'data/{settings.env}/date={date}.json'
        # Upload the data to s3

        s3.put_object(Bucket=BUCKET_NAME, Key=file_name, Body=buffer.getvalue())
        logging.info(f'Successfully uploaded reviews to {BUCKET_NAME} for {date}')

    logging.info(f'Succesfully Uploaded reviews to {BUCKET_NAME}')


if __name__ == '__main__':
    main()
