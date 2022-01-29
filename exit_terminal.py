# Exit terminal

import re
import pymongo

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster01.yxbr3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['CarSUSDB']

menu_options = {
    1: 'Zapłać i wyjedź z parkingu',
    2: 'Wyjście'
}

# PSUEDO PARKING CONST
parking_cost = 100


def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def validate_pin(card_number):
    if len(card_number) == 4:
        return re.search('[^0-9]', card_number) is None
    else:
        return False


def option1():
    print('Wpisz numer karty, aby zapłacić na parking i z niego wyjechać:')
    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        result = database['Users'].find_one({'card_id': '{}'.format(card_number_input)})

        if result:
            print(result)
            login = result['login']
            balance = result['acc_balance']

            if balance >= 0:
                balance -= parking_cost
                print('Zapłacono pomyślnie, możesz wyjechać z parkingu :)')
                database['Users'].update_one(
                    {'login': '{}'.format(login)},
                    {"$set": {'acc_balance': balance}},
                    True
                )
            else:
                print('Przykro mi przyjacielu, twoje karta jest na debecie, '
                      'więc zgodnie z naszym regulaminem nie możesz wyjechać z parkingu :(')
                exit()
        else:
            print("no user")
    else:
        print('Niewłaściwy pin!')


def main():
    print('\nWitaj w systemie parkingowym, \nwybierz opcje z menu:\n')

    while True:
        print_menu()
        option = ''

        try:
            option = int(input('Wpisz numer wyboru: '))
        except:
            print('Niewłaściwe dane wejściowe. Proszę wprowadź numer ...')

        if option == 1:
            option1()
        elif option == 2:
            print('Do zobaczenia! :)')
            exit()
        else:
            print('Niewłaściwy numer. Proszę wprowadź numer 1 albo 2')


if __name__ == '__main__':
    main()
