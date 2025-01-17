import os
import json
import subprocess
from github import collect_github_activity

# Load environment variables from .env file
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    username = os.getenv("USER_GITHUB")
    token = os.getenv("TOKEN_GITHUB")
    activity_summary = collect_github_activity(username, token)
    # Convert activity_summary to JSON string
    activity_summary_json = json.dumps(activity_summary)
    # Call the telegram.py script with the activity summary
    subprocess.run(["python", "telegram_bot.py", activity_summary_json])