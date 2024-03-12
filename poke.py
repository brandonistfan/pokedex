import requests
import json

def catch_pokemon(url, pokedex_file):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        pokemon_info = get_data(data)
        append_pokedex(pokedex_file, pokemon_info)
    else: 
        print(f"Failed to retreive data, status code: {response.status_code}")

def get_data(data):
    info = {}
    name = data['species']['name']

    type = ''
    amount_of_types = len(data['types'])

    for t in range(amount_of_types):
        if t == amount_of_types - 1:
            type += data['types'][t]['type']['name'].capitalize()
        else:
            type += data['types'][t]['type']['name'].capitalize() + ", "

    
    ability = ''
    amount_of_abilities = len(data['abilities'])

    for a in range(amount_of_abilities):
        if a == amount_of_abilities - 1:
            ability += data['abilities'][a]['ability']['name'].capitalize()
        else:
            ability += data['abilities'][a]['ability']['name'].capitalize() + ", "

    info.update({'Pokemon': name.capitalize(), 'Info': {'Types': type, 'Abilities': ability}})
    
    print(name.capitalize() + ' has been successfully added to the pokedex.')

    return info


def append_pokedex(pokedex_file, pokemon_info):
    data = load_pokedex(pokedex_file)

    data.append(pokemon_info)

    with open(pokedex_file, 'w') as pokedex:
        json.dump(data, pokedex, indent = 4)

def load_pokedex(pokedex_file):
    try:
        with open(pokedex_file, 'r') as pokedex:
            data = json.load(pokedex)
            
    except FileNotFoundError:
        data = []

    return data

choice = input('Would you like to load or add pokemon (Load/Add): ').lower()

pokedex_file = input('Enter current pokedex: ')

if choice == 'load':
    data = json.dumps(load_pokedex(pokedex_file), indent=4)
    if data == '[]':
        print('The chosen pokedex is empty.')
    else:
        print(data)

elif choice == 'add':

    pokemon = input('Enter pokemon to get data: ').lower()

    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}/'

    catch_pokemon(url, pokedex_file)