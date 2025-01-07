#!/usr/bin/env python3
"""
auto_dev.py

A production-ready autonomous script that:
1. Pulls the latest code from GitHub.
2. Uses DeepSeek to generate new code features and HTML templates.
3. Tests changes.
4. Commits and pushes on success, or reverts on repeated failure.
   - On success, restarts 'gunicorn-theseus.service' and reloads Nginx.

Additionally:
- Allows custom system prompt (configured in config.yaml or directly below).
- Supports 'manual-run' mode for a one-off iteration.
- Implements robust error handling, logging, and security checks.
- Follows best practices to keep the repository consistent and maintainable.
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

# Rotating file handler (max ~1MB, keep 5 backups)
file_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=1_000_000, backupCount=5
)
file_format = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(message)s"
)
file_handler.setFormatter(file_format)
logger.addHandler(file_handler)

# We'll optionally add console logging if 'manual-run' is used
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

# This system prompt ensures DeepSeek knows it must produce compiling code.
SYSTEM_PROMPT = config.get(
    "system_prompt",
    "You are a helpful AI developer. Your goal is to add NEW and UNIQUE features to the existing Flask application. "
    "Each feature must:\n"
    "1. Build upon the existing codebase.\n"
    "2. Add interactivity (e.g., buttons, forms, links).\n"
    "3. Create navigable pages with a clear user flow.\n"
    "4. Avoid trivial or redundant routes (e.g., weather reports, placeholder data).\n"
    "5. Enhance the user experience and functionality of the website.\n\n"
    "Focus on features like:\n"
    "- A 'Contact Us' form with validation and submission feedback.\n"
    "- A navigation bar linking to all major pages.\n"
    "- A user profile page with editable fields.\n"
    "- A blog section with dynamic content loading.\n"
    "- A search bar with autocomplete functionality.\n\n"
    "Return ONLY the updated code. Do not include explanations or comments outside the code."
)

# Additional instructions (not displayed to end users).
USER_INSTRUCTIONS = config.get(
    "user_instructions",
    "Maintain a one-feature-at-a-time approach.\n"
    "Preserve existing functionality.\n"
    "Ensure any new routes or pages are navigable.\n"
    "Add interactive elements (e.g., buttons, forms, links).\n"
    "Avoid trivial or redundant routes (e.g., weather reports, placeholder data).\n"
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
    If missing or invalid, log errors or warnings.
    """
    if not DEESEEK_API_KEY or len(DEESEEK_API_KEY) < 10:
        logger.error("DEESEEK_API_KEY is missing or looks invalid. Exiting.")
        sys.exit(1)

    if not GITHUB_TOKEN:
        logger.warning("No GITHUB_TOKEN found in environment. Pushes may fail due to lack of credentials.")
    else:
        # Minimal check for length; real production code might do more thorough checks or use secrets management.
        if len(GITHUB_TOKEN) < 10:
            logger.warning("GITHUB_TOKEN looks unusually short; push might fail.")

validate_env_variables()

# -------------------------------------------------------------------------
#  DeepSeek Integration
# -------------------------------------------------------------------------
DEESEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
DEESEEK_MODEL = "deepseek-chat"
MAX_TOKENS = 2500  # Limit response length to prevent overly verbose output
DEESEEK_RETRIES = 3

def call_deepseek_api(payload):
    """
    Call the DeepSeek API with retry logic and exponential backoff.
    Returns the response text on success, or None on failure.
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
            logger.error(f"DeepSeek API call failed on attempt {attempt+1}: {e}")
            if attempt < DEESEEK_RETRIES - 1:
                backoff_time = 2 ** attempt
                logger.info(f"Retrying in {backoff_time} seconds...")
                time.sleep(backoff_time)
            else:
                logger.error("All attempts to call DeepSeek API have failed.")
                return None
    return None

def generate_code_change(current_code):
    """
    Send the existing code to DeepSeek, along with instructions on how to modify it.
    Return the updated code from the AI response.
    If DeepSeek fails, returns the original code plus an error comment.
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
                    "Return ONLY the updated code. Make sure it compiles and doesn't break existing tests. "
                    "Focus on adding meaningful features that contribute to building a full website. "
                    "Avoid adding trivial or silly routes like weather reports or placeholder data."
                ),
            },
        ],
        "temperature": 0,
        "max_tokens": MAX_TOKENS,
    }

    result = call_deepseek_api(payload)
    if not result:
        # Return the old code appended with error note if DeepSeek was unreachable
        return current_code + "\n# [DeepSeek ERROR] Could not generate new code.\n"

    try:
        ai_message = result["choices"][0]["message"]["content"].strip()
    except (KeyError, IndexError) as e:
        logger.error(f"Invalid response structure from DeepSeek: {e}")
        return current_code + "\n# [DeepSeek ERROR] Invalid response.\n"

    # Attempt to extract code from possible code fences
    if "```" in ai_message:
        splitted = ai_message.split("```")
        code_blocks = [chunk.strip() for chunk in splitted if chunk.strip()]
        # Pick the chunk with the most lines as the code block
        code_blocks_sorted = sorted(code_blocks, key=lambda x: len(x.splitlines()), reverse=True)
        code_part = code_blocks_sorted[0]
        # Remove language annotation if present
        code_part = code_part.replace("python", "").strip()
        return code_part
    else:
        return ai_message

