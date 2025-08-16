Job Finder Bot – Full Setup Guide

This project automates job searching by scraping job portals, saving results in a CSV file, and emailing them daily using cron jobs.

It includes:

Job scraping
CSV export
Gmail email alerts
Cron automation
Full GitHub-ready project structure


1. Prerequisites

Make sure you have installed:
Python 3.8+
pip (Python package manager)
git
nano/vim (for editing files)
Check versions:

python3 --version
pip3 --version
git --version



2. Clone or Create Project
mkdir job-finder-bot
cd job-finder-bot


3. Project Structure
job-finder-bot/
│── job_finder.py         # Main Python script
│── run_job_finder.sh     # Shell script to execute bot
│── requirements.txt      # Dependencies
│── .jobbot.env           # Environment variables (secrets)
│── README.md             # Documentation
│── .gitignore            # Ignore sensitive files
│── jobbot_output/        # Output folder (CSV + logs)


4.Setup Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
Install dependencies:

```
pip install requests beautifulsoup4 pandas python-dotenv
```

Save them:

```
pip freeze > requirements.txt
```

5. Gmail App Password Setup

Since Google blocks normal passwords, you must use App Passwords:

Enable 2-Step Verification in your Gmail.

Go to Google App Passwords (https://myaccount.google.com/apppasswords).

Create a password for "Mail → Other".

Copy the 16-character password

6. Create .jobbot.env
EMAIL_FROM=yourgmail@gmail.com
EMAIL_TO=yourgmail@gmail.com
APP_PW=abcd efgh ijkl mnop

7. Main Python Script – job_finder.py

This script will:

Scrape job portals

Save results in jobbot_output/jobs_YYYYMMDD_HHMMSS.csv

Send results via email


8. Shell Script – run_job_finder.sh
```
#!/bin/bash
cd /home/<your-username>/job-finder-bot
source venv/bin/activate
python job_finder.py
````

Make it executable:
```
chmod +x run_job_finder.sh
```
9. Automation with Cron
----------
Edit cron jobs:

crontab -e
Run every day at 9 AM:

```
0 9 * * * /home/<your-username>/job-finder-bot/run_job_finder.sh >> /home/<your-username>/job-finder-bot/jobbot_output/cron.log 2>&1

```
Check active jobs:

```
crontab -l
```
Check logs in real-time:

```
tail -f /home/<your-username>/job-finder-bot/jobbot_output/cron.log
```
Testing
-------

Run manually once:
```
./run_job_finder.sh
```
