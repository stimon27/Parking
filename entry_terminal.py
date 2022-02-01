# Entry terminal

import datetime

import null as null
import pymongo
import re

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster01.yxbr3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['CarSUSDB']

menu_options = {
    1: 'Wjedź na parking',
    2: 'Sprawdź bilans karty',
    3: 'Wyjście'
}

price = 4


def print_menu():
    print()
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def validate_pin(card_number):
    if len(card_number) == 4:
        return re.search('[^0-9]', card_number) is None
    else:
        return False


def option1():
    print('\nWpisz numer karty, aby móc wjechać na parking')
    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        result = database['Users'].find_one({'card_id': '{}'.format(card_number_input)})
        visit = database['Visits'].find_one({
            'card_id': '{}'.format(card_number_input),
            'status': 'running'
        })

        if result:
            if visit is None:
                login = result['login']
                balance = result['acc_balance']

                if balance >= 0:
                    print('\nWitaj na naszym parkingu ', login,
                          '\nPamiętaj, aby przy wyjeździe zapłacić! :)')

                    enter_time = datetime.datetime.now()

                    visit = {
                        "user_id": result["_id"],
                        "enter_time": enter_time,
                        "status": "running",
                        "price": 0,
                        "price_hour": price,
                        "card_id": card_number_input
                    }

                    database["Visits"].insert_one(visit)
                else:
                    print('\nPrzykro mi przyjacielu, twoje karta jest na debecie, '
                          '\nwięc zgodnie z naszym regulaminem nie możesz wjechać na parking :(')
            else:
                print("\nWygląda na to, że już u nas zaparkowałeś")
        else:
            print("\nNiewłaściwe dane")
    else:
        print('\nNiewłaściwy pin!')


def option2():
    print('\nWpisz numer karty, aby sprawdzić jej bilans')
    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        result = database['Users'].find_one({'card_id': '{}'.format(card_number_input)})

        if result:
            balance = result['acc_balance']
            print('\nBilans twojej karty [w PLN] to:', balance)
        else:
            print("\nNiewłaściwe dane.")
    else:
        print('\nNiewłaściwy pin!')


def main():
    print('\nWitaj w systemie parkingowym, \nwybierz opcje z menu:')
    while True:
        print_menu()

        option = ''

        try:
            option = int(input('Wpisz numer wyboru: '))
        except:
            print('\nNiewłaściwe dane wejściowe. Proszę wprowadź numer ...')

        if option == 1:
            option1()
        elif option == 2:
            option2()
        elif option == 3:
            print('\nDo zobaczenia! :)')
            exit()
        else:
            print('\nNiewłaściwy numer. Proszę wprowadź numer w zakresie od 1 do 3')


if __name__ == '__main__':
    main()