# -------------------------------------------------------------------------
#  Template Handling (Ensuring referenced templates exist)
# -------------------------------------------------------------------------
def ensure_file_exists(file_path, default_content=""):
    """
    Ensure a file exists. If it doesn't, create it with default content.
    If nested directories are missing, create them.
    """
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_content)
        logger.info(f"Created file: {file_path}")

def extract_template_names_from_code(code_str):
    """
    Extract all template names used in render_template calls.
    Returns a set of template names.
    """
    template_names = set()
    for line in code_str.splitlines():
        if "render_template" in line:
            try:
                # Naively parse the string between render_template(...)
                snippet = line.split("render_template(")[1].split(")")[0]
                snippet_clean = snippet.strip().strip('"').strip("'")
                if snippet_clean:
                    template_names.add(snippet_clean)
            except (IndexError, ValueError):
                # If parsing fails, just skip
                pass
    return template_names

def extract_inline_html_to_template(new_code):
    """
    If the AI inserted large blocks of HTML directly into app.py (detected by <html> tag),
    we can extract and store them as a separate template file. This is a naive approach;
    advanced parsing may be needed for complex cases.
    Returns potentially modified code (with references to the new template file) and
    the name of the newly created template if any. Otherwise returns (new_code, None).
    """
    if "<html>" not in new_code.lower():
        # No obvious inline HTML block
        return new_code, None

    # We'll do a basic extraction from <html> to </html>
    start_index = new_code.lower().find("<html>")
    end_index = new_code.lower().find("</html>", start_index)
    if start_index == -1 or end_index == -1:
        return new_code, None

    end_index += len("</html>")
    html_block = new_code[start_index:end_index]

    # Create a simple new template name with timestamp
    template_name = f"inline_extracted_{int(time.time())}.html"
    template_path = os.path.join("website", "templates", template_name)
    os.makedirs(os.path.dirname(template_path), exist_ok=True)

    # Validate HTML (naively check for <body> tag, not strictly enforced)
    if "<body>" not in html_block.lower():
        logger.warning("Extracted HTML does not contain <body>. It may be incomplete.")

    # Write extracted HTML to the new template
    with open(template_path, "w", encoding="utf-8") as f:
        f.write(html_block)
    logger.info(f"Extracted inline HTML to template: {template_path}")

    # Now remove the block from new_code or comment it out, 
    # and add a line that references render_template(template_name).
    code_without_html = (
        new_code[:start_index] + 
        f"\n# The following HTML block was extracted to templates/{template_name}\n" +
        new_code[end_index:]
    )

    # If there's no existing route referencing this HTML, 
    # you could optionally insert a reference in the code. 
    # For now, we just remove it and rely on the developer to link it.
    return code_without_html, template_name

# -------------------------------------------------------------------------
#  Testing
# -------------------------------------------------------------------------
def check_tests_exist(test_path="website/tests/"):
    """
    Verify that a test directory exists and is not empty.
    Log a warning if it doesn't exist or is empty.
    """
    if not os.path.exists(test_path):
        logger.warning("Test directory does not exist. The test suite may be incomplete.")
        return
    if not os.listdir(test_path):
        logger.warning("Test directory exists but is empty. The test suite may be incomplete.")

