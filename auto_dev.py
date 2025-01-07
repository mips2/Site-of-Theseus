#!/usr/bin/env python3
"""
auto_dev.py

An autonomous script that:
1. Pulls the latest code from GitHub.
2. Uses DeepSeek to generate new code features.
3. Tests changes.
4. Commits and pushes on success, or reverts on repeated failure.
"""

import os
import subprocess
import random
import time
from datetime import datetime
import yaml
import logging
import sys
import requests
from dotenv import load_dotenv

# ------------------------------------------------------------------------------
#  Logging Setup
# ------------------------------------------------------------------------------
LOG_FILE = "logs/auto_dev.log"
os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists

logging.basicConfig(
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)

# ------------------------------------------------------------------------------
#  Load Config
# ------------------------------------------------------------------------------
CONFIG_FILE = "config.yaml"
if not os.path.exists(CONFIG_FILE):
    logging.error(f"Missing config file: {CONFIG_FILE}. Exiting.")
    sys.exit(1)

with open(CONFIG_FILE, "r") as f:
    config = yaml.safe_load(f)

GITHUB_REPO = config.get("github_repo", "")
BRANCH_NAME = config.get("branch_name", "main")
RETRY_LIMIT = config.get("retry_limit", 5)
ENABLE_AUTODEV = config.get("enable_autodev", True)

# ------------------------------------------------------------------------------
#  DeepSeek API Key
# ------------------------------------------------------------------------------
# !!! WARNING: This is included directly here for demonstration. 
# For production, store in environment variables or a secret manager.
load_dotenv()
DEESEEK_API_KEY = os.getenv("DEESEEK_API_KEY")

if not DEESEEK_API_KEY:
    logging.error("No DeepSeek API key provided. Exiting.")
    sys.exit(1)

# ------------------------------------------------------------------------------
#  GitHub Token (Optional)
# ------------------------------------------------------------------------------
# You can store your GitHub token in an environment variable, e.g. GITHUB_TOKEN.
# If your local Git config is set up with SSH keys or GitHub CLI, you may not need this.
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)
if not GITHUB_TOKEN:
    logging.warning("No GITHUB_TOKEN found in environment. Proceeding without it.")

# ------------------------------------------------------------------------------
#  DeepSeek Integration
# ------------------------------------------------------------------------------
DEESEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEESEEK_MODEL   = "deepseek-chat"


def generate_code_change(current_code):
    """
    1. Send the existing code to DeepSeek, along with instructions on how to modify it.
    2. Return the updated code from the AI response.
    """

    # Example instruction: "Add a /hello route that returns 'Hello from AI!'"
    user_instructions = (
        "You are an AI developer. Please enhance this Flask code by adding a new route. "
        "For example, add a /hello route returning a friendly greeting or anything interesting. "
        "Ensure the code is valid Python and that it won't break the existing routes."
    )

    # Prepare the request body
    payload = {
        "model": DEESEEK_MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful AI developer."},
            {"role": "user", "content": user_instructions},
            {
                "role": "user",
                "content": f"Here is the existing code:\n\n{current_code}\n\nReturn only the updated code."
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {DEESEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(DEESEEK_API_URL, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        # Attempt to parse out the code from the AI
        result = response.json()
        ai_message = result["choices"][0]["message"]["content"]

        # The AI might return extra explanation. We want the Python code only.
        # For safety, we can assume the entire content is the updated code or 
        # contain code fences. Here, let's do a naive parse. 
        # If you want more robust parsing, you might do regex or more advanced filtering.
        if "```" in ai_message:
            # Attempt to extract code from triple backticks
            splitted = ai_message.split("```")
            # The code block could be splitted[1] or splitted[2], depending on markdown style. 
            # We'll pick the second chunk if it exists.
            if len(splitted) > 1:
                # This might contain language spec e.g. "```python"
                code_part = splitted[1].strip()
                # Remove "python" or similar if present
                code_part = code_part.replace("python", "").strip()
                return code_part
            else:
                return splitted[0].strip()
        else:
            # If no code fences, assume the entire response is code.
            return ai_message.strip()

    except requests.exceptions.RequestException as e:
        logging.error(f"DeepSeek API call failed: {e}")
        return current_code + "\n# [DeepSeek ERROR] Could not generate new code.\n"


# ------------------------------------------------------------------------------
#  Testing
# ------------------------------------------------------------------------------
def run_test_commands():
    """
    Run your website's tests to ensure the new code is valid.
    Return True if tests pass, False otherwise.
    """
    try:
        subprocess.check_call(["pip", "install", "-r", "website/requirements.txt"])
        subprocess.check_call(["pytest", "website/tests/", "--maxfail=1"])
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Test failed: {e}")
        return False

# ------------------------------------------------------------------------------
#  Git Helpers
# ------------------------------------------------------------------------------
def git_command(*args):
    """Helper to run git commands."""
    cmd = ["git"] + list(args)
    logging.info(f"Running git command: {' '.join(cmd)}")

    env = os.environ.copy()
    if GITHUB_TOKEN:
        # If you want to leverage https with token, you can do something like:
        # env["GIT_ASKPASS"] = "echo"
        # env["GIT_USERNAME"] = "YourUsername"
        # env["GIT_PASSWORD"] = GITHUB_TOKEN
        # But typically, you'd set up a credential helper. We'll assume SSH or existing config is fine.
        pass

    result = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logging.error(f"Git command error: {result.stderr.strip()}")
    else:
        logging.info(f"Git command success: {result.stdout.strip()}")
    return result

# ------------------------------------------------------------------------------
#  Main Loop
# ------------------------------------------------------------------------------
def main_loop():
    if not ENABLE_AUTODEV:
        logging.info("AUTO-DEV is disabled in config.yaml. Exiting gracefully.")
        return

    # Step 1: Pull latest code
    git_command("pull", "origin", BRANCH_NAME)

    target_file = "website/app.py"
    if not os.path.exists(target_file):
        logging.error(f"{target_file} does not exist! Cannot proceed.")
        return

    # Read the old/original code
    with open(target_file, "r") as f:
        old_code = f.read()

    new_code = old_code  # We'll update this in a loop
    success = False

    for attempt in range(1, RETRY_LIMIT + 1):
        logging.info(f"Attempt #{attempt} to generate feature and test.")

        # Generate code from DeepSeek
        new_code = generate_code_change(new_code)

        # Write changes to file
        with open(target_file, "w") as f:
            f.write(new_code)

        # Step 2: Run tests
        if run_test_commands():
            success = True
            break
        else:
            logging.warning(f"Test failed on attempt #{attempt}. Retrying...")

    if success:
        # Step 3: Commit and push
        git_command("add", ".")
        commit_msg = f"Auto-update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        git_push_result = git_command("push", "origin", BRANCH_NAME)
        if git_push_result.returncode == 0:
            logging.info("Successfully committed and pushed changes.")
        else:
            logging.error("Failed to push changes to remote repository.")
    else:
        # Step 4: Revert if we used up all attempts
        logging.error(f"All {RETRY_LIMIT} attempts failed. Reverting to previous version.")

        with open(target_file, "w") as f:
            f.write(old_code)

        git_command("add", ".")
        git_command("commit", "-m", "Reverting to previous working version")
        revert_push_result = git_command("push", "origin", BRANCH_NAME)
        if revert_push_result.returncode == 0:
            logging.info("Successfully reverted to the previous working version.")
        else:
            logging.error("Failed to push the revert to the remote repository.")

if __name__ == "__main__":
    main_loop()
