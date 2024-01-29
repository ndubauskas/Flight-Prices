import requests
from flight_data import FlightData

SEARCH_API_KEY = "API KEY"
TEQUILA_ENDPOINT = "https://tequila-api.kiwi.com"

class FlightSearch:

    def get_iata_code(self,city):
        location_endpoint = f"{TEQUILA_ENDPOINT}/locations/query"
        headers = {"apikey": SEARCH_API_KEY}
        query = {"term": city, "location_types": "city"}
        response = requests.get(url=location_endpoint,headers=headers,params=query)
        response.raise_for_status()
        data = response.json()["locations"]
        code = data[0]["code"]
        print(data[0]["code"])

        return code

    def search_flight(self,origin_city_code, destination_city_code, from_time, to_time):


        search_endpoint = f"{TEQUILA_ENDPOINT}/v2/search"
        headers = {"apikey": SEARCH_API_KEY}
        params = {
            "fly_from": origin_city_code,
            "fly_to": destination_city_code,
            "date_from": from_time.strftime("%d/%m/%Y"),
            "date_to": to_time.strftime("%d/%m/%Y"),
            "nights_in_dst_from": 7,
            "nights_in_dst_to": 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }
        response = requests.get(url=f"{search_endpoint}/v2/search",headers=headers,params=params)
        print(response.text)
        print(response.status_code)
        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f"No flights found for {destination_city_code}.")
            return None

        flight_data = FlightData(
            price=data["price"],
            origin_city=data["route"][0]["cityFrom"],
            origin_airport=data["route"][0]["flyFrom"],
            destination_city=data["route"][0]["cityTo"],
            destination_airport=data["route"][0]["flyTo"],
            out_date=data["route"][0]["local_departure"].split("T")[0],
            return_date=data["route"][1]["local_departure"].split("T")[0]
        )
        print(f"{flight_data.destination_city}: £{flight_data.price}")
        return flight_data