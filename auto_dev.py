#!/usr/bin/env python3
"""
auto_dev.py

An autonomous script that:
1. Pulls the latest code from GitHub.
2. Uses DeepSeek to generate new code features.
3. Tests changes.
4. Commits and pushes on success, or reverts on repeated failure.

Additionally:
- Allows custom system prompt (configured in config.yaml or directly below).
- Supports 'manual-run' mode for a one-off iteration.
"""

import os
import subprocess
import sys
import yaml
import logging
import requests
from datetime import datetime

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

# This system prompt ensures DeepSeek knows it must produce compiling code.
SYSTEM_PROMPT = config.get(
    "system_prompt",
    "You are a helpful AI developer. Your goal is to add a NEW and UNIQUE feature "
    "that compiles/passes tests successfully. Stability and correctness are top priority."
)

# Additional user instructions if needed
USER_INSTRUCTIONS = config.get(
    "user_instructions",
    "Please enhance this Flask code by adding a new route or improving functionality. "
    "Ensure the code is valid Python and doesn't break existing routes."
)

# ------------------------------------------------------------------------------
#  DeepSeek API Key
# ------------------------------------------------------------------------------
# !!! WARNING: Ideally store this in environment variables or a secret manager.
DEESEEK_API_KEY = os.environ.get("DEESEEK_API_KEY", None)
if not DEESEEK_API_KEY:
    logging.error("No DeepSeek API key provided. Exiting.")
    sys.exit(1)

# ------------------------------------------------------------------------------
#  GitHub Token (Optional)
# ------------------------------------------------------------------------------
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

    payload = {
        "model": DEESEEK_MODEL,
        "messages": [
            {
                "role": "system", 
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": USER_INSTRUCTIONS
            },
            {
                "role": "user",
                "content": (
                    f"Here is the existing code:\n\n{current_code}\n\n"
                    "Return ONLY the updated code. Make sure it compiles and doesn't break existing tests."
                ),
            },
        ],
    }

    headers = {
        "Authorization": f"Bearer {DEESEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(
            DEESEEK_API_URL, json=payload, headers=headers, timeout=60
        )
        response.raise_for_status()
        result = response.json()
        ai_message = result["choices"][0]["message"]["content"]

        # Attempt to extract code from possible code fences
        if "```" in ai_message:
            splitted = ai_message.split("```")
            # The code block could be splitted[1] or splitted[2], etc.
            # We'll just look for the largest chunk that looks like code.
            code_blocks = [chunk.strip() for chunk in splitted if chunk.strip()]
            # Attempt to filter out 'python' or any language spec
            # We'll pick the chunk with the most lines as the code block
            code_blocks_sorted = sorted(code_blocks, key=lambda x: len(x), reverse=True)
            code_part = code_blocks_sorted[0]
            # Remove language annotation if present
            code_part = code_part.replace("python", "").strip()
            return code_part
        else:
            return ai_message.strip()

    except requests.exceptions.RequestException as e:
        logging.error(f"DeepSeek API call failed: {e}")
        return current_code + "\n# [DeepSeek ERROR] Could not generate new code.\n"

# ------------------------------------------------------------------------------
#  Testing
# ------------------------------------------------------------------------------
def run_test_commands():
    """
    Install dependencies and run tests to ensure the new code is valid.
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
        # Optionally, we can set env vars for Git-based authentication:
        # env["GIT_ASKPASS"] = "echo"
        # env["GIT_USERNAME"] = "YourUsername"
        # env["GIT_PASSWORD"] = GITHUB_TOKEN
        pass

    result = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logging.error(f"Git command error: {result.stderr.strip()}")
    else:
        logging.info(f"Git command success: {result.stdout.strip()}")
    return result

# ------------------------------------------------------------------------------
#  Main Automated Loop
# ------------------------------------------------------------------------------
def main_loop():
    """
    Automates the entire process:
    1. Pull latest code.
    2. Generate new code (retry up to RETRY_LIMIT times).
    3. Run tests.
    4. Commit/push if successful, revert if not.
    """
    if not ENABLE_AUTODEV:
        logging.info("AUTO-DEV is disabled in config.yaml. Exiting gracefully.")
        return

    # Pull latest code
    git_command("pull", "origin", BRANCH_NAME)

    target_file = "website/app.py"
    if not os.path.exists(target_file):
        logging.error(f"{target_file} does not exist! Cannot proceed.")
        return

    # Read original code
    with open(target_file, "r") as f:
        old_code = f.read()

    new_code = old_code
    success = False

    for attempt in range(1, RETRY_LIMIT + 1):
        logging.info(f"Attempt #{attempt} to generate feature and test.")

        # Generate code from DeepSeek
        new_code = generate_code_change(new_code)

        # Write changes to file
        with open(target_file, "w") as f:
            f.write(new_code)

        # Run tests
        if run_test_commands():
            success = True
            break
        else:
            logging.warning(f"Test failed on attempt #{attempt}. Retrying...")

    if success:
        # Commit and push
        git_command("add", ".")
        commit_msg = f"Auto-update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        git_push_result = git_command("push", "origin", BRANCH_NAME)
        if git_push_result.returncode == 0:
            logging.info("Successfully committed and pushed changes.")
        else:
            logging.error("Failed to push changes to remote repository.")
    else:
        # Revert to original code
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

# ------------------------------------------------------------------------------
#  Manual Run (One-Off Iteration)
# ------------------------------------------------------------------------------
def manual_run():
    """
    Perform a single iteration of:
    1. Generate code once.
    2. Test it.
    3. If success, commit/push. If fail, revert.

    Useful for manual testing before letting the script run automatically.
    """
    logging.info("Starting MANUAL RUN of the AI code update process.")

    git_command("pull", "origin", BRANCH_NAME)

    target_file = "website/app.py"
    if not os.path.exists(target_file):
        logging.error(f"{target_file} does not exist! Cannot proceed.")
        return

    # Backup old code
    with open(target_file, "r") as f:
        old_code = f.read()

    # Generate code once
    new_code = generate_code_change(old_code)
    with open(target_file, "w") as f:
        f.write(new_code)

    # Run tests
    if run_test_commands():
        logging.info("Manual run: Tests passed on first try.")
        git_command("add", ".")
        commit_msg = f"Manual-run update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        git_push_result = git_command("push", "origin", BRANCH_NAME)
        if git_push_result.returncode == 0:
            logging.info("Manual-run: Successfully committed and pushed changes.")
        else:
            logging.error("Manual-run: Failed to push changes.")
    else:
        logging.error("Manual run: Tests failed. Reverting to old code.")
        with open(target_file, "w") as f:
            f.write(old_code)

        git_command("add", ".")
        git_command("commit", "-m", "Manual-run revert to previous working version")
        revert_push_result = git_command("push", "origin", BRANCH_NAME)
        if revert_push_result.returncode == 0:
            logging.info("Manual-run: Successfully reverted to the previous version.")
        else:
            logging.error("Manual-run: Failed to push revert.")

# ------------------------------------------------------------------------------
#  Entry Point
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    # If you run "python auto_dev.py manual-run",
    # we'll do a one-off iteration (manual_run) instead of the full main_loop.
    if len(sys.argv) > 1 and sys.argv[1] == "manual-run":
        manual_run()
    else:
        main_loop()
