from re import L
import requests 
import json
import sys
import math
from math import pi, sin, cos

def getDirections(origin_lat, origin_lng, dest_place_ID,arv_time, mode, transit_option = ""):
    dest_place_ID = "place_id:"+ dest_place_ID
    api_key = "" #api_key's been removed 
    url = "https://maps.googleapis.com/maps/api/directions/json?destination=" + dest_place_ID + "&origin=" + origin_lat + "%2C" + origin_lng + "&arrival_time=" + arv_time + "&mode=" + mode
    
    #extra parameter in case of mode 
    if mode == "transit": 
        assert(transit_option) #check whether the parameter has been provided
        url += "&transit_mode=" + transit_option
    url += "&key=" + api_key

    response = requests.request("GET", url = url, headers = {}, data = {})
    response_dict = json.loads(response.content)

    route = response_dict["routes"][0]
    leg = route["legs"]
    return leg



if __name__ == '__main__':
    start_lat = sys.argv[1] #string of start location latitude
    start_lng = sys.argv[2] #string of start location longitude
    event_info = sys.argv[3:] #list of strings of event info(multiple of 3 in order of place_id arrival, mode)
    for i in range(0,len(event_info),3):
        dest_place_ID = event_info[i] #get destination place_id
        arv_time = event_info[i+1] #get arrival time in unix timestamp
        mode = event_info[i+2] #mode of transportaion
        if mode not in ["driving","walking","bicycling"]:
            transit_option = mode #bus,train, etc..
            mode = "transit"
            direction = getDirections(start_lat,start_lng,dest_place_ID,arv_time,mode,transit_option)
        else:
            direction = getDirections(start_lat,start_lng,dest_place_ID,arv_time,mode)
        


"""
piada :     place_id : ChIJw-xxVofxNIgRPoR9kR0qQaU
            time : 1644076800
            mode : walking
starbucks : place_id : ChIJV9x5pxXyNIgR5rO9GDHxInE
            time : 1644084000
            mode : bicycling
pnc :       place_id : ChIJjUYlvxHyNIgRtZCrPQsNyP4
            time : 1644087600
            mode : bus
"""


#python Directions.py 40.4432 -79.9428 ChIJw-xxVofxNIgRPoR9kR0qQaU 1644076800 walking ChIJV9x5pxXyNIgR5rO9GDHxInE 1644084000 bicycling ChIJjUYlvxHyNIgRtZCrPQsNyP4 1644087600 driving
