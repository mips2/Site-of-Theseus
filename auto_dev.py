#!/usr/bin/env python3
"""
auto_dev.py

A production-ready autonomous script that:
1. Pulls the latest code from GitHub.
2. Uses DeepSeek to generate new code/features split across allowed files.
3. Tests changes.
4. Commits and pushes on success, or reverts on repeated failure.
   - On success, restarts 'gunicorn-theseus.service' and reloads Nginx.

Constraints:
- The AI is not allowed to edit files within website/tests.
- Any HTML must be placed in website/templates, not inline in app.py.
- The AI response may contain multiple files, indicated by lines like "File: website/somefile.py".
- If the AI attempts to modify a disallowed file, we skip it.

Additionally:
- Allows custom system prompt (configured in config.yaml or directly below).
- Supports 'manual-run' mode for a one-off iteration.
- Implements robust error handling, logging, and security checks.
"""

import os
import sys
import yaml
import time
import logging
import requests
import subprocess
from datetime import datetime
from logging.handlers import RotatingFileHandler

# -------------------------------------------------------------------------
#  Logging Setup with Rotation + Console (for manual runs)
# -------------------------------------------------------------------------
LOG_FILE = "logs/auto_dev.log"
os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=5
)
file_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(file_format)

# -------------------------------------------------------------------------
#  Load Config
# -------------------------------------------------------------------------
CONFIG_FILE = "config.yaml"
if not os.path.exists(CONFIG_FILE):
    logger.error(f"Missing config file: {CONFIG_FILE}. Exiting.")
    sys.exit(1)

with open(CONFIG_FILE, "r") as f:
    config = yaml.safe_load(f)

GITHUB_REPO = config.get("github_repo", "")
BRANCH_NAME = config.get("branch_name", "main")
RETRY_LIMIT = config.get("retry_limit", 5)
ENABLE_AUTODEV = config.get("enable_autodev", True)

# System prompt ensures DeepSeek knows it must produce compiling code and separate files properly.
SYSTEM_PROMPT = config.get(
    "system_prompt",
    "You are a helpful AI developer. Your goal is to add NEW and UNIQUE features to the existing Flask application. "
    "You must ONLY return separate code blocks for each file you are changing, clearly indicating the filename. "
    "You are NOT allowed to put HTML in app.py; place HTML in website/templates/. "
    "You are NOT allowed to modify the tests under website/tests/. "
    "Each feature must:\n"
    "1. Build upon the existing codebase.\n"
    "2. Add interactivity (e.g., buttons, forms, links).\n"
    "3. Create navigable pages with a clear user flow.\n"
    "4. Avoid trivial or redundant routes (e.g., weather reports, placeholder data).\n"
    "5. Enhance the user experience and functionality of the website.\n\n"
    "Return only code blocks labeled with 'File: ...' for each file you edit. No explanations outside code blocks."
)

USER_INSTRUCTIONS = config.get(
    "user_instructions",
    "Maintain a one-feature-at-a-time approach.\n"
    "Preserve existing functionality.\n"
    "Ensure any new routes or pages are navigable.\n"
    "Add interactive elements (e.g., buttons, forms, links).\n"
    "Avoid trivial or redundant routes (e.g., weather reports, placeholder data).\n"
    "Place all HTML in website/templates, never inline in a .py file.\n"
    "Do not edit tests in website/tests.\n"
    "Focus on features that enhance user experience and functionality."
)

# -------------------------------------------------------------------------
#  Environment Variables (DeepSeek API Key & GitHub Token)
# -------------------------------------------------------------------------
DEESEEK_API_KEY = os.environ.get("DEESEEK_API_KEY", None)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)

def validate_env_variables():
    """
    Validate essential environment variables.
    """
    if not DEESEEK_API_KEY or len(DEESEEK_API_KEY) < 10:
        logger.error("DEESEEK_API_KEY is missing or invalid. Exiting.")
        sys.exit(1)

    if not GITHUB_TOKEN:
        logger.warning("No GITHUB_TOKEN found in environment. Pushes may fail.")
    else:
        if len(GITHUB_TOKEN) < 10:
            logger.warning("GITHUB_TOKEN appears too short; push might fail.")

validate_env_variables()

