import datetime
import json
import re
import requests
from geopy.geocoders import Nominatim

API_URL = "https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}" \
          "&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}"


class WeatherAPI:

    def __init__(self):
        self.date, self.city = self.get_input_data()
        self.longitude, self.latitude = self.find_coordinates_for_city()
        self.forecast_data = self.read_data_from_file()
        self.raining_data = None

    def get_input_data(self):
        city = input("Podaj miasto, dla którego chcesz sprawdzić pogodę: ")
        while city == "":
            city = input("Nie podano nazwy miasta. Podaj miasto, dla którego chcesz sprawdzić pogodę: ")
        date = input("Podaj datę, dla której chcesz sprawdzić pogodę w formacie YYYY-mm-dd: ")
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if date == '':
            date = str(datetime.date.today() + datetime.timedelta(days=1))
            print(f'Nie podano daty. Przyjmuję dzień jutrzejszy, czyli: {date}')
        else:
            while not re.match(pattern, date):
                print('Niepoprawny format daty.')
                date = input('Podaj datę w formacie YYY-mm-dd: ')
        return date, city

    def find_coordinates_for_city(self):
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(self.city)
        return location.latitude, location.longitude

    def read_data_from_file(self):
        with open("rain_vol.txt", mode="r+") as file:
            data_in_file = file.read()
        return json.loads(data_in_file) if data_in_file else {}

    def retrieve_data_from_api(self):
        response = requests.get(API_URL.format(latitude=self.latitude,
                                               longitude=self.longitude,
                                               searched_date=self.date))
        data = json.loads(response.text)
        return data

    def check_raining_sum(self, data: dict):
        if data.get("error"):
            reason = data.get("reason").replace("'", '-')
            return f'Błąd: {reason}'
        raining_sum = data.get("daily").get("rain_sum")[0]
        if raining_sum > 0.0:
            return "będzie padać."
        elif raining_sum == 0.0:
            return "nie będzie padać."
        else:
            return "nie wiem, czy będzie padać."

    def retrieve_data(self):
        city_data = self.forecast_data.get(self.city)
        if city_data:
            if city_data.get(self.date):
                new_data = False
                return new_data
        data = self.retrieve_data_from_api()
        self.raining_data = self.check_raining_sum(data)
        new_data = True
        return new_data

    def write_data_to_file(self):
        with open("rain_vol.txt", mode="w") as file:
            new_data = self.__setitem__(self.raining_data)
            file.write(new_data)

    def __setitem__(self, raining_info):
        if self.forecast_data.get(self.city):
            self.forecast_data[self.city][self.date] = raining_info
        else:
            self.forecast_data[self.city] = {}
            self.forecast_data[self.city][self.date] = raining_info
        return json.dumps(self.forecast_data).replace("'", '"')

    def items(self):
        for city in self.forecast_data.keys():
            for date in self.forecast_data.get(city).keys():
                yield date, city

    def __iter__(self):
        return iter(self.forecast_data)

    def __getitem__(self, item):
        city, date = item
        try:
            city_data = self.forecast_data[city][date]
            return f"{date}: {city} - {city_data}"
        except KeyError:
            return f"No weather data stored for {date} {city}"
        #return self.forecast_data[city][date]

