import requests
from collections import defaultdict
from datetime import datetime
import boto3
import io
import json
import logging
import yaml
import argparse
from helpers import get_date_range


# Parse command line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--start_date', type=str, required=True)
parser.add_argument('--end_date', type=str, required=False)
args = parser.parse_args()


def load_config(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)


# Load the configuration
config = load_config('config.yml')

# Constants from config
URL = config['api']['url']
LIMIT = config['api']['limit']
BUCKET_NAME = config['aws']['bucket_name']

# Configure logging
logging.basicConfig(level=logging.INFO)


def convert_str_to_datetime(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str.replace("Z", "+00:00"))


def get_review_offset(url: str, offset: int, limit: int) -> list[dict]:
    """ Fetch reviews from the API """
    try:
        response = requests.get(url, params={"offset": offset, "limit": limit})
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching reviews: {e}")
        return []


def get_all_reviews(start_date: datetime, end_date: datetime) -> list[dict]:
    """ Get all reviews from the API for specified date range """
    reviews_list = []
    # Start at the first page
    page = 0

    # Loop through pages until we've passed the date we want
    while True:
        offset = page * LIMIT
        reviews = get_review_offset(URL, offset, LIMIT)
        reviews_list.extend(reviews)

        # Check the last review's date of the page to determine if we've
        # passed the date we want to load
        last_ts_of_page = convert_str_to_datetime(reviews[-1]['date'])

        # Break loop if we've passed the date we want to load
        if last_ts_of_page.date() < start_date.date():
            break
        else:
            page += 1

    # Partition data for load to s3
    reviews_by_date = defaultdict(list)

    # Partition reviews by date
    for review in reviews_list:
        dt = datetime.fromisoformat(review['date'].replace("Z", "+00:00"))
        reviews_by_date[dt.strftime("%Y-%m-%d")].append(review)

    date_range = get_date_range(start_date, end_date)

    print(date_range)
    print(reviews_by_date.keys())

    filtered_reviews_by_date = { k:v for k, v in reviews_by_date.items() if k in date_range}

    print(" YEEEEET ", filtered_reviews_by_date.keys())
    # Print the number of reviews for each day
    for date, reviews in filtered_reviews_by_date.items():
        logging.info(f"{date}: {len(reviews)}")

    return reviews_by_date


def main(args: argparse.Namespace) -> None:
    # Get reviews for the date range. If end_date is not provided, use start_date for both.
    if args.end_date is None:
        args.end_date = args.start_date
    reviews_by_date = get_all_reviews(datetime.strptime(args.start_date, "%Y-%m-%d"), datetime.strptime(args.end_date, "%Y-%m-%d"))

    # Load data to s3
    s3 = boto3.client('s3')

    for date, reviews in reviews_by_date.items():
        buffer = io.StringIO()
        buffer.write(json.dumps(reviews))

        s3.put_object(Bucket=BUCKET_NAME, Key=f"data/date={date}.json", Body=buffer.getvalue())

    logging.info("Succesfully Uploaded reviews to s3")


if __name__ == "__main__":
    main(args)