# -------------------------------------------------------------------------
#  DeepSeek Integration
# -------------------------------------------------------------------------
DEESEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEESEEK_MODEL = "deepseek-chat"
MAX_TOKENS = 2500
DEESEEK_RETRIES = 3

def call_deepseek_api(payload):
    """
    Call the DeepSeek API with retry logic and exponential backoff.
    Returns the response JSON or None on failure.
    """
    headers = {
        "Authorization": f"Bearer {DEESEEK_API_KEY}",
        "Content-Type": "application/json",
    }
    for attempt in range(DEESEEK_RETRIES):
        try:
            response = requests.post(
                DEESEEK_API_URL, json=payload, headers=headers, timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"DeepSeek API call failed (attempt {attempt+1}): {e}")
            if attempt < DEESEEK_RETRIES - 1:
                backoff_time = 2 ** attempt
                logger.info(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                logger.error("All attempts to call DeepSeek API have failed.")
    return None

def generate_code_change(current_code):
    """
    Send the existing code to DeepSeek, along with instructions on how to modify it.
    Return the AI's entire raw response (which may contain multiple files).
    If DeepSeek fails, return a marker comment.
    """
    payload = {
        "model": DEESEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_INSTRUCTIONS},
            {
                "role": "user",
                "content": (
                    f"Here is the existing code:\n\n{current_code}\n\n"
                    "Return multiple code blocks if multiple files are changed, each labeled with 'File: path/to/file'. "
                    "Do not place HTML inline in .py files. Do not edit any tests in website/tests. "
                    "Return ONLY the updated code blocks."
                ),
            },
        ],
        "temperature": 0,
        "max_tokens": MAX_TOKENS,
    }

    result = call_deepseek_api(payload)
    if not result:
        return "# [DeepSeek ERROR] Could not generate new code.\n"
    try:
        ai_message = result["choices"][0]["message"]["content"].strip()
        return ai_message
    except (KeyError, IndexError) as e:
        logger.error(f"Invalid DeepSeek response structure: {e}")
        return "# [DeepSeek ERROR] Invalid response.\n"

# -------------------------------------------------------------------------
#  Multi-File Parsing
# -------------------------------------------------------------------------
def parse_ai_response_into_files(ai_response):
    """
    The AI may return multiple 'File:' blocks. Each block is surrounded by code fences:
    e.g.
    ```
    File: website/app.py
    <code here>
    ```
    We parse them out and return a dictionary: { "website/app.py": "<code>", ... }.
    We skip or ignore any file that references website/tests.
    We also skip any HTML inline in .py code, but we do allow separate .html files under website/templates.
    """
    files_dict = {}
    # Split on triple backticks
    segments = ai_response.split("```")
    for seg in segments:
        seg = seg.strip()
        if seg.startswith("File: "):
            # Extract the filename from the first line, then the remainder as code
            lines = seg.splitlines()
            filename_line = lines[0]
            code_lines = lines[1:]
            # e.g. "File: website/app.py"
            _, file_path = filename_line.split("File: ", 1)
            file_path = file_path.strip()
            # Skip if referencing tests
            if file_path.startswith("website/tests"):
                logger.warning(f"AI attempted to modify tests file '{file_path}'. Skipping.")
                continue
            # If referencing a .py file but there's <html>, remove that
            if file_path.endswith(".py"):
                joined_code = "\n".join(code_lines)
                if "<html>" in joined_code.lower():
                    logger.warning(f"AI inline HTML in .py file '{file_path}' - removing HTML block.")
                    # We do a naive removal of anything from <html> to </html>
                    while "<html>" in joined_code.lower():
                        start_idx = joined_code.lower().find("<html>")
                        end_idx = joined_code.lower().find("</html>", start_idx)
                        if end_idx == -1:
                            break
                        end_idx += len("</html>")
                        joined_code = joined_code[:start_idx] + "# [HTML REMOVED]\n" + joined_code[end_idx:]
                    code_lines = joined_code.splitlines()
                files_dict[file_path] = "\n".join(code_lines)
            else:
                # For HTML or other file types, store as is
                files_dict[file_path] = "\n".join(code_lines)
    return files_dict

