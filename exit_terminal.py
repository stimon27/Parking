# Exit terminal
import math
import re, datetime, pymongo, dns, certifi

client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster01.yxbr3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tlsCAFile=certifi.where())

database = client['CarSUSDB']

menu_options = {
    1: 'Zapłać i wyjedź z parkingu',
    2: 'Wyjście'
}

# HOURLY PARKING COST
parking_cost = 5

def print_menu():
    for key in menu_options.keys():
        print(key, '--', menu_options[key])


def validate_pin(card_number):
    if len(card_number) == 4:
        return re.search('[^0-9]', card_number) is None
    else:
        return False


def option1():
    print('Wpisz numer karty, aby zapłacić za parking i z niego wyjechać:')
    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        result = database['Users'].find_one({'card_id': '{}'.format(card_number_input)})

        if result:
            print(result)
            login = result['login']
            balance = result['acc_balance']

            entry_time = datetime.datetime.strptime('31/01/22 18:00:00', '%d/%m/%y %H:%M:%S')
            exit_time = datetime.datetime.now()

            parking_hours = math.floor(abs((exit_time - entry_time).seconds / 3600))
            if parking_hours == 0:
                parking_hours = 1

            balance -= parking_hours * parking_cost
            print('Zapłacono pomyślnie, możesz wyjechać z parkingu :)')
            database['Users'].update_one(
                {'login': '{}'.format(login)},
                {"$set": {'acc_balance': balance}},
                True
            )
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
