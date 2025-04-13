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
python3 -m src.gui.main
```

## Bundle with pyinstaller

Run
```bash
pyinstaller pdf2img.spec
```