# -------------------------------------------------------------------------
#  Template Handling
# -------------------------------------------------------------------------
def ensure_file_exists(file_path, default_content=""):
    """
    Ensure a file exists. If it doesn't, create it with default content.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_content)
        logger.info(f"Created file: {file_path}")

# -------------------------------------------------------------------------
#  Testing
# -------------------------------------------------------------------------
def check_tests_exist(test_path="website/tests/"):
    """
    Quick check if the tests directory is present and non-empty.
    """
    if not os.path.exists(test_path):
        logger.warning("Test directory does not exist. Tests may be incomplete.")
    elif not os.listdir(test_path):
        logger.warning("Test directory is empty. Tests may be incomplete.")

def run_test_commands():
    """
    Install dependencies from website/requirements.txt, then run pytest.
    Return True if tests pass, False otherwise.
    """
    req_file = "website/requirements.txt"
    if not os.path.exists(req_file):
        logger.warning("requirements.txt not found. Dependencies may be incomplete.")
    else:
        try:
            proc_install = subprocess.run(
                ["pip", "install", "-r", req_file],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(proc_install.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Dependency installation failed: {e.stderr}")
            return False

    check_tests_exist()

    try:
        subprocess.check_call(["pytest", "website/tests/", "--maxfail=1"])
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Test failed: {e}")
        return False

# -------------------------------------------------------------------------
#  Git Helpers
# -------------------------------------------------------------------------
def git_command(*args):
    """
    Run git commands, logging output.
    """
    cmd = ["git"] + list(args)
    logger.info(f"Running git command: {' '.join(cmd)}")
    env = os.environ.copy()
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error(f"Git command error: {result.stderr.strip()}")
    else:
        logger.info(f"Git command success: {result.stdout.strip()}")
    return result

def revert_to_previous_commit():
    """
    Hard reset to HEAD~1, forcibly discarding local changes.
    """
    logger.info("Reverting to the previous commit with git reset --hard HEAD~1.")
    git_command("reset", "--hard", "HEAD~1")

# -------------------------------------------------------------------------
#  Systemd Service Handling
# -------------------------------------------------------------------------
def check_service_exists(service_name):
    try:
        result = subprocess.run(
            ["systemctl", "status", service_name],
            capture_output=True,
            text=True
        )
        if "Loaded: not-found" in result.stdout:
            return False
        return True
    except Exception as e:
        logger.error(f"Failed checking service {service_name}: {e}")
        return False

def restart_service(service_name):
    """
    Restart systemd service if it exists, then log status.
    """
    if not check_service_exists(service_name):
        logger.error(f"Service {service_name} not found.")
        return
    try:
        logger.info(f"Restarting {service_name}...")
        subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart {service_name}: {e}")
        return
    try:
        post_check = subprocess.run(
            ["systemctl", "is-active", service_name],
            capture_output=True, text=True
        )
        if post_check.stdout.strip() == "active":
            logger.info(f"{service_name} is running.")
        else:
            logger.warning(f"{service_name} is not active after restart.")
    except Exception as e:
        logger.error(f"Error checking {service_name} status: {e}")

def reload_nginx():
    """
    Reload nginx if it exists.
    """
    svc = "nginx"
    if not check_service_exists(svc):
        logger.error("nginx service not found.")
        return
    try:
        logger.info("Reloading nginx...")
        subprocess.run(["sudo", "systemctl", "reload", svc], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to reload nginx: {e}")
        return
    try:
        result = subprocess.run(
            ["systemctl", "is-active", svc],
            capture_output=True, text=True
        )
        if result.stdout.strip() == "active":
            logger.info("nginx is running.")
        else:
            logger.warning("nginx is not active after reload.")
    except Exception as e:
        logger.error(f"Error checking nginx status: {e}")

# -------------------------------------------------------------------------
#  Main Automated Loop
# -------------------------------------------------------------------------
def main_loop():
    """
    1. Pull the latest code.
    2. Generate new files from AI (retry up to RETRY_LIMIT times).
    3. Write them to the correct locations (skipping website/tests).
    4. Test, commit, push, and restart services if success; otherwise revert.
    """
    if not ENABLE_AUTODEV:
        logger.info("AUTO-DEV is disabled in config.yaml. Exiting.")
        return

    git_command("pull", "origin", BRANCH_NAME)

    # We'll keep the old version of app.py to revert if needed
    app_path = "website/app.py"
    if not os.path.exists(app_path):
        logger.error(f"{app_path} does not exist! Cannot proceed.")
        return
    with open(app_path, "r", encoding="utf-8") as f:
        old_app_code = f.read()

    success = False
    current_code = old_app_code

    for attempt in range(1, RETRY_LIMIT + 1):
        logger.info(f"Generation attempt #{attempt} of {RETRY_LIMIT}.")
        ai_response = generate_code_change(current_code)

        # Parse AI response into multiple files
        files_dict = parse_ai_response_into_files(ai_response)
        if not files_dict:
            logger.warning("AI did not return any valid file changes.")
            # If no changes, skip testing (nothing changed).
            # We'll proceed to next attempt, or revert if out of attempts.
            continue

        # Write changes to disk
        for filepath, code_str in files_dict.items():
            # If app.py is updated, remember that as our 'current_code' for next iteration
            if filepath == "website/app.py":
                current_code = code_str
            # Create directories if missing, write new code
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as fw:
                fw.write(code_str)
            logger.info(f"Updated file: {filepath}")

        # Now run tests
        if run_test_commands():
            success = True
            break
        else:
            logger.warning("Test failed. Will retry.")

    if success:
        git_command("add", ".")
        commit_msg = f"Auto-update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        push_res = git_command("push", "origin", BRANCH_NAME)
        if push_res.returncode == 0:
            logger.info("Successfully pushed changes.")
          #  restart_service("gunicorn-theseus.service")
            reload_nginx()
        else:
            logger.error("Push failed. Attempting revert to previous commit.")
            revert_to_previous_commit()
    else:
        logger.error(f"All {RETRY_LIMIT} attempts failed. Reverting to previous commit.")
        revert_to_previous_commit()
        force_push_res = git_command("push", "origin", BRANCH_NAME, "--force")
        if force_push_res.returncode == 0:
            logger.info("Successfully forced a revert to remote.")
        else:
            logger.error("Failed to push revert. Local is reverted, remote may be out of sync.")

# -------------------------------------------------------------------------
#  Manual Run (One-Off Iteration)
# -------------------------------------------------------------------------
def manual_run():
    """
    One-off: 
    1. Pull latest code.
    2. Generate changes from AI.
    3. Write them, test, if fail revert, if success push and restart services.
    Shows console logs for real-time feedback.
    """
    logger.addHandler(console_handler)  # Real-time console output

    logger.info("Starting MANUAL RUN of AI code update process.")
    git_command("pull", "origin", BRANCH_NAME)

    app_path = "website/app.py"
    if not os.path.exists(app_path):
        logger.error(f"{app_path} does not exist! Cannot proceed.")
        return

    with open(app_path, "r", encoding="utf-8") as f:
        old_app_code = f.read()

    ai_response = generate_code_change(old_app_code)
    files_dict = parse_ai_response_into_files(ai_response)
    if not files_dict:
        logger.warning("AI did not return any valid file changes during manual run.")
        return

    # Write changes
    current_app_code = old_app_code
    for filepath, code_str in files_dict.items():
        if filepath == "website/app.py":
            current_app_code = code_str
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fw:
            fw.write(code_str)
        logger.info(f"[MANUAL RUN] Updated file: {filepath}")

    # Test
    if run_test_commands():
        logger.info("Tests passed.")
        git_command("add", ".")
        commit_msg = f"Manual-run update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        push_res = git_command("push", "origin", BRANCH_NAME)
        if push_res.returncode == 0:
            logger.info("Manual-run: Pushed successfully.")
            restart_service("gunicorn-theseus.service")
            reload_nginx()
        else:
            logger.error("Manual-run: Push failed. Reverting local commit.")
            revert_to_previous_commit()
    else:
        logger.error("Manual-run: Tests failed. Reverting local changes.")
        with open(app_path, "w", encoding="utf-8") as fw:
            fw.write(old_app_code)
        git_command("add", "website/app.py")
        git_command("commit", "-m", "Manual-run revert to old code")
        revert_push = git_command("push", "origin", BRANCH_NAME, "--force")
        if revert_push.returncode == 0:
            logger.info("Successfully forced a revert.")
        else:
            logger.error("Failed to push revert. Local is reverted, remote may differ.")

# -------------------------------------------------------------------------
#  Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "manual-run":
        manual_run()
    else:
        main_loop()
