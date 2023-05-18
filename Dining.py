#pip install googlemaps
import googlemaps
#pip install prettyprint
import prettyprint
import json
import requests
#from flask import Flask, render_template
import time

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
    endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
    params = {
        "location" : location,
        "radius" : radius,
        "type" : "restaurant",
        "key" : api_key,
    }
    result = json.loads(requests.get(endpoint_url,params=params).content)
    return result

def main():
    print("Hello World")
    print(get_user_location("Elmhurst NY"))



if __name__ == "__main__":
    main()