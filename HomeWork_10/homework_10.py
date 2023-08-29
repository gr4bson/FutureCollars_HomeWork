"""
Rozbuduj program do zarządzania firmą. Wszystkie funkcjonalności (komendy, zapisywanie i czytanie przy użyciu pliku
itp.) pozostają bez zmian.

Stwórz clasę Manager, która będzie implementowała dwie kluczowe metody - execute i assign. Przy ich użyciu wywołuj
poszczególne fragmenty aplikacji. Metody execute i assign powinny zostać zaimplementowane zgodnie z przykładami
z materiałów do zajęć.

Niedozwolone są żadne zmienne globalne, wszystkie dane powinny być przechowywane wewnątrz obiektu Manage
"""
#from enums import ChoosePrompt
from prompts import manager
from files_management import FileManager
import time

initial_message = "Witaj w Twoim magazynie. Lista dostępnych komend to:\n" \
                  " 1. Saldo\n 2. Sprzedaż\n 3. Zakup\n 4. Konto\n 5. Lista\n 6. Magazyn\n 7. Przegląd\n 8. Koniec"
warehouse_handler = FileManager()
end_program = False
while not end_program:
    print(initial_message)
    #print(manager.operation_log)
    print(f"saldo: {manager.account_balance}")
    #print(manager.kitchen_warehouse)
    try:
        choice = int(input("Podaj operację, którą chcesz wykonać: "))
    except ValueError:
        choice = "unavailable"
    if choice == 8:
        end_program = True
        manager.write_data_to_file(
            file=manager.stock_file,
            balance=manager.account_balance,
            stock=manager.kitchen_warehouse
        )
        manager.write_log_to_file(
            file=manager.operation_log_file,
            hist_log=manager.operation_log)
    else:
        manager.execute(choice)