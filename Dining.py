#pip install googlemaps
import googlemaps
#pip install prettyprint
import prettyprint

import time

#Please do not share this, I am broke
API_Key = "AIzaSyDLR544uFKruW4TKtE3TnJfXnjTBaRjDyY"
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



def main():
    print("Hello World")
    print(get_user_location("Elmhurst NY"))

if __name__ == "__main__":
    main()
