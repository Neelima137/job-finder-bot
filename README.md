**Job Finder Bot**
--------------------
This project automates job search using Google Custom Search API, stores results in CSV, and emails them daily using Gmail. Deployed on Google Cloud Compute Engine (VM) with cron.

Features

Fetches job listings using Google Programmable Search Engine (CSE)

Saves results into CSV with timestamp

Emails results daily using Gmail SMTP + App Password

Runs automatically via cron job on GCP VM

Setup Guide
-------------------
1. Create a Compute Engine VM (GCP)

Go to Google Cloud Console (https://console.cloud.google.com/)

Navigate to Compute Engine → VM instances

Create a VM (Ubuntu recommended)

Machine type: e2-medium (2 vCPU, 4 GB RAM)

Allow HTTP/HTTPS traffic

Connect via SSH

Update system:

sudo apt update && sudo apt upgrade -y


Install dependencies:

sudo apt install git python3 python3-pip -y

2. Clone Repo & Setup Project
git clone https://github.com/yourusername/job-finder-bot.git
cd job-finder-bot
mkdir -p jobbot_output


Install Python packages:

pip3 install -r requirements.txt

3. Enable Gmail App Password

Go to Google Account → Security (https://myaccount.google.com/security)

Enable 2-Step Verification

Go to App passwords

Create a new app password (16 characters, e.g., abdv cwgq brzs ohiz)

4. Enable Google Custom Search API

Go to Google Cloud API Library (https://console.cloud.google.com/apis/library)

Enable Custom Search API

Go to Credentials → Create API Key

5. Create Programmable Search Engine (CSE) 

Go to Programmable Search (https://programmablesearchengine.google.com/)

Click Add → Add job sites (e.g. *.linkedin.com, *.naukri.com, *.indeed.com)

Get your CSE ID

6. Configure Environment File

Create .jobbot.env:


7. Python Script (job_finder.py)

8. Run Script Manually
./run_job_finder.sh


 You should see:

Saved: /home//jobbot_output/jobs_20250816_150527.csv
Emailed: yes

9. Setup Cron Job

Open crontab:

crontab -e


Add job (runs daily at 9 AM):

````

0 9 * * * /home//run_job_finder.sh >> /home//jobbot_output/cron.log 2>&1
````

Check logs:

tail -f /home//jobbot_output/cron.log

 File Structure
job-finder-bot \
│── job_finder.py \
│── run_job_finder.sh \
│── .jobbot.env \
│── requirements.txt \
│── README.md \
└── jobbot_output \

Requirements

Python 3.x

Google Cloud VM (Ubuntu)

Gmail with App Password

Google Custom Search API + CSE


<img width="1024" height="1536" alt="image" src="https://github.com/user-attachments/assets/061e4c6e-4acd-4c5d-a9db-4f3f1e40b4b3" />






