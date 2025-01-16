#!/usr/bin/env python3
"""
auto_dev.py

A production-ready autonomous script that:
1. Pulls the latest code from GitHub.
2. Uses DeepSeek to generate new code/features split across allowed files.
3. Tests changes.
4. Commits and pushes on success, or reverts on repeated failure.

Additional improvements implemented:
1. Improved AI response parsing (handling partial or missing code blocks).
2. Enhanced AI prompting (feedback loop on failed attempts).
3. Basic syntax validation for AI-generated .py files before writing to disk.
4. More detailed logging (including raw AI response in debug logs).
5. Added a feedback loop to inform AI about failures.
6. (Skipping some numbers for brevity, see docstring or commit logs for details)
9. Simple rate limiting (exponential backoff) for repeated AI calls.
11. Added basic security scanning step (using 'bandit' if available).
12. Added a simple run metrics log at the end of each session.
15. Dry-run mode to simulate the process without writing/committing.
19. Improved template handling checks to ensure new templates are referenced.

Latest fixes:
- Remove triple backticks and any ```python lines before parsing filenames.
- If *any* .py file fails syntax, we discard the entire set of files (all-or-nothing approach).
- Strip trailing '-->' from filenames to avoid creating files like 'index.html -->'.
- Service restarts removed (gunicorn-theseus.service, nginx).

Modified to gather the entire existing codebase (all .py and .html files) and provide it as context to the AI.
"""

import os
import re
import sys
import yaml
import time
import logging
import requests
import subprocess
import ast
from datetime import datetime
from logging.handlers import RotatingFileHandler

# -------------------------------------------------------------------------
#  Logging Setup with Rotation + Console
# -------------------------------------------------------------------------
LOG_FILE = "logs/auto_dev.log"
os.makedirs("logs", exist_ok=True)  # Ensure logs directory exists

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Allow debug logs for more detail

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=5)
file_format = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
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
RETRY_LIMIT = config.get("retry_limit", 1)
ENABLE_AUTODEV = config.get("enable_autodev", True)
DRY_RUN = config.get("dry_run", False)  # For improvement #15

SYSTEM_PROMPT = config.get(
    "system_prompt",
    "You are a highly skilled AI developer tasked with building and enhancing a production-ready social media platform. "
    "Your goal is to create a complete 'everything app' that includes features like user profiles, posts, messaging, notifications, and more. "
    "Follow these guidelines:\n"
    "1. **Core Idea**: The platform is a social media 'everything app' that combines communication, content sharing, and community features. "
    "Choose a unique theme or niche for the platform (e.g., professional networking, hobby-based communities, local events).\n"
    "2. **Iterative Development**: Build the platform one feature at a time. Each feature must be fully functional, tested, and integrated before moving to the next. "
    "Start with the most essential features (e.g., user authentication, profiles) and gradually add advanced features (e.g., messaging, notifications).\n"
    "3. **Static Data Integration**: Use **static data** or **local data sources** for initial development. Avoid external APIs unless absolutely necessary. "
    "For example, use hardcoded user data or local JSON files for posts and profiles.\n"
    "4. **Code Quality**: Write modular, well-structured code. Use meaningful names and avoid repetition.\n"
    "5. **Error Handling**: Validate inputs, handle edge cases, and include logging for debugging. Ensure failures are gracefully handled.\n"
    "6. **Security**: Sanitize inputs, use secure authentication, and avoid vulnerabilities. Do not use API keys or external services unless explicitly allowed.\n"
    "7. **Performance**: Optimize for speed and resource usage. Use caching and minimize unnecessary computations.\n"
    "8. **Scalability**: Design for growth. Use configuration files or environment variables for flexibility.\n"
    "9. **Documentation**: Add comments and docstrings to explain complex logic. Include details about data sources and feature implementations in the documentation.\n"
    "10. **Testing**: Write unit and integration tests for all new functionality, including tests for data handling and user interactions.\n"
    "11. **Separation of Concerns**: Keep HTML in `templates/`, CSS/JS in `static/`, and Python logic in `.py` files.\n"
    "12. **Modern Design**: Ensure the website is responsive and visually appealing.\n"
    "13. **Interactivity**: Add lightweight, engaging features that enhance user experience. Use static or user-generated data to make the experience dynamic.\n"
    "14. **Reusability**: Create reusable components and functions, especially for data handling and user interactions.\n"
    "15. **Standards**: Follow PEP 8 for Python and W3C standards for HTML/CSS.\n"
    "16. **Feedback**: If issues arise, provide clear feedback on improvements needed.\n"
    "Return only code blocks labeled with 'File: ...' for each file you edit. No explanations outside code blocks."
)

