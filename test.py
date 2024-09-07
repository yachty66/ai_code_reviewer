import os
import json
import subprocess
from github import collect_github_activity, fetch_last_event_local_time
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

username = os.getenv("USER_GITHUB")
token = os.getenv("TOKEN_GITHUB")

last_event_time = fetch_last_event_local_time(username, token)

print("last_event_time", last_event_time)