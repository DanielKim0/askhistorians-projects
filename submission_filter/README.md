# README

Submission Filter is a script that fetches all posts from a given subreddit and time period that do not have non-distinguished first-level comments, exports their info, and then deletes them, with GUI support.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install this script's requirements.
```bash
pip install -r requirements.txt
```

Then, run main.py using python.
```bash
python main.py
```

Note that you must place a .env file in this directory with the proper CLIENTID and CLIENTSECRET variables before using this script.

Alternatively, if you're using Windows, you can use the executable function located in the releases section.
