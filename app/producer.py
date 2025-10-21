import boto3
import json
import os

from app.odds import OddsAPIHandler

KINESIS_STREAM_NAME = 'sport-odds'
ODDS_API_KEY = os.getenv('ODDS_API_KEY')


def main(event) -> list[dict]:
    SPORTS_TO_GET = ['americanfootball_ncaaf']
    REGIONS_TO_GET = 'us'
    MARKETS_TO_GET = 'totals'

    odds_api_handler = OddsAPIHandler(ODDS_API_KEY)

    odds_data = odds_api_handler.get_odds(SPORTS_TO_GET[0], REGIONS_TO_GET, MARKETS_TO_GET)

    return odds_data


def lambda_handler(event, context) -> dict:
    events = main(event)

    kinesis_client = boto3.client('kinesis')

    records = []

    for odds_event in events:
        records.append(
            {
                'Data': json.dumps(odds_event),  # must be bytes/string
                'PartitionKey': str(odds_event['sport_key']),  # must be string,
            }
        )

    # Send records
    response = kinesis_client.put_records(Records=records, StreamName=KINESIS_STREAM_NAME)

    print('Response:')
    print(json.dumps(response, indent=2))

    return {'statusCode': 200, 'body': f'Processed {len(records)} records'}


if __name__ == '__main__':
    # Used for local testing
    event = {}
    context = {}
    data = lambda_handler(event, context)
    print(data)
