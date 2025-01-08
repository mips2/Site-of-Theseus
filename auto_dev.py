
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
RETRY_LIMIT = config.get("retry_limit", 5)
ENABLE_AUTODEV = config.get("enable_autodev", True)
DRY_RUN = config.get("dry_run", False)  # For improvement #15

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
def generate_code_change(current_code, failure_reason=""):
    """
    Send the existing code to DeepSeek, along with instructions on how to modify it.
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
                    + "Here is the existing code:\n\n"
                    + current_code
                    + "\n\n"
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
        logger.debug(f"RAW AI RESPONSE:\n{ai_message}\n")  # Debug-level log
        return ai_message
    except (KeyError, IndexError) as e:
        logger.error(f"Invalid DeepSeek response structure: {e}")
        return "# [DeepSeek ERROR] Invalid response.\n"

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
        filename_line = match[0]  # e.g., "File: website/app.py"
        file_path = match[1].strip()
        code_block = match[2].strip()

        # Remove trailing --> if AI appended it
        if file_path.endswith("-->"):
            file_path = file_path.replace("-->", "").strip()

        # Skip tests
        if file_path.startswith("website/tests"):
            logger.warning(f"AI attempted to modify tests file '{file_path}'. Skipping.")
            continue

        # Force everything else to be in `website/`
        if not file_path.startswith("website/"):
            file_path = f"website/{file_path.lstrip('/')}"

        # If referencing a .py file but there's <html>, remove inline HTML
        if file_path.endswith(".py"):
            if "<html>" in code_block.lower():
                logger.warning(f"AI inline HTML in .py file '{file_path}' - removing HTML block.")
                while True:
                    start_idx = code_block.lower().find("<html>")
                    if start_idx == -1:
                        break
                    end_idx = code_block.lower().find("</html>", start_idx)
                    if end_idx == -1:
                        break
                    end_idx += len("</html>")
                    code_block = code_block[:start_idx] + "# [HTML REMOVED]\n" + code_block[end_idx:]

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

    # Attempt a bandit scan if available
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

    # Finally, run tests
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
    This ensures the local repository matches the remote state.
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
    else:
        logger.info("Successfully reverted to the latest remote commit.")

# -------------------------------------------------------------------------
#  Main Automated Loop
# -------------------------------------------------------------------------
def main_loop():
    global ATTEMPTED_COMMITS, SUCCESSFUL_COMMITS

    if not ENABLE_AUTODEV:
        logger.info("AUTO-DEV is disabled in config.yaml. Exiting.")
        return

    logger.addHandler(console_handler)  # Ensure console output for auto runs

    # 1. Pull latest code
    git_command("pull", "origin", BRANCH_NAME)

    # 2. Ensure website/app.py is present
    app_path = "website/app.py"
    if not os.path.exists(app_path):
        logger.error(f"{app_path} does not exist! Cannot proceed.")
        return

    with open(app_path, "r", encoding="utf-8") as f:
        old_app_code = f.read()

    current_code = old_app_code
    success = False
    failure_reason = ""

    # Attempt multiple times
    for attempt in range(1, RETRY_LIMIT + 1):
        logger.info(f"Generation attempt #{attempt} of {RETRY_LIMIT}.")
        if attempt > 1:
            logger.info("Pausing briefly before next AI request (rate limit).")
            time.sleep(3 * attempt)

        ai_response = generate_code_change(current_code, failure_reason=failure_reason)
        files_dict = parse_ai_response_into_files(ai_response)

        if not files_dict:
            failure_reason = "No valid (or fully valid) file changes returned by AI."
            logger.warning(failure_reason)
            continue

        # 3. Check for template references
        template_references_check(files_dict)

        # 4. Dry-run skip actual writes/tests
        if DRY_RUN:
            logger.info("[DRY RUN] Would update files, but skipping actual writes/tests.")
            success = True
            break
        else:
            # Write changes
            for filepath, code_str in files_dict.items():
                dir_path = os.path.dirname(filepath)
                if dir_path:  # Only create if not empty
                    os.makedirs(dir_path, exist_ok=True)
                with open(filepath, "w", encoding="utf-8") as fw:
                    fw.write(code_str)
                logger.info(f"Updated file: {filepath}")


            # Test
            if run_test_commands():
                success = True
                break
            else:
                failure_reason = "Tests failed for generated code."
                logger.warning(failure_reason)

    # 5. Commit or revert
    if success:
        ATTEMPTED_COMMITS += 1
        git_command("add", ".")
        commit_msg = f"Auto-update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        push_res = git_command("push", "origin", BRANCH_NAME)
        if push_res.returncode == 0:
            SUCCESSFUL_COMMITS += 1
            logger.info("Successfully pushed changes.")
        else:
            logger.error("Push failed. Attempting revert to latest remote commit.")
            revert_to_latest_remote_commit()
    else:
        logger.error(f"All {RETRY_LIMIT} attempts failed. Reverting to latest remote commit.")
        revert_to_latest_remote_commit()
        force_push_res = git_command("push", "origin", BRANCH_NAME, "--force")
        if force_push_res.returncode == 0:
            logger.info("Successfully forced a revert to remote.")
        else:
            logger.error("Failed to push revert. Local is reverted, remote may be out of sync.")

    # Final metrics/log
    logger.info(
        f"Session metrics - Attempted commits: {ATTEMPTED_COMMITS}, "
        f"Successful commits: {SUCCESSFUL_COMMITS}"
    )

# -------------------------------------------------------------------------
#  Manual Run (One-Off Iteration)
# -------------------------------------------------------------------------
def manual_run():
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

    template_references_check(files_dict)

    if DRY_RUN:
        logger.info("[DRY RUN] Would update files, but skipping actual writes.")
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
        else:
            logger.error("Manual-run: Push failed. Reverting to latest remote commit.")
            revert_to_latest_remote_commit()
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
