# ai_code_reviewer

now all i need to find out is how many












------------------------------------------------------------------------------------------------------------------------------------------------------

- in the case the user did not pushed any code he is getting roasted or a motivational qoute is shared 

## Overview

checks at the end of your day all your commited and gives you feedback on the code you commited similar to https://www.producthunt.com/products/ai-code-reviewer-2?utm_source=badge-top-post-badge&utm_medium=badge#ai-code-reviewer delivered directly to your DMs on X

## Features

- **Automated Code Reviews**: Get detailed feedback on code changes using AI.
- **Metrics Tracking**: Provides quantitative metrics like lines of code added/removed, complexity, and test coverage.
- **Email Notifications**: Receive daily email reports with comprehensive feedback and metrics.
- **Customizable**: Adapt the feedback prompts, email format, and metrics as needed.

## Requirements

- Python 3.x
- Flask
- Requests
- OpenAI (or the relevant SDK for your chosen LLM)
- SMTP server configuration for sending emails

## Installation

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/ai-code-reviewer.git
    cd ai-code-reviewer
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Set Up API Keys and Configuration**:
    - Obtain an API key from your chosen LLM provider (e.g., OpenAI).
    - Add your API key and email server credentials to a configuration file or environment variables.
    
    Example for environment variables:
    ```sh
    export OPENAI_API_KEY="your_openai_api_key"
    export EMAIL_HOST="smtp.example.com"
    export EMAIL_PORT=587
    export EMAIL_USER="your_email@example.com"
    export EMAIL_PASSWORD="your_email_password"
    ```

4. **Run the Application**:
    ```sh
    python app.py
    ```

## Usage

### Webhook Configuration

1. **Set Up Webhooks**:
    - Configure your code repository (e.g., GitHub, GitLab) to send push events to your running Flask application.
    - Example for GitHub:
      - Go to your repository settings.
      - Select "Webhooks" and click "Add webhook".
      - Set the payload URL to your server's URL (e.g., `http://yourserver.com/webhook`).
      - Choose "application/json" as the content type.
      - Select "Just the push event" or other relevant events.

### Handling Push Events

The application listens for push events and processes code changes to generate feedback. Here’s a sample structure for handling a push event:

```python
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if data["action"] == "push":
        repo_name = data["repository"]["name"]
        commits = data["commits"]
        handle_push_event(repo_name, commits)
    return '', 200

def handle_push_event(repo_name, commits):
    for commit in commits:
        commit_id = commit["id"]
        diff = get_commit_diff(repo_name, commit_id)
        review_feedback = get_code_review_feedback(diff)
        send_email_with_feedback(diff, review_feedback)
```

### Email Structure

Emails sent by the application are structured as follows:

- **Introduction**
- **Summary of Changes**
- **AI-Generated Detailed Feedback**
- **Metrics and Other Information**
- **Closing Remarks**

Example email content is provided in the script.

## Configuration

You can customize the prompts, email format, and various metrics tracked by editing the respective sections of the code. 

### Customizing Prompts

```python
def get_code_review_feedback(code_diff):
    prompt = f"""
    You are a senior software engineer. Please review the following code changes and provide detailed feedback on code quality, potential bugs, optimization suggestions, and best practices.
    
    Code changes:
    {code_diff}
    """
    
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=1500,
        temperature=0.5,
    )
    
    feedback = response.choices[0].text.strip()
    return feedback
```

### Setting Up SMTP for Email Notifications

Configure your email credentials and SMTP server details to enable email notifications. Example SMTP setup is provided in the script.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

### Contact

For any questions or issues, please [open an issue](https://github.com/yourusername/ai-code-reviewer/issues) or reach out to [your_email@example.com](mailto:your_email@exa2mple.com).

## Acknowledgements

- [OpenAI](https://www.openai.com/) for the GPT-4 model.
- [Flask](https://flask.palletsprojects.com/en/2.0.x/) for the web server.

```

Replace placeholders with actual information like your repository URL, email, and any specific configurations related to your project. This README provides a comprehensive guide to setting up, running, and customizing your AI-powered code review application.

