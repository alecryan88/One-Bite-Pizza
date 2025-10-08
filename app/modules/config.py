import os
from datetime import datetime, timedelta


class Settings:
    def __init__(self, event):
        self.event = event
        self.env = os.getenv('ENV', 'dev')
        self.api_url = 'https://api.onebite.app/review'
        self.limit = 50
        self.start_date_dt = datetime.fromisoformat(event['time'].replace('Z', '+00:00'))
        self.end_date_dt = self.start_date_dt

    @property
    def date_range(self):
        return [
            (self.start_date_dt + timedelta(days=x)).strftime('%Y-%m-%d')
            for x in range((self.end_date_dt - self.start_date_dt).days + 1)
        ]
