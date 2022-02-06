from re import L
import requests 
import json
import sys
import math
from math import pi, sin, cos

def rad(d):
    return d * pi / 180.0
    
def getDistance(start_lat, start_lng, lat1, lng1):
    # location of hbh, cmu
    lat2 = start_lat
    lng2 = start_lng
    EARTH_RADIUS = 6378.137
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)
    s = 2 * math.asin(
        math.sqrt(math.pow(sin(a / 2), 2) + cos(radLat1) * cos(radLat2) * math.pow(sin(b / 2), 2)))
    s = s * EARTH_RADIUS / 1.609344
    return s


"""
getCandidates(location, lat, lng)
parameters : 
    location :location keyword
    lat : current latitude
    lng : current longtitude
returns : 
    result : dictionary with key = place_id
                             value = list of additional info [name,address,location,distance]
"""
def getCandidates(lat, lng, location): 
    
    api_key = "" #api_key's been removed 
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + lat + "%2C" + lng + "&rankby=distance&keyword=" + location + "&key=" +api_key
    data = {}
    headers = {}

    #get request
    response = requests.request("GET", url, headers = headers, data= data)
    response_dict = json.loads(response.content)
    result_dict = dict()
    #if the request was succesful
    if response_dict["status"] == "OK":
        #get the results 
        candidates = response_dict["results"]

        #for each search result candidates
        for candidate in candidates: 

            #get relevant info
            location = (candidate["geometry"]["location"]['lat'],candidate["geometry"]["location"]['lng']) #lat/lng
            address = candidate["vicinity"] #address
            name = candidate["name"] #exact location name
            distance = getDistance(float(lat),float(lng),float(location[0]),float(location[1])) #distance from current location to diff places
            place_id = candidate["place_id"] #unique identifier

            #add to dictionary 
            result_dict[place_id] = [name,address,location,distance]
        return result_dict

    else:
        print("API Retrieval Failed.")
        return 0



if __name__ == '__main__':
    start_lat = sys.argv[1] #string of start location latitude
    start_lng = sys.argv[2] #string of start location longitude
    event_loc = sys.argv[3:] #list of strings of event location
    for i in range(len(event_loc)):
        candidate = getCandidates(start_lat,start_lng, event_loc[i])
