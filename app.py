from flask import Flask, render_template, request
import requests
from warframetrack import RetrieveAlerts, RetrieveSorties
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler
import os
import json

app = Flask(__name__)


def check_for_update():
    # Send api request
    # Open cached json
    # Compare api json to stored json
    # If api is newer than stored json, replace stored with api json
    # Else do nothing

    # Sending API Request
    try:
        url = ("https://fortnite-public-api.theapinetwork.com/prod09/store/get")
        header = {'Authorization': '',
                  'content-type': 'application/x-www-form-urlencoded'}
        apibody = {'language': 'en'}
        r = requests.post(url, headers=header, data=apibody)
        apidata = r.json()
    except:
        print("no worky")
        return

    # Open current config.json
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_json = basedir+'\cachedstore.json'
    with open(data_json, encoding="utf8") as f:
        cacheddata = json.load(f)

    # If the date on both jsons are the same
    if apidata["date"] == cacheddata["date"]:
        # Print versions are the same and do nothing
        print("Versions are the same")
        return cacheddata
    else:  # Otherwise the store has been updated
        print("Store Updated")  # Print store updated
        with open(data_json, 'w') as outfile:  # Open the cached json and write in new data
            json.dump(apidata, outfile, sort_keys=True,
                      indent=4, ensure_ascii=False)
            return apidata


shop = check_for_update()

scheduler = BackgroundScheduler()
scheduler.add_job(func=check_for_update, trigger="interval", minutes=20)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

# Homepage


@app.route('/')
def home():
    return render_template('index.html')

# Fortnite Store


@app.route('/store')
def store():
    return render_template('store.html', stuff=shop)

# Warframe Tracker


@app.route('/wftrack')
def wftrack():
    return render_template('wftrack.html', sorties=RetrieveSorties(), alerts=RetrieveAlerts(), sortiecount=1)


if __name__ == '__main__':
    app.run(debug=True)
