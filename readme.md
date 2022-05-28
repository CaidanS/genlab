# Generation Lab Take Home

## Scrape K State Student Database

This script does its best to collect and clean name/email pairs from the search.k-state.edu database. It makes no claims as too coverage of all students completeness. Example output can be found in data.csv

## Installation

You will need to install and configure the correct version of chromedriver for your system/version of chrome from here https://chromedriver.chromium.org/downloads

```
git clone https://github.com/CaidanS/genlab.git
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Use

```
python3 scrape.py
```