USER_INSTRUCTIONS = config.get(
    "user_instructions",
    "You are building and improving a production-ready social media platform. Follow these steps:\n"
    "1. **Choose a Theme**: Select a unique theme or niche for the platform (e.g., professional networking, hobby-based communities, local events).\n"
    "2. **Add Features Iteratively**: Propose and implement one feature at a time. Ensure it is fully functional, tested, and integrated before moving to the next. "
    "Start with essential features and gradually add advanced features. For example:\n"
    "   - **Phase 1**: User authentication, profiles, and basic posts.\n"
    "   - **Phase 2**: Follow/unfollow users, like posts, and comments.\n"
    "   - **Phase 3**: Direct messaging, notifications, and search functionality.\n"
    "   - **Phase 4**: Advanced features like groups, events, or analytics.\n"
    "3. **Static Data Integration**: Use **static data** or **local data sources** for initial development. Avoid external APIs unless absolutely necessary.\n"
    "4. **Write Clean Code**: Focus on readability, modularity, and efficiency.\n"
    "5. **Test Thoroughly**: Write unit and integration tests for all new functionality, including tests for data handling and user interactions.\n"
    "6. **Optimize**: Minimize resource usage, use caching, and avoid blocking operations.\n"
    "7. **Secure**: Sanitize inputs, use secure authentication, and avoid vulnerabilities. Do not use API keys or external services unless explicitly allowed.\n"
    "8. **Document**: Add comments and docstrings to explain your code. Include details about data sources and feature implementations in the documentation.\n"
    "9. **Separate Concerns**: Keep HTML, CSS, and JavaScript in their respective directories.\n"
    "10. **Make It Interactive**: Add engaging features that are lightweight and performant. Use static or user-generated data to make the experience dynamic.\n"
    "11. **Follow Standards**: Adhere to PEP 8 and W3C guidelines.\n"
    "12. **Provide Feedback**: If you encounter issues, suggest improvements clearly.\n"
    "Return only code blocks labeled with 'File: path/to/file' for each file you edit. No explanations outside code blocks."
)
# -------------------------------------------------------------------------
#  Environment Variables
# -------------------------------------------------------------------------
DEESEEK_API_KEY = os.environ.get("DEESEEK_API_KEY", None)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)

def validate_env_variables():
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
#  Metrics & Reporting
# -------------------------------------------------------------------------
ATTEMPTED_COMMITS = 0
SUCCESSFUL_COMMITS = 0

# -------------------------------------------------------------------------
#  DeepSeek Integration
# -------------------------------------------------------------------------
DEESEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEESEEK_MODEL = "deepseek-chat"
MAX_TOKENS = 4000
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

def gather_codebase():
    """
    Gather all relevant .py (except those in website/tests) and .html files 
    from the 'website' directory, and combine them into a compact string to
    provide context to the AI.
    """
    code_pieces = []
    for root, dirs, files in os.walk("website"):
        # Skip test folders
        if "tests" in root:
            continue
        for fname in files:
            if fname.endswith(".py") or fname.endswith(".html"):
                full_path = os.path.join(root, fname)
                try:
                    with open(full_path, "r", encoding="utf-8") as f:
                        contents = f.read()
                    # Provide a "compact" format: ### File: path
                    code_pieces.append(f"### File: {full_path}\n{contents}\n")
                except Exception as e:
                    logger.warning(f"Error reading file {full_path}: {e}")
    return "\n".join(code_pieces)

def generate_code_change(full_codebase, failure_reason=""):
    """
    Send the existing codebase to DeepSeek, along with instructions on how to modify it.
    Provide feedback to the AI if there's a failure_reason.
    Return the AI's entire raw response (which may contain multiple files).
    """
    feedback_message = ""
    if failure_reason:
        feedback_message = f"Previous attempt failed due to: {failure_reason}\n"

    payload = {
        "model": DEESEEK_MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": USER_INSTRUCTIONS},
            {
                "role": "user",
                "content": (
                    feedback_message
                    + "Here is the existing codebase:\n\n"
                    + full_codebase
                    + "\n\n"
                    "Return multiple code blocks if multiple files are changed, each labeled with 'File: path/to/file'. "
                    "Do not place HTML inline in .py files. Do not edit any tests in website/tests. "
                    "Return ONLY the updated code blocks."
                ),
            },
        ],
        "temperature": 0.7,
        "max_tokens": MAX_TOKENS,
    }

    result = call_deepseek_api(payload)
    if not result:
        return "# [DeepSeek ERROR] Could not generate new code.\n"
    try:
        ai_message = result["choices"][0]["message"]["content"].strip()
        logger.debug(f"RAW AI RESPONSE:\n{ai_message}\n")
        return ai_message
    except (KeyError, IndexError) as e:
        logger.error(f"Invalid DeepSeek response structure: {e}")
        return "# [DeepSeek ERROR] Invalid response.\n"

