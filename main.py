import os
import json
import subprocess
from github import collect_github_activity, fetch_last_event_local_time
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

def check_time(username, token):
    last_event_time = fetch_last_event_local_time(username, token)
    print("last_event_time", last_event_time)

    # print("last_event_time", last_event_time)
    # # Extract timezone offset from the given datetime string
    # timezone_offset = last_event_time.utcoffset().total_seconds() / 60  # offset in minutes
    # timezone = pytz.FixedOffset(timezone_offset)

    # # Get the current time in the extracted timezone
    # current_time = datetime.now(timezone)
    # print("current_time", current_time.hour, current_time.minute)

    # # Check if the current time is within 5 minutes of 16:07
    # print("checking time")
    # if current_time.hour == 16 and current_time.minute in range(2, 20):
    #     print("it's time")
    #     return True
    # print("not time yet")
    # return False

if __name__ == "__main__":
    print("starting")
    username = os.getenv("USER_GITHUB")
    token = os.getenv("TOKEN_GITHUB")

    if check_time(username, token):
        print("collecting activity")
        # activity_summary = collect_github_activity(username, token)
        # print(activity_summary)

        # # Convert activity_summary to JSON string
        # activity_summary_json = json.dumps(activity_summary)

        # # Call the telegram.py script with the activity summary
        # subprocess.run(["python", "telegram_bot.py", activity_summary_json])