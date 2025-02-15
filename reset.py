import os
import shutil
from datetime import datetime

# Define paths
website_dir = 'website'
templates_dir = os.path.join(website_dir, 'templates')
static_dir = os.path.join(website_dir, 'static')
archive_root_dir = 'archive'
app_file = os.path.join(website_dir, 'app.py')  # Define app_file here

# Debug: Print paths to verify they are correct
print(f"Website directory: {website_dir}")
print(f"Templates directory: {templates_dir}")
print(f"Static directory: {static_dir}")
print(f"App file: {app_file}")

# Create archive root directory if it doesn't exist
os.makedirs(archive_root_dir, exist_ok=True)

# Find the next available archive folder name
archive_index = 1
while True:
    archive_dir = os.path.join(archive_root_dir, f'archive_{archive_index}')
    if not os.path.exists(archive_dir):
        break
    archive_index += 1

# Create the archive directory
os.makedirs(archive_dir)
print(f"Created archive directory: {archive_dir}")

# Export templates and static to archive
if os.path.exists(templates_dir):
    print(f"Moving templates to {archive_dir}")
    shutil.move(templates_dir, os.path.join(archive_dir, 'templates'))
else:
    print(f"Templates directory not found: {templates_dir}")

if os.path.exists(static_dir):
    print(f"Moving static to {archive_dir}")
    shutil.move(static_dir, os.path.join(archive_dir, 'static'))
else:
    print(f"Static directory not found: {static_dir}")

if os.path.exists(app_file):
    print(f"Moving app.py to {archive_dir}")
    shutil.move(app_file, os.path.join(archive_dir, 'app.py'))
else:
    print(f"App file not found: {app_file}")

# Create new base Flask template
os.makedirs(templates_dir, exist_ok=True)
os.makedirs(static_dir, exist_ok=True)

# Create empty app.py
with open(os.path.join(website_dir, 'app.py'), 'w') as f:
    f.write("""from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
""")

# Create index.html
with open(os.path.join(templates_dir, 'index.html'), 'w') as f:
    f.write("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hello World</title>
</head>
<body>
    <h1>Hello World</h1>
</body>
</html>
""")

print(f"Export and replacement completed successfully. Files moved to {archive_dir}.")