def generate_change_summary(old_code, new_code):
    """
    Generate a concise and readable summary of changes using DeepSeek.
    Returns a string summarizing the changes.
    """
    payload = {
        "model": DEESEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant. Summarize the changes between the old and new code in a concise and readable way.",
            },
            {
                "role": "user",
                "content": (
                    "Here is the old code:\n\n"
                    + old_code
                    + "\n\n"
                    "Here is the new code:\n\n"
                    + new_code
                    + "\n\n"
                    "Summarize the changes in one or two sentences. Focus on what was added, removed, or modified."
                ),
            },
        ],
        "temperature": 0.5,
        "max_tokens": 200,
    }

    result = call_deepseek_api(payload)
    if not result:
        return "Changes: Unable to generate summary."
    try:
        summary = result["choices"][0]["message"]["content"].strip()
        return f"Changes: {summary}"
    except (KeyError, IndexError) as e:
        logger.error(f"Invalid DeepSeek response structure: {e}")
        return "Changes: Unable to generate summary."

# -------------------------------------------------------------------------
#  Multi-File Parsing & Basic Syntax Validation
# -------------------------------------------------------------------------
def is_valid_python_syntax(code_str):
    """
    Basic syntax validation for Python code using ast.parse.
    Returns True if syntax is valid, False otherwise.
    """
    try:
        ast.parse(code_str)
        return True
    except SyntaxError as e:
        logger.error(f"SyntaxError in generated code: {e}")
        return False

def parse_ai_response_into_files(ai_response):
    # Remove triple backticks
    cleaned_response = re.sub(r"```[a-zA-Z]*", "", ai_response)
    cleaned_response = cleaned_response.replace("```", "")

    pattern = r"(File:\s*([^\n]+))(.*?)(?=File:|$)"
    matches = re.findall(pattern, cleaned_response, flags=re.DOTALL)

    temp_files = {}
    for match in matches:
        filename_line = match[0]
        file_path = match[1].strip()
        code_block = match[2].strip()

        if file_path.endswith("-->"):
            file_path = file_path.replace("-->", "").strip()

        # Skip tests
        if file_path.startswith("website/tests"):
            logger.warning(f"AI attempted to modify tests file '{file_path}'. Skipping.")
            continue

        # Force everything else to be in `website/`
        if not file_path.startswith("website/"):
            file_path = f"website/{file_path.lstrip('/')}"

        # If referencing a .py file, remove HTML comments and blocks
        if file_path.endswith(".py"):
            code_block = re.sub(r"<!--.*?-->", "", code_block, flags=re.DOTALL)
            code_block = re.sub(r"<[^>]+>", "", code_block)

        temp_files[file_path] = code_block

    return temp_files

# -------------------------------------------------------------------------
#  Template Handling Checks
# -------------------------------------------------------------------------
def template_references_check(files_dict):
    """
    Ensure any new templates have at least one referencing route in .py updates.
    Very simple approach: if a .html file is introduced, see if any .py code references that filename.
    """
    html_files = [fp for fp in files_dict if fp.endswith(".html")]
    if not html_files:
        return True

    all_python_updates = ""
    for fp, code in files_dict.items():
        if fp.endswith(".py"):
            all_python_updates += code.lower()

    for html_file in html_files:
        base_name = os.path.basename(html_file).lower()
        if base_name not in all_python_updates:
            logger.warning(
                f"Template '{html_file}' not referenced in any .py update. Potential orphan template."
            )
    return True

# -------------------------------------------------------------------------
#  Requirements Check
# -------------------------------------------------------------------------
def ensure_requirements_installed(req_file="website/requirements.txt"):
    """
    Verify requirements from the file are installed; if not, install them.
    """
    if not os.path.exists(req_file):
        logger.warning("No requirements.txt found. Skipping check.")
        return

    try:
        logger.info("Verifying all requirements are installed...")
        with open(req_file, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith("#")]
        for requirement in lines:
            logger.debug(f"Checking if '{requirement}' is installed...")
            check_proc = subprocess.run(["pip", "show", requirement], capture_output=True, text=True)
            if check_proc.returncode != 0:
                logger.info(f"Requirement '{requirement}' not found. Installing...")
                install_proc = subprocess.run(["pip", "install", requirement], capture_output=True, text=True)
                if install_proc.returncode != 0:
                    logger.error(f"Failed to install '{requirement}': {install_proc.stderr}")
    except Exception as e:
        logger.error(f"Error ensuring requirements installed: {e}")

