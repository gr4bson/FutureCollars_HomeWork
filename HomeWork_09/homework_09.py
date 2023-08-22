"""
Napisz program oparty na klasach i dziedziczeniu, który odczyta wejściowy plik, następnie zmodyfikuje go i wyświetli
w terminalu jego zawartość, a na końcu zapisze w wybranej lokalizacji.

Uruchomienie programu przez terminal:
python reader.py <plik_wejsciowy> <plik_wyjsciowy> <zmiana_1> <zmiana_2> ... <zmiana_n>

     <plik_wejsciowy> - nazwa pliku, który ma zostać odczytany, np. in.csv, in.json lub in.txt
     <plik_wyjsciowy> - nazwa pliku, do którego ma zostać zapisana zawartość, np. out.csv, out.json, out.txt
     lub out.pickle
     <zmiana_x> - Zmiana w postaci "x,y,wartosc" - x (kolumna) oraz y (wiersz) są współrzędnymi liczonymi od 0,
     natomiast "wartosc" zmianą która ma trafić na podane miejsce.


Przykładowy plik wejściowy znajduje się w repozytorium pod nazwą "in.json”.

Przykład działania:
python reader.py in.json out.csv 0,0,gitara 3,1,kubek 1,2,17 3,3,0
Z pliku in.json ma wyjść plik out.csv:
gitara,3,7,0
kanapka,12,5,kubek
pedzel,17,34,5
plakat,czerwony,8,0
Wymagane formaty:

    .csv
    .json
    .txt
    .pickle
"""
import sys

from file_handler import FileHandler

input_file = sys.argv[1]
output_file = sys.argv[2]
list_of_changes = sys.argv[3:]

file = FileHandler(input_file=input_file, output_file=output_file, list_of_changes=list_of_changes)
file.check_file_extension()
if file.chosen_handler:
    file.chosen_handler.read_data_from_file()
    if file.input_file_exists:
        file.chosen_handler.prepare_data_to_save()
        file.chosen_handler.write_data_to_file()
    else:
        print(f'Input file {input_file} missing')
else:
    print('File extension not supported. Supported file extensions: json, pkl, txt and csv')

