import requests


class OddsAPIHandler:
    def __init__(self, api_key: str):
        self.url = 'https://api.the-odds-api.com'
        self.params = {'apiKey': api_key}

    def make_request(self, path: str, params: dict) -> dict:
        response = requests.get(self.url + path, params=params)
        print(f'Request URL: {response.url}')
        print(f'Status Code: {response.status_code}')
        if response.status_code != 200:
            raise Exception(
                f'Error making request to {self.url + path}: {response.status_code} {response.text}'
            )
        return response.json()

    def get_sports(self) -> list[dict]:
        """Returns a list of in-season sport objects. The sport key can be used as the sport parameter in other endpoints.
        This endpoint does not count against the usage quota.
        """
        path = '/v4/sports/'
        return self.make_request(path, self.params)

    def get_odds(self, sport: str, regions: str, markets: str) -> list[dict]:
        """Returns a list of upcoming and live games with recent odds for a given sport,
        region and market
        """
        path = f'/v4/sports/{sport}/odds'

        params = self.params.copy()
        params.update({'regions': regions, 'markets': markets})

        data = self.make_request(path, params)
        return data
