#!/usr/bin/python3

import requests
import json
import datetime
import os

def get_compare_date (tmp_date):
    month, day, year = tmp_date.split('/')
    return datetime.datetime(int(year),int(month),int(day))

def parse_json (my_json_data):
    homeUsage = None
    for i in my_json_data.keys():
        if type(my_json_data[i]) == list:
            for k in my_json_data[i]:
                startDate = k["startDate"]
                start = get_compare_date(startDate)
                endDate = k["endDate"]
                end = get_compare_date(endDate)
                usage = k['homeUsage']
                if (today >= start):
                    if today <= end:
                        homeUsage = usage
                        #print(start,end,usage, todayDate)
    return homeUsage

def parse_secrets (filename):
    username = ""
    password = ""
    f = open(filename,"r")
    for line in f:
        a,b = line.split(':')
        if a == "username":
            username = b.rstrip()
        elif a == "password":
            password = b.rstrip()

    # Close the file
    f.close()

    # Only return data if secrets is parsed correctly
    if (username == "") or (password == ""):
        print("No username or password found - please correct secrets file")
        return
    else:
        return username, password

# Determine today's date for later comparison
today = datetime.datetime.today()
todayDate = today.strftime('%m/%d/%Y')
detailedDate = today.strftime('%m/%d/%Y %H:%M:%S')

# URLs 
LOGIN_URL = "https://login.xfinity.com/login"
USAGE_URL = "https://customer.xfinity.com/apis/services/internet/usage"

# POST request data
username, password = parse_secrets("secrets.txt")
data = {"user": username,
        "passwd": password,
        "s": "oauth",
        "continue": "https://oauth.xfinity.com/oauth/authorize?client_id=my-account-web&prompt=login&redirect_uri=https%3A%2F%2Fcustomer.xfinity.com%2Foauth%2Fcallback&response_type=code"
        }
# Define a persistent session
s = requests.Session()

# POST request to login
r1 = s.post(url = LOGIN_URL, data = data)

# GET request to pull usage data
r2 = s.get(url = USAGE_URL)

# Parse Usage
my_usage = parse_json(json.loads(r2.text))

# Print usage is available otherwise end
if my_usage is None:
    pass
else:
    print(detailedDate, ",", my_usage)
