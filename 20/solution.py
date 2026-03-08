import pandas as pd

df = pd.read_csv("server_access_logs.csv")

# Step A: Find scraper IP
rate_limited = df[(df["status_code"] == 429) & (df["endpoint"] == "/api/pricing")]
scraper_ip = rate_limited["ip_address"].value_counts().idxmax()

# Step B: Median response time for scraper
scraper_rows = df[df["ip_address"] == scraper_ip]
median_rt = scraper_rows["response_time_ms"].median()
print(f"{scraper_ip}, {median_rt}")
