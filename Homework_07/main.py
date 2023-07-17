"""
Napisz program, który sprawdzi, czy danego dnia będzie padać. Użyj do tego poniższego API. Aplikacja ma działać następująco:

    Program pyta dla jakiej daty należy sprawdzić pogodę. Data musi byc w formacie YYYY-mm-dd, np. 2022-11-03. W przypadku nie podania daty, aplikacja przyjmie za poszukiwaną datę następny dzień.
    Aplikacja wykona zapytanie do API w celu poszukiwania stanu pogody.
    Istnieją trzy możliwe informacje dla opadów deszczu:
        Będzie padać (dla wyniku większego niż 0.0)
        Nie będzie padać (dla wyniku równego 0.0)
        Nie wiem (gdy wyniku z jakiegoś powodu nie ma lub wartość jest ujemna)

Będzie padać
Nie będzie padać
Nie wiem

    Wyniki zapytań powinny być zapisywane do pliku. Jeżeli szukana data znajduje sie juz w pliku, nie wykonuj zapytania do API, tylko zwróć wynik z pliku.


URL do API:
https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=rain&daily=rain_sum&timezone=Europe%2FLondon&start_date={searched_date}&end_date={searched_date}

W URL należy uzupełnić parametry: latitude, longitude oraz searched_date
"""

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
        self.file_data = self.read_data_from_file()
        self.raining_data = None

    def get_input_data(self):
        city = input("Podaj miasto, dla którego chcesz sprawdzić pogodę: ")
        date = input("Podaj datę, dla której chcesz sprawdzić pogodę w formacie YYYY-mm-dd: ")
        pattern = r'^\d{4}-\d{2}-\d{2}$'
        if date == '':
            date = datetime.date.today() + datetime.timedelta(days=1)
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
            reason = data.get("reason").replace('"', '-')
            return f'Błąd: {reason}'
        raining_sum = data.get("daily").get("rain_sum")[0]
        if raining_sum > 0.0:
            return "będzie padać."
        elif raining_sum == 0.0:
            return "nie będzie padać."
        else:
            return "nie wiem, czy będzie padać."

    def retrieve_data(self):
        city_data = self.file_data.get(self.city)
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
            new_data = self.transform_data_in_file(self.raining_data)
            file.write(new_data)

    def transform_data_in_file(self, raining_info):
        if self.file_data.get(self.city):
            self.file_data[self.city][self.date] = raining_info
        else:
            self.file_data[self.city] = {}
            self.file_data[self.city][self.date] = raining_info
        return json.dumps(self.file_data).replace("'", '"')

data = WeatherAPI()
write_new_data_to_file = data.retrieve_data()
if write_new_data_to_file:
    data.write_data_to_file()
    print(f'W dniu {data.date} w mieście {data.city} {data.raining_data}')
else:
    print(f'W dniu {data.date} w mieście {data.city} {data.file_data.get(data.city).get(data.date)}')