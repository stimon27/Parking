# Exit terminal
import math
import re, datetime, pymongo

client = pymongo.MongoClient(
    "mongodb+srv://admin:admin@cluster01.yxbr3.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

database = client['CarSUSDB']

menu_options = {
    1: 'Zapłać i wyjedź z parkingu',
    2: 'Wyjście'
}

parking_cost = 5


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
    print('\nWpisz numer karty, aby zapłacić za parking i z niego wyjechać')
    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        result = database['Users'].find_one({'card_id': '{}'.format(card_number_input)})

        if result:
            login = result['login']
            balance = result['acc_balance']

            visit = database['Visits'].find_one({
                'card_id': '{}'.format(card_number_input),
                'status': 'running'
            })

            if visit:
                entry_time = visit['enter_time']
                exit_time = datetime.datetime.now()

                parking_hours = math.floor(abs((exit_time - entry_time).seconds / 3600))
                parking_hours += 1

                price = parking_hours * visit['price_hour']

                balance -= price

                database['Users'].update_one(
                    {'login': '{}'.format(login)},
                    {"$set": {'acc_balance': balance}},
                    True
                )

                database['Visits'].update_one(
                    {
                        'card_id': '{}'.format(card_number_input),
                        'status': 'running'
                    },
                    {
                        "$set":
                            {
                                'status': "finished",
                                'price': price,
                                'leave_time': exit_time
                            }
                    },
                    True
                )

                print('\nZapłacono pomyślnie, możesz wyjechać z parkingu :)')
            else:
                print("\nNajpierw zaparkuj u nas, dopiero póżniej zapłacisz")
        else:
            print("\nUżytkownik nie istnieje")
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
            print('\nDo zobaczenia! :)')
            exit()
        else:
            print('\nNiewłaściwy numer. Proszę wprowadź numer 1 albo 2')


if __name__ == '__main__':
    main()
