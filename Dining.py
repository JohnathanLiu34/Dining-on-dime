#pip install googlemaps
import googlemaps
#pip install prettyprint
import prettyprint
import json
import requests
import time
import sys

#Please do not share this, I am broke
API_Key = "AIzaSyAAsPXGsYgX8aF5O4HdP21AY-kbjMTJYsw"
google_client  = googlemaps.Client(API_Key)

def get_user_location(name):
    try:
        response = google_client.places(query = name)
        print("getting user location")
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
        print("finding nearby restaurants")
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
    return result


def parse_price_level(desired_level,restaurants):
    results = []
    print("parsing based on price")
    for restaurant in restaurants['results']:
        if "price_level" in restaurant:
            if restaurant["price_level"] <= desired_level:
                data = {'name': restaurant['name'],
                        'address':restaurant['vicinity'],
                        'rating':restaurant['rating'],
                        }
                results.append(data)
                
    return results

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
        print("error caught")
        return


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


def complete_restaurant_finder(location,cash,distance):
    loc = location_to_coordinates(location)
    budget = budgeting_formula(cash)
    restaurants = find_restaurants(API_Key,loc, radius=distance)
    finished_restaurants = parse_price_level(budget,restaurants)
    return finished_restaurants


def main():
    print(complete_restaurant_finder("Elmhurst, NY", 20, 1600))
    
    
if __name__ == "__main__":
    main()
  
