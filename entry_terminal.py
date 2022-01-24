#Entry terminal
from pickle import FALSE
import re

menu_options = {
    1: 'Wjedź na parking',
    2: 'Sprawdź bilans karty',
    3: 'Exit',
}
class customer: 
    def __init__(self, name, card_number): 
        self.name = name 
        self.card_number = card_number

#PSEUDO DATABASE
customer_list = []
customer_list.append(customer('Paweł', 1234))
customer_list.append(customer('Szymon', 2345))
customer_list.append(customer('Łukasz', 3456))
customer_list.append(customer('Danil', 4567))

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key])

def validate_pin(card_number):
    if len(card_number) == 4:
        if re.search('[^0-9]', card_number) == None: 
            return True
        else:
            return False
    else:   
        return False

def option1():
    print('Witaj w systemie parkingowym')
    print('Wpisz numer karty, aby móc wjechać na parking')
    print(customer_list[0].card_number)

    card_number_input = ''
    card_number_input = input("Twój pin: ")

    if validate_pin(card_number_input) == True: #tu bedziemy sprawdzac (w funkcji validate_pin) czy nr zgadza sie z tym w bazie, jesli sie zgadza - czyli card_number rowna sie temu z bazy to metoda zwroci nam true to program robi brrr i leci dalej
        tmp_check_owner_of_card_number = 0
        while(tmp_check_owner_of_card_number < 4):
            if int(card_number_input) == customer_list[tmp_check_owner_of_card_number].card_number:
                print('Witaj na naszym parkingu', customer_list[tmp_check_owner_of_card_number].name,'\nPamiętaj, aby przy wyjeździe zapłacić!')
                tmp_check_owner_of_card_number += 1
            else:
                tmp_check_owner_of_card_number += 1

        exit()
    else:
        print('Niewłaściwy pin!')

def option2():
    print('tu cos powstanie')

def main():
        while(True):
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
                print('Do zobaczenia!')
                exit()
            else:
                print('Niewłaściwy numer. Proszę wprowadź numer w zakresie od 1 do 3')

main()
