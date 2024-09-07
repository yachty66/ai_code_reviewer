import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

# Load the bot token and chat ID from environment variables
TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def format_metadata(metadata):
    message = "Daily GitHub Activity Report:\n\n"
    
    for item in metadata:
        if 'total_lines_code_added' in item:
            message += f"Total lines of code added: {item['total_lines_code_added']}\n"
        if 'total_lines_code_removed' in item:
            message += f"Total lines of code removed: {item['total_lines_code_removed']}\n"
        if 'total_commits' in item:
            message += f"Total commits: {item['total_commits']}\n"
        if 'commits_per_repo' in item:
            message += "Commits per repository:\n"
            for repo in item['commits_per_repo']:
                message += f"  - {repo['repo_name']}: {repo['commit_count']} commits\n"
        if 'repos_created_last_24_hours' in item:
            message += "Repositories created in the last 24 hours:\n"
            for repo in item['repos_created_last_24_hours']:
                message += f"  - {repo}\n"
        if 'issues_opened_last_24_hours' in item:
            message += "Issues opened in the last 24 hours:\n"
            if item['issues_opened_last_24_hours']:
                for issue in item['issues_opened_last_24_hours']:
                    message += f"  - {issue['repo_name']}: {issue['issue_title']}\n"
            else:
                message += "  - None\n"
        if 'pull_requests_opened_last_24_hours' in item:
            message += "Pull requests opened in the last 24 hours:\n"
            if item['pull_requests_opened_last_24_hours']:
                for pr in item['pull_requests_opened_last_24_hours']:
                    message += f"  - {pr['repo_name']}: {pr['pr_title']}\n"
            else:
                message += "  - None\n"
    
    return message

async def send_daily_report(metadata):
    bot = Bot(token=TOKEN)
    message = format_metadata(metadata)
    await bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == '__main__':
    import sys
    import json

    # Read metadata from command line argument
    metadata = json.loads(sys.argv[1])
    asyncio.run(send_daily_report(metadata))