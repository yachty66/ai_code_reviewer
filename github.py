import requests
from datetime import datetime, timedelta
import pytz
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def fetch_last_event_local_time(username, token):
    if not username or not token:
        raise ValueError("GitHub username or token is not set.")

    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching events: {response.status_code}")

    events = response.json()
    if not events:
        print("No events found for the user.")
        return None

    last_event_time_utc = events[0]["created_at"]  # The last event's timestamp

    # Convert to local time
    dt = datetime.strptime(last_event_time_utc, "%Y-%m-%dT%H:%M:%SZ")
    utc_time = dt.replace(tzinfo=pytz.UTC)
    local_time = utc_time.astimezone()  # Convert to local timezone

    return local_time


def get_time_24_hours_back(event_time):
    # Get the current time in the same timezone as the event time
    current_time = datetime.now(event_time.tzinfo)

    # Calculate the time 24 hours back
    time_24_hours_back = current_time - timedelta(hours=24)

    return time_24_hours_back


def fetch_user_events(username, token):
    if not username or not token:
        raise ValueError("GitHub username or token is not set.")

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    url = f"https://api.github.com/users/{username}/events"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Error fetching events: {response.status_code}")

    events = response.json()
    return events


def filter_commits_last_24_hours(events, since, until):
    commits = []
    for event in events:
        if event["type"] == "PushEvent":
            event_time = datetime.strptime(
                event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=pytz.UTC)
            if since <= event_time <= until:
                for commit in event["payload"]["commits"]:
                    repo_name = event["repo"]["name"]
                    commit_sha = commit["sha"]
                    commits.append((repo_name, commit_sha))
    return commits


def fetch_commit_details(username, repo, sha, token):
    headers = {"Authorization": f"token {token}"}
    url = f"https://api.github.com/repos/{repo}/commits/{sha}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"Error fetching commit details for {sha}: {response.status_code}"
        )

    return response.json()


def calculate_lines_added(commits, token):
    total_lines_added = 0
    for repo_name, commit_sha in commits:
        commit_details = fetch_commit_details(
            repo_name.split("/")[0], repo_name, commit_sha, token
        )
        total_lines_added += commit_details["stats"]["additions"]
    return total_lines_added


def calculate_lines_removed(commits, token):
    total_lines_removed = 0
    for repo_name, commit_sha in commits:
        commit_details = fetch_commit_details(
            repo_name.split("/")[0], repo_name, commit_sha, token
        )
        total_lines_removed += commit_details["stats"]["deletions"]
    return total_lines_removed


def count_commits_per_repo(commits):
    repo_commit_count = {}
    for repo_name, _ in commits:
        if repo_name not in repo_commit_count:
            repo_commit_count[repo_name] = 0
        repo_commit_count[repo_name] += 1
    return [
        {"repo_name": repo, "commit_count": count}
        for repo, count in repo_commit_count.items()
    ]


def filter_repos_created_last_24_hours(events, since, until):
    repos_created = []
    for event in events:
        if (
            event["type"] == "CreateEvent"
            and event["payload"]["ref_type"] == "repository"
        ):
            event_time = datetime.strptime(
                event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=pytz.UTC)
            if since <= event_time <= until:
                repos_created.append(event["repo"]["name"])
    return repos_created


def filter_issues_opened_last_24_hours(events, since, until):
    issues_opened = []
    for event in events:
        if event["type"] == "IssuesEvent" and event["payload"]["action"] == "opened":
            event_time = datetime.strptime(
                event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=pytz.UTC)
            if since <= event_time <= until:
                repo_name = event["repo"]["name"]
                issue_title = event["payload"]["issue"]["title"]
                issues_opened.append(
                    {"repo_name": repo_name, "issue_title": issue_title}
                )
    return issues_opened


def filter_pull_requests_opened_last_24_hours(events, since, until):
    pull_requests_opened = []
    for event in events:
        if (
            event["type"] == "PullRequestEvent"
            and event["payload"]["action"] == "opened"
        ):
            event_time = datetime.strptime(
                event["created_at"], "%Y-%m-%dT%H:%M:%SZ"
            ).replace(tzinfo=pytz.UTC)
            if since <= event_time <= until:
                repo_name = event["repo"]["name"]
                pr_title = event["payload"]["pull_request"]["title"]
                pull_requests_opened.append(
                    {"repo_name": repo_name, "pr_title": pr_title}
                )
    return pull_requests_opened


def collect_github_activity(username, token):
    # Step 1: Get the last event time in local timezone
    event_time = fetch_last_event_local_time(username, token)
    if not event_time:
        return []

    # Step 2: Calculate the time 24 hours back
    time_24_hours_back = get_time_24_hours_back(event_time)

    # Step 3: Fetch all recent events
    events = fetch_user_events(username, token)
    if not events:
        return []

    # Step 4: Filter commits from the last 24 hours
    commits_last_24_hours = filter_commits_last_24_hours(
        events, time_24_hours_back, event_time
    )

    # Step 5: Calculate total lines of code added
    total_lines_added = calculate_lines_added(commits_last_24_hours, token)

    # Step 6: Calculate total lines of code removed
    total_lines_removed = calculate_lines_removed(commits_last_24_hours, token)

    # Step 7: Count the number of commits
    total_commits = len(commits_last_24_hours)

    # Step 8: Count commits per repository
    commits_per_repo = count_commits_per_repo(commits_last_24_hours)

    # Step 9: Filter repositories created in the last 24 hours
    repos_created_last_24_hours = filter_repos_created_last_24_hours(
        events, time_24_hours_back, event_time
    )

    # Step 10: Filter issues opened in the last 24 hours
    issues_opened_last_24_hours = filter_issues_opened_last_24_hours(
        events, time_24_hours_back, event_time
    )

    # Step 11: Filter pull requests opened in the last 24 hours
    pull_requests_opened_last_24_hours = filter_pull_requests_opened_last_24_hours(
        events, time_24_hours_back, event_time
    )

    # Collect all metrics into a list of dictionaries
    activity_summary = [
        {"total_lines_code_added": total_lines_added},
        {"total_lines_code_removed": total_lines_removed},
        {"total_commits": total_commits},
        {"commits_per_repo": commits_per_repo},
        {"repos_created_last_24_hours": repos_created_last_24_hours},
        {"issues_opened_last_24_hours": issues_opened_last_24_hours},
        {"pull_requests_opened_last_24_hours": pull_requests_opened_last_24_hours},
    ]

    return activity_summary


# if __name__ == "__main__":
#     username = os.getenv("GITHUB_USER")
#     token = os.getenv("GITHUB_TOKEN")

#     activity_summary = collect_github_activity(username, token)
#     print(activity_summary)