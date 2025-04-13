# CRM Automation App

## Installation

Create a virtual environment:
```bash
python3 -m venv scraper-env
```

Activate the environment:
```bash
source scraper-env/bin/activate 
```

Install dependencies:
```bash
pip3 install -r requirements.txt
```

## Usage

Run the script for scraping:
```bash
python3 -m src.main
```

Run the script for updating notes:
```bash
python3 -m src.update_notes
```

Run the script for updating stages:
```bash
python3 -m src.update_stages
```

## Email Sending Configuration

### Using the Gmail API

Uses OAuth 2.0 for secure authentication (no storing passwords or app passwords)

Lets you:

* Send emails with HTML formatting
* Attach files
* Read from inbox
* Organize messages (labels, threads)
* Recommended if you’ll be doing more than just basic emailing

### Step-by-Step Setup (First Time Only)

1. Create or use a Google Cloud Project
* Go to Google Cloud Console
* Create a new project (or select an existing one)

2. Enable the Gmail API
* Go to Gmail API
* Click Enable

3. Set Up OAuth 2.0 Credentials
* In the sidebar, go to APIs & Services > Credentials
* Click + Create Credentials > OAuth client ID
* Choose: Application type: Desktop app
* Download the credentials.json file

4. Move credentials to this project
* In `secrets/` store downloaded `credentials.json` as `google_credentials.json`

---

## TODO

- [ ] Automate clearing sort and always select "Opportunity Name"
- [ ] Use threads in GUI to keep it responsive
- [ ] Add ability to change lead stage from one to another via GUI
- [ ] Fix modal closing issue — use "Close" button instead of the "X"
