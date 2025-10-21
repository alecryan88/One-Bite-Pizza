import requests


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
