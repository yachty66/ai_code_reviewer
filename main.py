import os
from github import collect_github_activity

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

if __name__ == "__main__":
    username = os.getenv("GITHUB_USER")
    token = os.getenv("GITHUB_TOKEN")

    activity_summary = collect_github_activity(username, token)
    print(activity_summary)
    #send message to telegram
