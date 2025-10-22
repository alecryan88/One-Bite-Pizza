import boto3
import json
import os
import requests

KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME')
ODDS_API_KEY = os.getenv('ODDS_API_KEY')


class OddsAPIHandler:
    def __init__(self, api_key: str):
        self.url = 'https://api.the-odds-api.com'
        self.params = {'apiKey': api_key}

    def get_sports(self) -> list[dict]:
        """Returns a list of in-season sport objects. The sport key can be used as the sport parameter in other endpoints.
        This endpoint does not count against the usage quota.
        """
        path = '/v4/sports/'
        response = requests.get(self.url + path, params=self.params)
        return response.json()

    def get_odds(self, sport: str, regions: str, markets: str) -> list[dict]:
        """Returns a list of upcoming and live games with recent odds for a given sport,
        region and market
        """
        path = f'/v4/sports/{sport}/odds'

        params = {'regions': regions, 'markets': markets}

        self.params.update(params)

        response = requests.get(self.url + path, params=self.params)

        print(response.url)

        print(response.status_code)
        return response.json()


def main(event) -> list[dict]:
    SPORTS_TO_GET = ['americanfootball_ncaaf']
    REGIONS_TO_GET = 'us'
    MARKETS_TO_GET = 'totals'

    odds_api_handler = OddsAPIHandler(ODDS_API_KEY)

    odds_data = odds_api_handler.get_odds(SPORTS_TO_GET[0], REGIONS_TO_GET, MARKETS_TO_GET)
    print(odds_data)
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
