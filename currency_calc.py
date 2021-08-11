import requests
import json
import os

api_url = 'https://free.currconv.com'
api_key = os.environ.get('CURRCONV_API_KEY')

list_of_currencies = '/api/v7/currencies?apiKey='
source = requests.get(f'{api_url}{list_of_currencies}{api_key}').text

data = json.loads(source)
# print(json.dumps(data, indent=2))  # To get updated currency list

# with open('Currencies_Info.json', 'w') as f:  # To create updated currency list data file
#     json.dump(data, f, indent=2)


def helper_menu():
    user_help = input('Do you want to see all the currencies available ((Y)es/(N)o)? ').upper()
    if user_help == 'YES' or user_help == 'Y':
        for item in data['results']:
            currency_name = data['results'][item]['currencyName']
            currency_id = data['results'][item]['id']
            try:
                currency_sym = data['results'][item]['currencySymbol']
                print(f'{currency_name}: {currency_id} | {currency_sym}  ')
            except KeyError:
                print(f'{currency_name}: {currency_id}')


def currency_validate_input(text):
    all_currencies = [data['results'][item]['id'] for item in data['results']]
    while True:
        user_input = input(text).upper()
        if user_input not in all_currencies:
            print('The value you entered is not a valid currency!')
            continue
        break
    return user_input


helper_menu()

while True:
    try:
        amount = float(input('Amount of money to convert: '))
        from_c = currency_validate_input('Which currency do you want to convert from? ')
        to_c = currency_validate_input('Which currency do you want to convert to? ')

        convert = f'/api/v7/convert?q={from_c}_{to_c}&compact=ultra&apiKey='
        r = requests.get(f'{api_url}{convert}{api_key}').text
        value = json.loads(r)

        result = amount * value[f'{from_c}_{to_c}']
        print(f'{amount} {from_c} are {result:.2f} {to_c}')

    except ValueError:
        print('You can only input numbers!')
        continue
    break
