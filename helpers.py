from datetime import datetime, timedelta


def get_date_range(start_date: datetime, end_date: datetime) -> list[str]:
    """Takes start and end date and returns a list of dates between them"""
    # First get the index for each date in the range
    index_range = list(range((end_date - start_date).days + 1))

    # For each index, add the index as days to the start date and return the
    # date in the format YYYY-MM-DD
    date_range = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in index_range]

    return date_range
