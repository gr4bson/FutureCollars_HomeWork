"""
optymalizuj kod z poprzedniego zadania z pogodą.

Utwórz klasę WeatherForecast, która będzie służyła do odczytywania i zapisywania pliku, a także odpytywania API.

Obiekt klasy WeatherForecast dodatkowo musi poprawnie implementować cztery metody:

     __setitem__
     __getitem__
     __iter__
     items


Wykorzystaj w kodzie poniższe zapytania:

    weather_forecast[date] da odpowiedź na temat pogody dla podanej daty
    weather_forecast.items() zwróci generator tupli w formacie (data, pogoda) dla już zapisanych rezultatów przy wywołaniu
    weather_forecast to iterator zwracający wszystkie daty, dla których znana jest pogoda
"""
from weather_forecast import WeatherAPI

weather_forecast = WeatherAPI()
write_new_data_to_file = weather_forecast.retrieve_data()
if write_new_data_to_file:
    weather_forecast.write_data_to_file()
    print(f'W dniu {weather_forecast.date} w mieście {weather_forecast.city} {weather_forecast.raining_data}')
else:
    print(f'W dniu {weather_forecast.date} w mieście {weather_forecast.city} {weather_forecast.forecast_data.get(weather_forecast.city).get(weather_forecast.date)}')

for item in weather_forecast.items():
    print(item)
for city in weather_forecast:
    print(city)

print(weather_forecast["Warszawa", "2023-09-01"])
print(weather_forecast["Elk", "2023-11-12"])