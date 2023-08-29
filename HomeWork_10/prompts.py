from manager import Manager
import time

manager = Manager(operation_log_file="operation_log.txt", stock_file="stock.txt")

@manager.assign(1)
def change_balance(manager: Manager):
    amount = None
    while amount is None:
        try:
            amount = float(input("Podaj kwotę, o którą należy skorygować saldo: ")) #or "200")
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
            manager.account_balance += amount
        case "-":
            manager.account_balance -= amount
    manager.operation_log.append(
        f"Zmieniono saldo konta o: {add_deduct} {amount} PLN.")
    print('*' * 50)
    print(f'\n{manager.operation_log[-1]}')
    print(f'Aktualne saldo to: {manager.account_balance}\n')
    print('*' * 50)
    time.sleep(2)

@manager.assign(2)
def sell_item(manager: Manager):
    product_chosen = False
    while not product_chosen:
        print("Podaj nazwę produktu z następujących dostępnych w magazynie:")
        for products in manager.kitchen_warehouse:
            print(products)
        product = input("Wybrany produkt: ")
        while product not in manager.kitchen_warehouse.keys():
            product = input("Wybranego produktu nie ma w magazynie. Podaj nazwę dostępnego produktu: ")
        product_chosen = True
        how_many = None
        while how_many is None:
            try:
                how_many = int(input(f'W magazynie jest {manager.kitchen_warehouse[product]["liczba"]}. Ile sztuk '
                                     f'sprzedano?: '))
            except ValueError:
                print('Twoja odpowiedź nie jest liczbą. Spróbuj jeszcze raz.')
                continue
        while how_many > manager.kitchen_warehouse[product]["liczba"]:
            how_many = None
            while how_many is None:
                try:
                    how_many = int(input(f'W magazynie nie ma tylu sztuk towaru. Dostępnych jest '
                                         f'{manager.kitchen_warehouse[product]["liczba"]} sztuk. Ile sztuk sprzedano?: '))
                except ValueError:
                    print('Twoja odpowiedź nie jest liczbą. Spróbuj jeszcze raz.')
                    continue
        manager.kitchen_warehouse[product]["liczba"] -= how_many
        manager.account_balance += manager.kitchen_warehouse[product]["cena"] * how_many
        manager.operation_log.append(f'Sprzedaż {how_many} sztuk produktu: {product}.')

@manager.assign(3)
def buy_item(manager: Manager):
    account_check = False
    while not account_check:
        account_check = True
        product_bought = ''
        number_bought = 0
        price_bought = None
        while product_bought == '':
            product_bought = input('Podaj nazwę zakupionego produktu, który należy dodać do magazynu: ')
            if product_bought == '':
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
        if price_bought * number_bought > manager.account_balance:
            print(
                'Wartość zamówienia przekracza saldo konta. Skoryguj liczbę zakupionych produktów lub cenę '
                'jednostkową.')
            account_check = False
    if product_bought in manager.kitchen_warehouse.keys():
        if manager.kitchen_warehouse[product_bought]["cena"] != price_bought:  # calculating new average buy price
            average_price = (price_bought * number_bought + manager.kitchen_warehouse[product_bought]["cena"] *
                             manager.kitchen_warehouse[product_bought]["liczba"]) / (number_bought +
                                                                             manager.kitchen_warehouse[product_bought][
                                                                                 "liczba"])
            manager.kitchen_warehouse[product_bought]["cena"] = average_price
        manager.kitchen_warehouse[product_bought]["liczba"] += number_bought
    else:
        manager.kitchen_warehouse[product_bought] = {"cena": price_bought, "liczba": number_bought}
    manager.account_balance -= number_bought * price_bought
    manager.operation_log.append(f'Zakup {number_bought} sztuk produktu: {product_bought}.')
    print('*' * 50)
    print(f'\n{manager.operation_log[-1]}\n')
    print(f'Stan konta zaktualizowany. Obecne saldo: {manager.account_balance}\n')
    print('*' * 50)
    time.sleep(2)

@manager.assign(4)
def show_balance(manager: Manager):
    print('*' * 50)
    print(f'\nWyświetlam aktualne saldo konta: {manager.account_balance}.\n')
    print('*' * 50)
    manager.operation_log.append(f'Wyświetlono aktualne saldo konta: {manager.account_balance}.')
    time.sleep(2)

@manager.assign(5)
def show_stock_list(manager: Manager):
    print('*' * 50)
    print(f'\nW magazynie znajdują się następujące produkty:')
    for product, detail in manager.kitchen_warehouse.items():
        print(product)
        for position, more_details in detail.items():
            print(f' - {position}: {more_details}')
    print(f'\n')
    print('*' * 50)
    manager.operation_log.append('Wyświetlono stan magazynu.')
    time.sleep(2)

@manager.assign(6)
def show_product_data(manager: Manager):
    print('Wybierz produkt z następującej listy: ')
    for products in manager.kitchen_warehouse.keys():
        print(products)
    product = input('Podaj produkt: ')
    while product not in manager.kitchen_warehouse:
        product = input('Podanego produktu nie ma w magazynie. Podaj produkt z powyższej listy: ')
    manager.operation_log.append(
        f'Wyświetlono stan magazynowy produktu {product}: {manager.kitchen_warehouse[product]["liczba"]}'
        f' szt. Cena produktu: {manager.kitchen_warehouse[product]["cena"]} PLN.')
    print('*' * 50)
    print(f'\nWyświetlam stan magazynowy produktu {product}: {manager.kitchen_warehouse[product]["liczba"]}'
        f' szt. Cena produktu: {manager.kitchen_warehouse[product]["cena"]} PLN.\n')
    print('*' * 50)
    time.sleep(2)
@manager.assign(7)
def show_operation_log(manager: Manager):
    print('Aby wyświetlić historię operacji podaj numer początkowy i końcowy operacji. Jeśli nie podasz żadnej '
          'wartości, wyświetlony zostanie cały log.')
    input_info = True
    while input_info:
        log_in = input(f'Podaj początek zakresu operacji do przeglądu (od 0 do {len(manager.operation_log) - 1}): ')
        try:
            if log_in:
                log_in = int(log_in)
            input_info = False
        except ValueError:
            input_info = True
            continue
    input_info = True
    while input_info:
        log_out = input(f'Podaj koniec zakresu operacji do przeglądu (max {len(manager.operation_log) - 1}): ')
        try:
            if log_out:
                log_out = int(log_out)
            input_info = False
        except ValueError:
            input_info = True
            continue
    if not log_in and not log_out:
        for operation in manager.operation_log:
            print(operation)
    if log_in and not log_out:
        operation = log_in
        while operation < len(manager.operation_log):
            print(manager.operation_log[operation])
            operation += 1
    if not log_in and log_out:
        log_in = 0
        while log_in <= log_out:
            print(manager.operation_log[log_in])
            log_in += 1
    if log_in and log_out:
        operation = log_in
        while operation <= log_out:
            print(manager.operation_log[operation])
            operation += 1
    manager.operation_log.append("Wyświetlono listę zrealizowanych operacji.")
    print('*' * 50)
    print(f'\n{manager.operation_log[-1]}\n')
    print('*' * 50)
    time.sleep(2)

@manager.assign(8)
def end_operation(manager: Manager):
    manager.write_data_to_file(file=manager.stock_file)
    manager.write_log_to_file(file=manager.operation_log_file, hist_log=manager.operation_log)
    print('*' * 50)
    print('\nMagazyn i konto zaktualizowane. Do zobaczenia.\n')
    print('*' * 50)