def run_test_commands():
    """
    Install dependencies and run tests to ensure the new code is valid.
    Return True if tests pass, False otherwise.
    """
    req_file = "website/requirements.txt"
    if not os.path.exists(req_file):
        logger.warning("requirements.txt is missing or was not found. Dependencies may be incomplete.")

    # Ideally, use a virtual environment here; for simplicity, we'll just run pip.
    if os.path.exists(req_file):
        try:
            install_result = subprocess.run(
                ["pip", "install", "-r", req_file],
                check=True,
                capture_output=True,
                text=True
            )
            logger.info(install_result.stdout.strip())
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to install dependencies: {e.stderr}")
            return False

    # Check if tests exist before running
    check_tests_exist()

    # Run pytest
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
    """Helper to run git commands, logging output and errors."""
    cmd = ["git"] + list(args)
    logger.info(f"Running git command: {' '.join(cmd)}")

    env = os.environ.copy()
    # If you need to provide token-based auth, do so here
    # e.g., env["GIT_ASKPASS"] = "/path/to/custom/askpass" if needed

    result = subprocess.run(cmd, check=False, capture_output=True, text=True, env=env)
    if result.returncode != 0:
        logger.error(f"Git command error: {result.stderr.strip()}")
    else:
        logger.info(f"Git command success: {result.stdout.strip()}")
    return result

def revert_to_previous_commit():
    """
    Hard reset to the previous commit (HEAD~1).
    """
    logger.info("Reverting to the previous commit using git reset --hard HEAD~1.")
    git_command("reset", "--hard", "HEAD~1")

# -------------------------------------------------------------------------
#  Systemd Service Handling
# -------------------------------------------------------------------------
def check_service_exists(service_name):
    """
    Check if a systemd service is recognized on this system.
    Return True if the service is recognized, False otherwise.
    """
    try:
        result = subprocess.run(
            ["systemctl", "status", service_name],
            capture_output=True,
            text=True
        )
        # If 'Loaded: not-found' is in the output, the service doesn't exist
        if "Loaded: not-found" in result.stdout:
            return False
        return True
    except Exception as e:
        logger.error(f"Failed to check service {service_name}: {e}")
        return False

