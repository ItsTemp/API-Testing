import json
import requests
import os
import data

#0 = Cetus, 1=Alert, 2=fissure, 3=sortie
Endpoints = ["https://api.warframestat.us/pc/cetusCycle", #0
             "https://api.warframestat.us/pc/alerts", #1 
             "https://api.warframestat.us/pc/fissures", #2
             "https://api.warframestat.us/pc/sortie"] #3

#Sends api request
def WarframeAPIRequest(endpoint):
    url = (endpoint)
    header = {'content-type': 'application/x-www-form-urlencoded'}
    apibody = {'language': 'en'}
    r = requests.get(url, headers=header, data=apibody)
    apidata = r.json()
    return apidata

#Retrieves the sorties information
def RetrieveSorties():
    Sorties = WarframeAPIRequest(Endpoints[3])
    return Sorties

#Retrieves alert information
def RetrieveAlerts():
    Alerts = WarframeAPIRequest(Endpoints[1])
    return Alerts


#Gets the daily deals from worldstate json
def GetDailyDeals():
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_json = basedir+'\world.json'

    with open(data_json, encoding="utf8") as f:
        data = json.load(f)

    DailyDeals = data["DailyDeals"]

    return DailyDeals




