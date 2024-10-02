import json
import requests
import os
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
import redis
import time

load_dotenv()

API_URL = "https://open-data-api.jin10.com/data-api/v2/flash?category=2"
APP_KEY = os.getenv("APP_KEY")

redis_client = redis.Redis(host='127.0.0.1', port=6379, db=0)
REDIS_NEWS_LIST_KEY = "news:Story:ALL"
seen_ids = set()

def fetch_data():
    headers = {
        "secret-key": APP_KEY
    }
    try:
        response = requests.get(API_URL, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def split_and_push_news():
    global seen_ids
    data = fetch_data()
    if "error" not in data:
        for news_item in data.get("data", []):
            story_id = news_item.get("id", "unknown_id")
            if story_id not in seen_ids:
                seen_ids.add(story_id)
                redis_client.rpush(REDIS_NEWS_LIST_KEY, json.dumps(news_item))
                print(f"Pushed new story {story_id} to Redis.")
            else:
                print(f"Duplicate story {story_id} detected, skipping.")
    else:
        print(f"Error fetching data: {data['error']}")

scheduler = BackgroundScheduler()
scheduler.add_job(split_and_push_news, 'interval', seconds=60, max_instances=1, misfire_grace_time=30)
scheduler.start()

try:
    print("Starting news fetching service...")
    while True:
        time.sleep(1)
except (KeyboardInterrupt, SystemExit):
    print("Shutting down the scheduler...")
    scheduler.shutdown()
