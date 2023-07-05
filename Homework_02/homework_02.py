'''
Napisz program do obsługi ładowarki paczek. Po uruchomieniu, aplikacja pyta ile paczek chcesz wysłać, a następnie wymaga podania wagi dla każdej z nich.
Na koniec działania program powinien wyświetlić w podsumowaniu:
    Liczbę paczek wysłanych
    Liczbę kilogramów wysłanych
    Suma "pustych" - kilogramów (brak optymalnego pakowania). Liczba paczek * 20 - liczba kilogramów wysłanych
    Która paczka miała najwięcej "pustych" kilogramów, jaki to był wynik
Restrykcje:
    Waga elementów musi być z przedziału od 1 do 10 kg.
    Każda paczka może maksymalnie zmieścić 20 kilogramów towaru.
    W przypadku, jeżeli dodawany element przekroczy wagę towaru, ma zostać dodany do nowej paczki, a obecna wysłana.
    W przypadku podania wagi elementu mniejszej od 1kg lub większej od 10kg, dodawanie paczek zostaje zakończone i wszystkie paczki są wysłane. Wyświetlane jest podsumowanie.
Przykład 1:
    Ilość elementów: 2
    Wagi elementów: 7, 9
Podsumowanie:
    Wysłano 1 paczkę (7+9)
    Wysłano 16 kg
    Suma pustych kilogramów: 4kg
    Najwięcej pustych kilogramów ma paczka 1 (4kg)

Przykład 2:
     Ilość elementów: 6
    Wagi elementów: 3, 6, 5, 8, 2, 3
Podsumowanie:
    Wysłano 2 paczki (3+6+5, 8+2+3)
    Wysłano 27 kg
    Suma pustych kilogramów: 13kg
    Najwięcej pustych kilogramów ma paczka 2 (7kg)

Przykład 3:
 I  lość elementów: 8
    Wagi elementów: 7, 14
    Podsumowanie:
    Wysłano 1 paczkę (7)
    Wysłano 7 kg
    Suma pustych kilogramów: 13kg
    Najwięcej pustych kilogramów ma paczka 13
'''
ask_again = True
while ask_again:
    try:
        items_to_send = int(input('Ile przedmiotów chcesz wysłać?: '))
    except ValueError:
        ask_again = True
        print('Nie podałeś/łaś liczby. Spróbuj jeszcze raz.')
        continue
    if items_to_send <=0:
        ask_again = True
        print('Podana wartośc jest <= 0. Spróbuj jeszcze raz.')
        continue
    ask_again = False
    item_no = 1
    package_weight = 0
    packages_sent = 1
    package_no = 1
    item_weights = []
    max_package_space_left = 0
    while item_no <= items_to_send:
        wrong_weight = False
        first_item_weight_wrong = False
        try:
            item_weight = float(input(f'Podaj masę przedmiotu nr {item_no} w kg: '))
        except ValueError:
            print('Nie podałeś/łaś masy przedmiotu. Spróbuj jeszcze raz.')
            continue
        if item_weight <= 0:
            print('Podana masa przedmiotu = 0. Spróbuj jeszcze raz.')
            continue
        elif item_weight > 10 or item_weight < 1:
            if sum(item_weights) == 0:
                first_item_weight_wrong = True
                print('Nie można wysyłać przedmiotów o wadze < 1kg lub > 10kg')
                break
            else:
                wrong_weight = True
                message = f'Waga przedmiotu {item_no} przekracza 10 kg lub jest poniżej 1 kg. Tego przedmiotu nie można wysłać.'
            break
        else:
            item_weights.append(item_weight)
            if package_weight + item_weight > 20:
                packages_sent += 1
                current_package_space_left = 20 - package_weight
                if current_package_space_left > max_package_space_left:
                    max_package_space_left = current_package_space_left
                    package_no = packages_sent
                package_weight = 0
            else:
                package_weight += item_weight
        item_no += 1

#the above loop does not add a package when the sum of all items added to that package = 20 kg
#if sum(item_weights) % 20 != 0:
#    packages_sent += 1
#   package_no += 1


if not first_item_weight_wrong:
    empty_space = packages_sent * 20 - sum(item_weights)
    print(f'Wysłano {packages_sent} paczek ważących łącznie {sum(item_weights)} kg')
    print(f'Suma pustych kilogramów = {empty_space}')
    if empty_space == 0:
        print('Paczki wypełnione w 100%. Brak pustej przestrzeni')
    else:
        print(f'Najwięcej pustych kilogramów ma paczka {package_no}')
    if wrong_weight:
        print(message)