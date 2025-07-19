import schedule
import time
from main import run_bot

print("🚀 Scheduler started...")  # Log 1

schedule.every().day.at("17:41").do(lambda: print("⏰ Time matched!") or run_bot())

while True:
    print("⏳ Waiting...")  # Log 2
    schedule.run_pending()
    time.sleep(60)
