from files_management import load_data_from_file
from files_management import load_operation_log
from files_management import write_data_to_file
from files_management import write_log_to_file
import time

account_balance = load_data_from_file(file="stock.txt")["account_balance"]
kitchen_warehouse = load_data_from_file(file="stock.txt")["magazyn"]
operation_log = load_operation_log(file="operation_log.txt")
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

print("Witaj.")
initial_message = "Komendy dostępne dla twojego magazynu wysposażenia kuchni:"
run_operation = True
while run_operation:
    print(initial_message)
    for keys, values in available_prompts.items():
        print(f"{keys}: {values}")
    try:
        choice = int(input("Podaj numer komendy z listy powyżej: "))
    except ValueError:
        print("Wybrałeś niedostępną komendę. Spróbuj jeszcze raz.")
        continue
    match choice:
        case 1:  # account value update
            amount = None
            while amount is None:
                try:
                    amount = float(input("Podaj kwotę, o którą należy skorygować saldo: ") or "200")
                except ValueError:
                    print("Nie podano kwoty. Spróbuj jeszcze raz.")
                    continue
            add_deduct = input(
                'Wpisz:\n "+" jeśli chcesz dodać saldo\n "-" jeśli chcesz odjąć saldo\nWybierz + lub -:') or "+"
            while add_deduct not in ["+","-"]:
                add_deduct = input('Nieprawidłowa odpowiedź.\nWpisz:\n "+" jeśli chcesz dodać saldo\n "-" jeśli '
                                   'chcesz odjąć saldo.\nTwój wybór: ')
            match add_deduct:
                case "+":
                    account_balance += amount
                case "-":
                    account_balance -= amount
            operation_log.append(
                f"Zmieniono saldo konta o: {add_deduct} {amount} PLN.")
            print('*' * 50)
            print(f'\n{operation_log[-1]}')
            print(f'Aktualne saldo to: {account_balance}\n')
            print('*' * 50)
            time.sleep(2)
        case 2:  # warehouse update after sale
            product_chosen = False
            while not product_chosen:
                print("Podaj nazwę produktu z następujących dostępnych w magazynie:")
                for products in kitchen_warehouse:
                    print(products)
                product = input("Wybrany produkt: ")
                while product not in kitchen_warehouse.keys():
                    product = input("Wybranego produktu nie ma w magazynie. Podaj nazwę dostępnego produktu: ")
                product_chosen = True
                how_many = None
                while how_many is None:
                    try:
                        how_many = int(input(f'W magazynie jest {kitchen_warehouse[product]["liczba"]}. Ile sztuk '
                                             f'sprzedano?: '))
                    except ValueError:
                        print('Twoja odpowiedź nie jest liczbą. Spróbuj jeszcze raz.')
                        continue
                while how_many > kitchen_warehouse[product]["liczba"]:
                    how_many = None
                    while how_many is None:
                        try:
                            how_many = int(input(f'W magazynie nie ma tylu sztuk towaru. Dostępnych jest '
                                         f'{kitchen_warehouse[product]["liczba"]} sztuk. Ile sztuk sprzedano?: '))
                        except ValueError:
                            print('Twoja odpowiedź nie jest liczbą. Spróbuj jeszcze raz.')
                            continue
                kitchen_warehouse[product]["liczba"] -= how_many
                account_balance += kitchen_warehouse[product]["cena"] * how_many
                operation_log.append(f'{available_prompts[choice]} {how_many} sztuk produktu: {product}.')
                print('*' * 50)
                print(f'\n{operation_log[-1]}')
                print(f'Stan konta zaktualizowany. Obecne saldo: {account_balance}\n')
                print('*' * 50)
                time.sleep(2)
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
                    try:
                        number_bought = float(input('Podaj ilość zakupionego produktu, który należy dodać do magazynu: '))
                    except ValueError:
                        print('Twoja odpowiedź nie jest liczbą. Spróbuj jeszcze raz.')
                        continue
                while price_bought is None:
                    try:
                        price_bought = float(input('Podaj cenę jednostkową zakupionego produktu: '))
                    except ValueError:
                        print('Nie podałeś ceny jednostkowej zakupionego produktu. Spróbuj jeszcze raz.')
                if price_bought * number_bought > account_balance:
                    print(
                        'Wartość zamówienia przekracza saldo konta. Skoryguj liczbę zakupionych produktów lub cenę '
                        'jednostkową.')
                    account_check = False
            if product_bought in kitchen_warehouse.keys():
                if kitchen_warehouse[product_bought]["cena"] != price_bought:  # calculating new average buy price
                    average_price = (price_bought * number_bought + kitchen_warehouse[product_bought]["cena"] *
                                     kitchen_warehouse[product_bought]["liczba"]) / (number_bought +
                                                                                     kitchen_warehouse[product_bought][
                                                                                         "liczba"])
                    kitchen_warehouse[product_bought]["cena"] = average_price
                kitchen_warehouse[product_bought]["liczba"] += number_bought
            else:
                kitchen_warehouse[product_bought] = {"cena": price_bought, "liczba": number_bought}
            account_balance -= number_bought * price_bought
            operation_log.append(f'{available_prompts[choice]} {number_bought} sztuk produktu: {product_bought}.')
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print(f'Stan konta zaktualizowany. Obecne saldo: {account_balance}\n')
            print('*' * 50)
            time.sleep(2)
        case 4:  # show account value
            print('*' * 50)
            print(f'\nWyświetlam aktualne saldo konta: {account_balance}.\n')
            print('*' * 50)
            operation_log.append(f'Wyświetlono aktualne saldo konta: {account_balance}.')
            time.sleep(2)
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
            time.sleep(2)
        case 6:  # show product stock
            print('Wybierz produkt z następującej listy: ')
            for products in kitchen_warehouse.keys():
                print(products)
            product = input('Podaj produkt: ')
            while product not in kitchen_warehouse:
                product = input('Podanego produktu nie ma w magazynie. Podaj produkt z powyższej listy: ')
            operation_log.append(
                f'Wyświetlono stan magazynowy produktu {product}: {kitchen_warehouse[product]["liczba"]}'
                f' szt. Cena produktu: {kitchen_warehouse[product]["cena"]} PLN.')
            print('*' * 50)
            print(f'\nWyświetlam stan magazynowy produktu {product}: {kitchen_warehouse[product]["liczba"]}'
                f' szt. Cena produktu: {kitchen_warehouse[product]["cena"]} PLN.\n')
            print('*' * 50)
            time.sleep(2)
        case 7:  # show warehouse operation log
            print('Aby wyświetlić historię operacji podaj numer początkowy i końcowy operacji. Jeśli nie podasz żadnej '
                  'wartości, wyświetlony zostanie cały log.')
            input_info = True
            while input_info:
                log_in = input(f'Podaj początek zakresu operacji do przeglądu (od 0 do {len(operation_log) - 1}): ')
                try:
                    if log_in:
                        log_in = int(log_in)
                    input_info = False
                except ValueError:
                    input_info = True
                    continue
            input_info = True
            while input_info:
                log_out = input(f'Podaj koniec zakresu operacji do przeglądu (max {len(operation_log) - 1}): ')
                try:
                    if log_out:
                        log_out = int(log_out)
                    input_info = False
                except ValueError:
                    input_info = True
                    continue
            if not log_in and not log_out:
                for operation in operation_log:
                    print(operation)
            if log_in and not log_out:
                operation = log_in
                while operation <= len(operation_log):
                    print(operation_log[operation])
                    operation += 1
            if not log_in and log_out:
                log_in = 0
                while log_in <= log_out:
                    print(operation_log[log_in])
                    log_in += 1
            if log_in and log_out:
                operation = log_in
                while operation <= log_out:
                    print(operation_log[operation])
                    operation += 1
            operation_log.append("Wyświetlono listę zrealizowanych operacji.")
            print('*' * 50)
            print(f'\n{operation_log[-1]}\n')
            print('*' * 50)
            time.sleep(2)
        case 8:  # end program
            run_operation = False
            write_data_to_file(file="stock.txt", balance = account_balance, stock = kitchen_warehouse)
            write_log_to_file(file="operation_log.txt", hist_log=operation_log)
            print('*' * 50)
            print('\nMagazyn i konto zaktualizowane. Do zobaczenia.\n')
            print('*' * 50)
