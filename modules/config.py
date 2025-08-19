import os
import argparse
from datetime import datetime, timedelta


class RuntimeArgumentHandler:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument('--start_date', type=str, required=True)
        self.parser.add_argument('--end_date', type=str, required=False)
        self.args = self.parser.parse_args()


class Settings:
    def __init__(self):
        self.runtime_argument_handler = RuntimeArgumentHandler()
        self.env = os.getenv('ENV', 'dev')
        self.api_url = 'https://api.onebite.app/review'
        self.limit = 50
        self.bucket_name = 'one-bite-pizza-reviews'
        self.start_date_str = self.runtime_argument_handler.args.start_date
        self.end_date_str = (
            self.runtime_argument_handler.args.end_date
            or self.runtime_argument_handler.args.start_date
        )
        self.start_date_dt = datetime.strptime(self.start_date_str, '%Y-%m-%d')
        self.end_date_dt = datetime.strptime(self.end_date_str, '%Y-%m-%d')

    @property
    def date_range(self):
        return [
            self.start_date_dt + timedelta(days=x)
            for x in range((self.end_date_dt - self.start_date_dt).days + 1)
        ]
