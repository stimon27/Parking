#Entry terminal

import re

menu_options = {
    1: 'Wjedź na parking',
    2: 'Sprawdź bilans karty',
    3: 'Wyjście'
}

class Customer:
    def __init__(self, name, card_number, card_balance): 
        self.name = name 
        self.card_number = card_number
        self.card_balance = card_balance

#PSEUDO DATABASE
customer_list = []
customer_list.append(Customer('Paweł', 1234, -400))
customer_list.append(Customer('Szymon', 2345, 500))
customer_list.append(Customer('Łukasz', 3456, -600))
customer_list.append(Customer('Danil', 4567, 700))

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key])

def validate_pin(card_number):
    if len(card_number) == 4:
        return re.search('[^0-9]', card_number) is None
    else:   
        return False

def option1():
    print('Wpisz numer karty, aby móc wjechać na parking')

    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        tmp_check_owner_of_card_number = 0

        while tmp_check_owner_of_card_number < 4:

            if int(card_number_input) == customer_list[tmp_check_owner_of_card_number].card_number:
                if customer_list[tmp_check_owner_of_card_number].card_balance >= 0:
                    print('Witaj na naszym parkingu', customer_list[tmp_check_owner_of_card_number].name,'\nPamiętaj, aby przy wyjeździe zapłacić! :)')
                    tmp_check_owner_of_card_number += 1
                else:
                    print('Przykro mi przyjacielu, twoje karta jest na debecie, więc zgodnie z naszym regulaminem nie możesz wjechać na parking :(')
                    exit()
            else:
                tmp_check_owner_of_card_number += 1

        exit()
    else:
        print('Niewłaściwy pin!')

def option2():
    print('Wpisz numer karty, aby sprawdzić jej bilans')

    card_number_input = ''
    card_number_input = input('Twój kod pin: ')

    if validate_pin(card_number_input):
        tmp_check_owner_of_card_number = 0

        while tmp_check_owner_of_card_number < 4:

            if int(card_number_input) == customer_list[tmp_check_owner_of_card_number].card_number:
                print('Bilans twojej karty [w PLN] to:', customer_list[tmp_check_owner_of_card_number].card_balance)
                tmp_check_owner_of_card_number += 1
            else:
                tmp_check_owner_of_card_number += 1

        exit()
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
                option2()
            elif option == 3:
                print('Do zobaczenia! :)')
                exit()
            else:
                print('Niewłaściwy numer. Proszę wprowadź numer w zakresie od 1 do 3')


if __name__ == '__main__':
    main()
