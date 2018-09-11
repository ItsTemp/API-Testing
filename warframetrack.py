import json
import requests
import os
import data

# Sends api request
def WarframeAPIRequest():
    url = ("https://ws.warframestat.us/pc")
    r = requests.get(url)
    apidata = r.json()

    #Directory of the locally saved worldstate json
    basedir = os.path.abspath(os.path.dirname(__file__))
    data_json = basedir+'\world.json'

    #Open and replace the current worldstate with the newly aquired json
    with open(data_json, 'w') as outfile:  
            json.dump(apidata, outfile)
    
    #After data has been replaced open the worldstate json
    with open(data_json, encoding="utf8") as f:
        cacheddata = json.load(f)

    #Return the content of the json for parsing
    return cacheddata

#Save content of json into a variable, too lazy atm to add checks to function so this will save time and api calls
WorldStateData = WarframeAPIRequest()

# Retrieves the sorties information
def RetrieveSorties():
    #Gets the data from the WorldStateData variable created above and filters out the sortie part which we need.
    Sorties = WorldStateData["sortie"]
    return Sorties

# Retrieves alert information
def RetrieveAlerts():
    Alerts = WorldStateData["alerts"]
    return Alerts

# Retrieves alert information
def RetrieveFissures():
    fissures = WorldStateData["fissures"]
    return fissures

# Retrieves the certus time cycle
def RetrieveCetusCycle():
    TimeCycle = WorldStateData["cetusCycle"]
    return TimeCycle

# Retrieves the certus time cycle
def RetrieveEarthCycle():
    TimeCycle = []
    TimeCycle.append(WorldStateData["earthCycle"]["timeLeft"])
    TimeCycle.append(WorldStateData["earthCycle"]["isDay"])

    return TimeCycle
