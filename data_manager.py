import requests
from pprint import pprint
sheet_endpoint = "https://api.sheety.co/12a24ef1febf21c644cea63d93ed9e95/flightDeals/prices/"

class DataManager:

    def __init__(self):
        self.destination_data = {}

    def get_data(self):

        response = requests.get(url=sheet_endpoint)
        data = response.json()
        print(data)
        self.destination_data = data["prices"]

        # 3. Try importing pretty print and printing the data out again using pprint().
        # pprint(data)
        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{sheet_endpoint}/{city['id']}",
                json=new_data
            )
            print(response.text)