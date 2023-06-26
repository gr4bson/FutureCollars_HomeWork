"""
Napisz program, który będzie rejestrował operacje na koncie firmy i stan magazynu.

Program po uruchomieniu wyświetla informację o dostępnych komendach:
    saldo
    sprzedaż
    zakup
    konto
    lista
    magazyn
    przegląd
    koniec


Po wprowadzeniu odpowiedniej komendy, aplikacja zachowuje się w unikalny sposób dla każdej z nich:
    saldo - Program pobiera kwotę do dodania lub odjęcia z konta.
    sprzedaż - Program pobiera nazwę produktu, cenę oraz liczbę sztuk. Produkt musi znajdować się w magazynie.
        Obliczenia respektuje względem konta i magazynu (np. produkt "rower" o cenie 100 i jednej sztuce spowoduje
        odjęcie z magazynu produktu "rower" oraz dodanie do konta kwoty 100).
    zakup - Program pobiera nazwę produktu, cenę oraz liczbę sztuk. Produkt zostaje dodany do magazynu, jeśli go
        nie było. Obliczenia są wykonane odwrotnie do komendy "sprzedaz". Saldo konta po zakończeniu operacji „zakup”
        nie może być ujemne.
    konto - Program wyświetla stan konta.
    lista - Program wyświetla całkowity stan magazynu wraz z cenami produktów i ich ilością.
    magazyn - Program wyświetla stan magazynu dla konkretnego produktu. Należy podać jego nazwę.
    przegląd - Program pobiera dwie zmienne „od” i „do”, na ich podstawie wyświetla wszystkie wprowadzone akcje zapisane
        pod indeksami od „od” do „do”. Jeżeli użytkownik podał pustą wartość „od” lub „do”, program powinien wypisać
        przegląd od początku lub/i do końca. Jeżeli użytkownik podał zmienne spoza zakresu, program powinien o tym
        poinformować i wyświetlić liczbę zapisanych komend (żeby pozwolić użytkownikowi wybrać odpowiedni zakres).
    koniec - Aplikacja kończy działanie.

Dodatkowe wymagania:
    Aplikacja od uruchomienia działa tak długo, aż podamy komendę "koniec".
    Komendy saldo, sprzedaż i zakup są zapamiętywane przez program, aby móc użyć komendy "przeglad".
    Po wykonaniu dowolnej komendy (np. "saldo") aplikacja ponownie wyświetla informację o dostępnych komendach, a także
    prosi o wprowadzenie jednej z nich.
    Zadbaj o błędy, które mogą się pojawić w trakcie wykonywania operacji (np. przy komendzie "zakup" jeśli dla produktu
     podamy ujemną kwotę, aplikacja powinna wyświetlić informację o niemożności wykonania operacji i jej nie wykonać).
     Zadbaj też o prawidłowe typy danych.
"""
account_balance = 1000
available_prompts = {
    1: "Saldo",
    2: "Sprzedaż",
    3: "Zakup",
    4: "Konto",
    5: "Lista",
    6: "Magazyn",
    7: "Przegląd",
    8: "Koniec"
}
kitchen_warehouse = {
    'szklanka': {
        'cena': 10.99,
        'liczba': 1000
    },
    'kieliszek': {
        'cena': 5.99,
        'liczba': 1000
    },
    'filizanka': {
        'cena': 12.75,
        'liczba': 1000
    },
    'widelec': {
        'cena': 2.75,
        'liczba': 1000
    },
    'lyzka': {
        'cena': 1.75,
        'liczba': 1000
    },
    'noz': {
        'cena': 12.75,
        'liczba': 1000
    },
}
operation_log = []
print('Witaj.')
initial_message = "Komendy dostępne dla twojego magazynu wysposażenia kuchni:"
run_operation = True
while run_operation:
    print(initial_message)
    for keys, values in available_prompts.items():
        print(f'{keys}: {values}')
    choice = int(input('Podaj numer komendy z listy powyżej: '))
    match choice:
        case 1:  # account value update
            amount = float(input('Podaj kwotę, o którą należy skorygować saldo: ') or "200")
            add_deduct = input(
                'Wpisz:\n "+" jeśli chcesz dodać saldo\n "-" jeśli chcesz odjąć saldo:\nWybierz + lub -:') or "+"
            match add_deduct:
                case "+":
                    account_balance += amount
                case "-":
                    account_balance -= amount
            operation_log.append(
                f'Zmieniono saldo konta o: {add_deduct} {amount} PLN. Aktualne saldo to: {account_balance}')
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print('*' * 50)
        case 2:  # warehouse update after sale
            product_chosen = False
            while not product_chosen:
                print('Podaj nazwę produktu z następujących dostępnych w magazynie:')
                for products in kitchen_warehouse:
                    print(products)
                product = input('Wybrany produkt: ')
                while product not in kitchen_warehouse.keys():
                    product = input('Wybranego produktu nie ma w magazynie. Podaj nazwę dostępnego produktu: ')
                product_chosen = True
                how_many = int(
                    input(f'W magazynie jest {kitchen_warehouse[product]["liczba"]}. Ile sztuk sprzedano?: '))
                while how_many > kitchen_warehouse[product]["liczba"]:
                    how_many = int(input(f'W magazynie nie ma tylu sztuk towaru. Dostępnych jest '
                                         f'{kitchen_warehouse[product]["liczba"]} sztuk. Ile sztuk sprzedano?: '))
                kitchen_warehouse[product]["liczba"] -= how_many
                account_balance += kitchen_warehouse[product]["cena"] * how_many
                operation_log.append(f'\n{available_prompts[choice]} {how_many} sztuk produktu: '
                                     f'{product}\nStan konta zaktualizowany. Obecne saldo: {account_balance}\n')
                print('*' * 50)
                print(f'\n{operation_log[-1]}\n')
                print('*' * 50)
        case 3:  # warehouse update after buy
            account_check = False
            while not account_check:
                account_check = True
                product_bought = ''
                number_bought = 0
                price_bought = None
                while product_bought == '':
                    product_bought = input('Podaj nazwę zakupionego produktu, który należy dodać do magazynu: ')
                    if product_bought == '' or type(product_bought) != str:
                        print('Nie podałeś nazwy produktu. Spróbuj jeszcze raz.')
                        product_bought = ''
                while number_bought == 0:
                    number_bought = float(input('Podaj ilość zakupionego produktu, który należy dodać do magazynu: '))
                    if number_bought == 0 or type(number_bought) != float:
                        print('Nie podałeś liczby zakupionych produktów lub podałeś 0. Spróbuj jeszcze raz.')
                        product_bought = 0
                while price_bought is None:
                    price_bought = float(input('Podaj cenę jednostkową zakupionego produktu: '))
                    if price_bought is None or (type(price_bought) != int and type(price_bought) != float):
                        print('Nie podałeś ceny jednostkowej zakupionego produktu. Spróbuj jeszcze raz.')
                        price_bought = None
                if price_bought * number_bought > account_balance:
                    print(
                        'Wartość zamówienia przekracza saldo konta. Skoryguj liczbę zakupionych produktów lub cenę '
                        'jednostkową.')
                    account_check = False
            if product_bought in kitchen_warehouse.keys():
                if kitchen_warehouse[product_bought]['cena'] != price_bought:  # calculating new average buy price
                    average_price = (price_bought * number_bought + kitchen_warehouse[product_bought]['cena'] *
                                     kitchen_warehouse[product_bought]['liczba']) / (number_bought +
                                                                                     kitchen_warehouse[product_bought][
                                                                                         'liczba'])
                    kitchen_warehouse[product_bought]['cena'] = average_price
                kitchen_warehouse[product_bought]['liczba'] += number_bought
            else:
                kitchen_warehouse[product_bought] = {'cena': price_bought, 'liczba': number_bought}
            account_balance -= number_bought * price_bought
            operation_log.append(f'\n{available_prompts[choice]} {number_bought} sztuk produktu: '
                                 f'{product_bought}\nStan konta zaktualizowany. Obecne saldo: {account_balance}\n')
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print('*' * 50)
        case 4:  # show account value
            operation_log.append(f'Wyświetlam aktualne saldo konta: {account_balance}')
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print('*' * 50)
        case 5:  # show warehouse stock
            print('*' * 50)
            print(f'\nW magazynie znajdują się następujące produkty:')
            for product, detail in kitchen_warehouse.items():
                print(product)
                for position, more_details in detail.items():
                    print(f' - {position}: {more_details}')
                    # print(f' - {stock}')
            print(f'\n')
            print('*' * 50)
            operation_log.append('Wyświetlono stan magazynu.')
        case 6:  # show product stock
            print('Wybierz produkt z następującej listy: ')
            for products in kitchen_warehouse.keys():
                print(products)
            product = input('Podaj produkt: ')
            while product not in kitchen_warehouse:
                product = input('Podanego produktu nie ma w magazynie. Podaj produkt z powyższej listy: ')
            operation_log.append(
                f'Wyświatlam stan magazynowy produktu {product}: {kitchen_warehouse[product]["liczba"]}'
                f' szt. Cena produktu: {kitchen_warehouse[product]["cena"]} PLN.')
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print('*' * 50)
        case 7:  # show warehouse operation log
            print('Aby wyświetlić historię operacji podaj numer początkowy i końcowy operacji.')
            log_in = input('Podaj początek zakresu operacji do przeglądu: ')
            log_out = input('Podaj koniec zakresu operacji do przeglądu: ')
            if not log_in and not log_out:
                for operation in operation_log:
                    print(operation)
            if log_in and not log_out:
                operation = int(log_in)
                while operation <= len(operation_log):
                    print(operation_log[operation])
                    operation += 1
            if not log_in and log_out:
                log_in = 0
                while log_in <= int(log_out):
                    print(operation_log[log_in])
                    log_in += 1
            if log_in and log_out:
                operation = int(log_in)
                while operation <= int(log_out):
                    print(operation_log[operation])
                    operation += 1
            operation_log.append("Wyświetlono listę zrealizowanych operacji.")
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print('*' * 50)
        case 8:  # end program
            run_operation = False
            print('*' * 50)
            print('\nMagazyn i konto zaktualizowane. Do zobaczenia.')
            print('*' * 50)