def restart_service(service_name):
    """
    Restart the given systemd service if it exists, then log status.
    """
    if not check_service_exists(service_name):
        logger.error(f"Service {service_name} not found or not installed.")
        return

    try:
        logger.info(f"Restarting {service_name}...")
        subprocess.run(["sudo", "systemctl", "restart", service_name], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to restart {service_name}: {e}")
        return

    # Check status post-restart
    try:
        result = subprocess.run(["systemctl", "is-active", service_name], capture_output=True, text=True)
        if result.stdout.strip() == "active":
            logger.info(f"{service_name} is running.")
        else:
            logger.warning(f"{service_name} is not active after restart.")
    except Exception as e:
        logger.error(f"Failed to verify status of {service_name}: {e}")

def reload_nginx():
    """
    Reload Nginx if it exists; log status.
    """
    if not check_service_exists("nginx"):
        logger.error("nginx service not found or not installed.")
        return

    try:
        logger.info("Reloading nginx...")
        subprocess.run(["sudo", "systemctl", "reload", "nginx"], check=True)
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to reload nginx: {e}")
        return

    # Check status post-reload
    try:
        result = subprocess.run(["systemctl", "is-active", "nginx"], capture_output=True, text=True)
        if result.stdout.strip() == "active":
            logger.info("nginx is running.")
        else:
            logger.warning("nginx is not active after reload.")
    except Exception as e:
        logger.error(f"Failed to verify status of nginx: {e}")

# -------------------------------------------------------------------------
#  Main Automated Loop
# -------------------------------------------------------------------------
def main_loop():
    """
    Automates the entire process:
    1. Pull the latest code.
    2. Generate new code and templates (retry up to RETRY_LIMIT times).
    3. Run tests.
    4. Commit/push if successful, otherwise revert to the previous commit.
       * On success, restarts 'gunicorn-theseus.service' and reloads Nginx.
    """
    if not ENABLE_AUTODEV:
        logger.info("AUTO-DEV is disabled in config.yaml. Exiting gracefully.")
        return

    # Pull latest code
    git_command("pull", "origin", BRANCH_NAME)

    target_file = "website/app.py"
    if not os.path.exists(target_file):
        logger.error(f"{target_file} does not exist! Cannot proceed.")
        return

    # Read original code
    with open(target_file, "r", encoding="utf-8") as f:
        old_code = f.read()

    new_code = old_code
    success = False

    for attempt in range(1, RETRY_LIMIT + 1):
        logger.info(f"Attempt #{attempt} to generate feature and test.")

        # Generate code from DeepSeek
        new_code = generate_code_change(new_code)

        # Check if AI inserted large HTML directly into app.py
        new_code, extracted_template = extract_inline_html_to_template(new_code)

        # Write changes to file
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(new_code)

        # Ensure templates exist if referenced in the code
        template_names = extract_template_names_from_code(new_code)
        for template_name in template_names:
            template_path = os.path.join("website", "templates", template_name)
            ensure_file_exists(
                template_path,
                f"<h1>Welcome!</h1>\n<p>This is the {template_name} page, auto-created.</p>"
            )

        # Run tests
        if run_test_commands():
            success = True
            break
        else:
            logger.warning(f"Test failed on attempt #{attempt}. Retrying...")

    if success:
        # Commit and push
        git_command("add", ".")
        commit_msg = f"Auto-update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        git_push_result = git_command("push", "origin", BRANCH_NAME)

        if git_push_result.returncode == 0:
            logger.info("Successfully committed and pushed changes.")


            # Reload Nginx (optional, ensures Nginx recognizes new config)
            reload_nginx()
        else:
            logger.error("Failed to push changes to remote repository. Attempting to revert local changes...")
            revert_to_previous_commit()
    else:
        # All attempts failed, revert
        logger.error(f"All {RETRY_LIMIT} attempts failed. Reverting to previous commit.")
        revert_to_previous_commit()

        # Force push the revert if needed
        revert_push_result = git_command("push", "origin", BRANCH_NAME, "--force")
        if revert_push_result.returncode == 0:
            logger.info("Successfully reverted to the previous working version.")
        else:
            logger.error("Failed to push the revert. Local repo is reverted, but remote may be out of sync.")

# -------------------------------------------------------------------------
#  Manual Run (One-Off Iteration)
# -------------------------------------------------------------------------
def manual_run():
    """
    Perform a single iteration of:
    1. Pull the latest code.
    2. Generate code once.
    3. Test it.
    4. If success, commit/push. If fail, revert local changes.
       * On success, also restarts Gunicorn and reloads Nginx.
    Provides console output for real-time feedback.
    """
    # Attach console handler for real-time feedback
    logger.addHandler(console_handler)

    logger.info("Starting MANUAL RUN of the AI code update process.")
    git_command("pull", "origin", BRANCH_NAME)

    target_file = "website/app.py"
    if not os.path.exists(target_file):
        logger.error(f"{target_file} does not exist! Cannot proceed.")
        return

    # Backup old code
    with open(target_file, "r", encoding="utf-8") as f:
        old_code = f.read()

    # Generate code once
    new_code = generate_code_change(old_code)

    # Check and extract any inline HTML
    new_code, extracted_template = extract_inline_html_to_template(new_code)

    with open(target_file, "w", encoding="utf-8") as f:
        f.write(new_code)

    # Ensure templates exist if referenced in the code
    template_names = extract_template_names_from_code(new_code)
    for template_name in template_names:
        template_path = os.path.join("website", "templates", template_name)
        ensure_file_exists(
            template_path,
            f"<h1>Welcome!</h1>\n<p>This is the {template_name} page, auto-created.</p>"
        )

    # Run tests
    if run_test_commands():
        logger.info("Manual run: Tests passed on first try.")
        git_command("add", ".")
        commit_msg = f"Manual-run update from AI on {datetime.now().isoformat()}"
        git_command("commit", "-m", commit_msg)
        git_push_result = git_command("push", "origin", BRANCH_NAME)

        if git_push_result.returncode == 0:
            logger.info("Manual-run: Successfully committed and pushed changes.")
            restart_service("gunicorn-theseus.service")
            reload_nginx()
        else:
            logger.error("Manual-run: Failed to push changes. Attempting to revert local changes...")
            revert_to_previous_commit()
    else:
        logger.error("Manual run: Tests failed. Reverting to old code locally.")
        with open(target_file, "w", encoding="utf-8") as f:
            f.write(old_code)

        git_command("add", ".")
        git_command("commit", "-m", "Manual-run revert to previous working version")
        revert_push_result = git_command("push", "origin", BRANCH_NAME, "--force")
        if revert_push_result.returncode == 0:
            logger.info("Manual-run: Successfully forced a revert to the previous version.")
        else:
            logger.error("Manual-run: Failed to push the revert. Local repo is reverted, but remote may be out of sync.")

# -------------------------------------------------------------------------
#  Entry Point
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # If you run "python auto_dev.py manual-run", we'll do a one-off iteration.
    # Otherwise, run the full main_loop.
    if len(sys.argv) > 1 and sys.argv[1] == "manual-run":
        manual_run()
    else:
        main_loop()
