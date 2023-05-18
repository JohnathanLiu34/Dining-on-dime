#pip install googlemaps
import googlemaps
#pip install prettyprint
import prettyprint
import json
import requests
from flask import Flask, render_template
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
    
def find_restaurants(api_key, location, radius = 1600):
    try:
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
        param = {
            "location" : location_to_coordinates(location),
            "radius" : radius,
            "type" : "restaurant",
            "key" : api_key,
        }
        print('\n')
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
        "fields" : "name,price_level",
        "key" : api_key
    }
    request_status = requests.get(endpoint_url,params=param)
    result = json.loads(request_status.content)

def budgeting_formula(cash):
    """
    cash = bank balance
    
    .3 = 50/30/20 rule
    .2 = spend no more than 20% of "wants" on eating out
    4 = eat out once per week (a reasonable number)
    """
    cash=int(cash)
    cash_available = .3*.2*cash/4
    if cash_available>50:
        return 4
    elif cash_available>25:
        return 3
    elif cash_available>10:
        return 2
    else:
        return 1
    
def parse_price_level(desired_level,restaurants):
    results = []
    for restaurant in restaurants['results']:
        if "price_level" in restaurant:
            if restaurant["price_level"] <= desired_level:
                try:
                    data = {'name': restaurant['name'],
                            'address':restaurant['vicinity'],
                            'rating':restaurant['rating'],
                            }
                    results.append(data)
                except KeyError:
                    print('exception')
                
    return results

def complete_restaurant_finder(location,cash,distance):
    loc = location_to_coordinates(location)
    budget = budgeting_formula(cash)
    restaurants = find_restaurants(API_Key,loc, radius=distance)
    finished_restaurants = parse_price_level(budget,restaurants)
    return finished_restaurants

def main():
    print("Hello World")
    #print(get_user_location("Elmhurst NY"))
    print(complete_restaurant_finder("Back Bay, Boston, MA",1000,1600))
    #print(complete_restaurant_finder("Montrose, Houston, TX",2000,1600))
    #print(complete_restaurant_finder("Oro Valley, AZ",3000,1600))

if __name__ == "__main__":
    main()