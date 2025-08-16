from datetime import datetime, timedelta


start_date = datetime(2025, 8, 1)
end_date = datetime(2025, 8, 15)

x = [(start_date + timedelta(days=i)).strftime("%Y-%m-%d") for i in list(range((end_date - start_date).days + 1))]

print(x)