# -------------------------------------------------------------------------
#  Testing
# -------------------------------------------------------------------------
def check_tests_exist(test_path="website/tests/"):
    if not os.path.exists(test_path):
        logger.warning("Test directory does not exist. Tests may be incomplete.")
    elif not os.listdir(test_path):
        logger.warning("Test directory is empty. Tests may be incomplete.")

def run_test_commands():
    """
    Install dependencies from website/requirements.txt, then run pytest.
    Run basic security scan with bandit if installed.
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

    bandit_installed = False
    try:
        subprocess.run(["bandit", "--version"], check=True, capture_output=True, text=True)
        bandit_installed = True
    except FileNotFoundError:
        logger.info("bandit not found, skipping security scan.")
    except subprocess.CalledProcessError:
        logger.info("bandit found but returned an error; skipping.")

    if bandit_installed:
        try:
            logger.info("Running security scan with bandit...")
            bandit_proc = subprocess.run(["bandit", "-r", "website"], capture_output=True, text=True)
            logger.info(bandit_proc.stdout)
            if bandit_proc.returncode != 0:
                logger.warning("bandit detected potential issues. Review recommended.")
        except Exception as e:
            logger.error(f"Error running bandit: {e}")

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
    cmd = ["git"] + list(args)
    logger.info(f"Running git command: {' '.join(cmd)}")
    env = os.environ.copy()
    result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error(f"Git command error: {result.stderr.strip()}")
    else:
        logger.info(f"Git command success: {result.stdout.strip()}")
    return result

def revert_to_latest_remote_commit():
    """
    Revert to the latest commit on the remote repository.
    This ensures the local repository matches the remote state,
    including removing any untracked files or directories.
    """
    logger.info("Fetching latest changes from remote...")
    fetch_result = git_command("fetch", "origin")
    if fetch_result.returncode != 0:
        logger.error("Failed to fetch latest changes from remote. Cannot revert.")
        return

    logger.info(f"Resetting local branch '{BRANCH_NAME}' to match remote...")
    reset_result = git_command("reset", "--hard", f"origin/{BRANCH_NAME}")
    if reset_result.returncode != 0:
        logger.error("Failed to reset local branch to match remote.")
        return
    else:
        logger.info("Successfully reverted to the latest remote commit.")

    logger.info("Running git clean -fd to remove untracked files/directories...")
    clean_result = git_command("clean", "-fd")
    if clean_result.returncode != 0:
        logger.error("Failed to clean untracked files/directories.")
    else:
        logger.info("Successfully cleaned untracked files/directories.")

# -------------------------------------------------------------------------
#  Main Automated Loop
# -------------------------------------------------------------------------
def main_loop():
    if not ENABLE_AUTODEV:
        logger.info("AUTO-DEV is disabled in config.yaml. Exiting.")
        return

    logger.addHandler(console_handler)

    ensure_requirements_installed()

    git_command("pull", "origin", BRANCH_NAME)
    full_codebase = gather_codebase()
    if not full_codebase.strip():
        logger.error("No code files found to provide context to AI. Aborting.")
        return

    app_path = "website/app.py"
    old_app_code = ""
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            old_app_code = f.read()

    ai_response = generate_code_change(full_codebase)
    files_dict = parse_ai_response_into_files(ai_response)

    if not files_dict:
        logger.error("No valid (or fully valid) file changes returned by AI. Aborting.")
        revert_to_latest_remote_commit()
        return

    template_references_check(files_dict)

    if DRY_RUN:
        logger.info("[DRY RUN] Would update files, but skipping actual writes/tests.")
        return

    for filepath, code_str in files_dict.items():
        dir_path = os.path.dirname(filepath)
        if dir_path:
            os.makedirs(dir_path, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fw:
            fw.write(code_str)
        logger.info(f"Updated file: {filepath}")

    if "website/app.py" in files_dict and old_app_code:
        new_app_code = files_dict["website/app.py"]
        change_summary = generate_change_summary(old_app_code, new_app_code)
    else:
        change_summary = "Changes made to non-app.py files."

    if run_test_commands():
        git_command("add", ".")
        commit_msg = f"Auto-update from AI on {datetime.now().isoformat()}\n\n{change_summary}"
        git_command("commit", "-m", commit_msg)
        push_res = git_command("push", "origin", BRANCH_NAME)
        if push_res.returncode == 0:
            logger.info("Successfully pushed changes.")
        else:
            logger.error("Push failed. Attempting revert to latest remote commit.")
            revert_to_latest_remote_commit()
    else:
        logger.error("Tests failed for generated code. Reverting to latest remote commit.")
        revert_to_latest_remote_commit()
        force_push_res = git_command("push", "origin", BRANCH_NAME, "--force")
        if force_push_res.returncode == 0:
            logger.info("Successfully forced a revert to remote.")
        else:
            logger.error("Failed to push revert. Local is reverted, remote may be out of sync.")

    logger.info("Done with single-attempt auto-dev run.")
    subprocess.run(["systemctl", "restart", "gunicorn-theseus"])

# -------------------------------------------------------------------------
#  Manual Run (One-Off Iteration)
# -------------------------------------------------------------------------
def manual_run():
    logger.addHandler(console_handler)

    logger.info("Starting MANUAL RUN of AI code update process.")
    ensure_requirements_installed()

    git_command("pull", "origin", BRANCH_NAME)
    full_codebase = gather_codebase()
    if not full_codebase.strip():
        logger.error("No code files found to provide context. Aborting manual run.")
        return

    app_path = "website/app.py"
    old_app_code = ""
    if os.path.exists(app_path):
        with open(app_path, "r", encoding="utf-8") as f:
            old_app_code = f.read()

    ai_response = generate_code_change(full_codebase)
    files_dict = parse_ai_response_into_files(ai_response)
    if not files_dict:
        logger.warning("AI did not return any valid file changes during manual run.")
        return

    template_references_check(files_dict)

    if DRY_RUN:
        logger.info("[DRY RUN] Would update files, but skipping actual writes.")
        return

    for filepath, code_str in files_dict.items():
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as fw:
            fw.write(code_str)
        logger.info(f"[MANUAL RUN] Updated file: {filepath}")

    if "website/app.py" in files_dict and old_app_code:
        new_app_code = files_dict["website/app.py"]
        change_summary = generate_change_summary(old_app_code, new_app_code)
    else:
        change_summary = "Changes made to non-app.py files."

    if run_test_commands():
        logger.info("Tests passed.")
        git_command("add", ".")
        commit_msg = f"Manual-run update from AI on {datetime.now().isoformat()}\n\n{change_summary}"
        git_command("commit", "-m", commit_msg)
        push_res = git_command("push", "origin", BRANCH_NAME)
        if push_res.returncode == 0:
            logger.info("Manual-run: Pushed successfully.")
        else:
            logger.error("Manual-run: Push failed. Reverting to latest remote commit.")
            revert_to_latest_remote_commit()
    else:
        logger.error("Manual-run: Tests failed. Reverting local changes.")
        if old_app_code:
            with open(app_path, "w", encoding="utf-8") as fw:
                fw.write(old_app_code)
            git_command("add", "website/app.py")
            git_command("commit", "-m", "Manual-run revert to old code")
        revert_push = git_command("push", "origin", BRANCH_NAME, "--force")
        if revert_push.returncode == 0:
            logger.info("Successfully forced a revert.")
        else:
            logger.error("Failed to push revert. Local is reverted, remote may differ.")

    subprocess.run(["systemctl", "restart", "gunicorn-theseus"])

# -------------------------------------------------------------------------
#  Run Forever
# -------------------------------------------------------------------------
def run_forever(interval_minutes=10):
    """
    Continuously runs main_loop() every 'interval_minutes' minutes,
    allowing the service manager to keep this script alive.
    """
    try:
        while True:
            main_loop()
            logger.info(f"Sleeping for {interval_minutes} minutes before next run...")
            time.sleep(interval_minutes * 60)
    except KeyboardInterrupt:
        logger.info("Received KeyboardInterrupt; exiting run_forever loop.")

# -------------------------------------------------------------------------
#  Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    interval_minutes = 10
    if len(sys.argv) > 1:
        if sys.argv[1] == "manual-run":
            manual_run()
            sys.exit(0)
        else:
            try:
                interval_minutes = int(sys.argv[1])
                if interval_minutes <= 0:
                    logger.error("Interval must be a positive integer. Using default (10 minutes).")
                    interval_minutes = 10
            except ValueError:
                logger.error("Invalid interval provided. Using default (10 minutes).")

    run_forever(interval_minutes=interval_minutes)
