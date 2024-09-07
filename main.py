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
    # Extract timezone from the given datetime object
    timezone = last_event_time.tzinfo
    print("timezone", timezone)

    # Get the current time in the extracted timezone
    current_time = datetime.now(pytz.utc).astimezone(timezone)
    print("current_time", current_time)

    # Define the target time (00:00) in the same timezone
    target_time = current_time.replace(hour=19, minute=15, second=0, microsecond=0)
    print("target_time", target_time)

    # Calculate the difference in minutes
    time_difference = (current_time - target_time).total_seconds() / 60

    # Check if the time difference is within ±5 minutes
    if -5 <= time_difference <= 5:
        return True
    return False


if __name__ == "__main__":
    print("starting")
    username = os.getenv("USER_GITHUB")
    token = os.getenv("TOKEN_GITHUB")

    if check_time(username, token):
        print("collecting activity")
        activity_summary = collect_github_activity(username, token)
        print(activity_summary)

        # Convert activity_summary to JSON string
        activity_summary_json = json.dumps(activity_summary)

        # Call the telegram.py script with the activity summary
        subprocess.run(["python", "telegram_bot.py", activity_summary_json])
