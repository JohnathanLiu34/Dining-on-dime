#pip install googlemaps
import googlemaps
#pip install prettyprint
import prettyprint
import json
import requests
from flask import Flask, render_template
import time
import sys

#Please do not share this, I am broke
API_Key = "AIzaSyAAsPXGsYgX8aF5O4HdP21AY-kbjMTJYsw"
google_client  = googlemaps.Client(API_Key)

def get_user_location(name):
    print("working")
    try:
        response = google_client.places(query = name)
        print("working2")
        results = response.get('results')
        return results
    except Exception as e:
        print("failed")
        print(e)
        return


def find_restaurants(api_key, location, radius = 1600):
    try:
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        param = {
            "location" : location,
            "radius" : radius,
            "type" : "restaurant",
            "key" : api_key,
        }
        request_status = requests.get(endpoint_url, params = param)
        result = json.loads(request_status.content)
        print("working3")
        return result
    except Exception as e:
        print(e)
        return


def get_place_details(api_key, place_id):
    endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
    param = {
        "place_id" : place_id,
        "fields" : "name,price_leve",
        "key" : api_key
    }
    request_status = requests.get(endpoint_url,params = param)
    result = json.loads(request_status.content)


def parse_price_level(desired_level):
    list = []
    restaurants = find_restaurants(API_Key,"40.74291,-73.87998")
    restaurants = restaurants["results"]
    for restaurant in restaurants:
        if "price_level" in restaurant:
            if restaurant["price_level"] == desired_level:
                list.append(restaurant)

    return list

def location_to_coordinates(location):
    try:
        endpoint_url = "https://maps.googleapis.com/maps/api/geocode/json?"
        param = {
            "address" : location,
            "key" : API_Key,
        }
        request_status = requests.get(endpoint_url, params = param)
        result = json.loads(request_status.content)['results'][0]['geometry']['location']
        coords = str(result['lat'])+', '+str(result['lng'])
        return coords

    except Exception as e:
        print(e)
        return


def main():
    print("Hello World")
    #print(get_user_location("Elmhurst NY"))
    #print(find_restaurants(API_Key,"40.74291,-73.87998"))
    #r = find_restaurants(API_Key,"40.74291,-73.87998")
    print(parse_price_level(1))
    
if __name__ == "__main__":
    main()
