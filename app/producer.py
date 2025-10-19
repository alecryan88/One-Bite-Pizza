import requests
import boto3
import json
import os
from datetime import datetime, timezone

KINESIS_STREAM_NAME = os.getenv('KINESIS_STREAM_NAME')


class OddsAPIHandler:
    def __init__(self):
        self.url = 'https://api.the-odds-api.com'
        self.params = {'apiKey': 'a757151ea690238d05a4538d110ddaa5'}

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

    odds_api_handler = OddsAPIHandler()

    odds_data = odds_api_handler.get_odds(SPORTS_TO_GET[0], REGIONS_TO_GET, MARKETS_TO_GET)

    return odds_data


def lambda_handler(event, context) -> dict:
    events = main(event)
    kinesis_client = boto3.client('kinesis')

    records = []
    for event in events:
        event['processing_time'] = datetime.now(timezone.utc).isoformat()
        records.append(
            {
                'Data': json.dumps(event),  # must be bytes/string
                'PartitionKey': str(event['sport_key']),  # must be string,
            }
        )

    # Send records
    response = kinesis_client.put_records(Records=records, StreamName=KINESIS_STREAM_NAME)

    print('Response:')
    print(json.dumps(response, indent=2))

    return {'statusCode': 200, 'example event': event}


if __name__ == '__main__':
    # Used for local testing
    event = {}
    context = {}
    data = lambda_handler(event, context)
    print(data)
