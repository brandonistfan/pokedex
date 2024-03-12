import requests
import json

def catch_pokemon(url, pokedex_file):
    try: 
        response = requests.get(url)
        data = response.json()
        pokemon_info = get_data(data)
        append_pokedex(pokedex_file, pokemon_info)
    except requests.exceptions.HTTPError as errh: 
        print("HTTP Error") 
        print(errh.args[0]) 
    except requests.exceptions.ReadTimeout as errrt: 
        print("Time out") 
    except requests.exceptions.ConnectionError as conerr: 
        print("Connection error") 
    except requests.exceptions.RequestException as errex: 
        print("Exception request") 
    
def get_data(data):
    name = data['species']['name'].capitalize()

    types = [t['type']['name'].capitalize() for t in data['types']]
    abilities = [a['ability']['name'].capitalize() for a in data['abilities']]

    info = {'Pokemon': name, 'Info': {'Types': ', '.join(types), 'Abilities': ', '.join(abilities)}}
    
    print(f"{name} has been successfully added to the pokedex.")
    return info


def append_pokedex(pokedex_file, pokemon_info):
    data = load_pokedex(pokedex_file)

    data.append(pokemon_info)

    with open(pokedex_file, 'w') as pokedex:
        json.dump(data, pokedex, indent = 4)

def remove_pokemon(pokedex_file, pokemon_to_delete):
    data = load_pokedex(pokedex_file)
    index = 0
    for pokemon in data:
        if pokemon['Pokemon'].lower() == pokemon_to_delete.lower():
            print(pokemon['Pokemon'])
            print(pokemon_to_delete)
            del data[index]
        index += 1

    with open(pokedex_file, 'w') as pokedex:
        json.dump(data, pokedex, indent = 4)

def load_pokedex(pokedex_file):
    try:
        with open(pokedex_file, 'r') as pokedex:
            data = json.load(pokedex)
            
    except FileNotFoundError:
        data = []

    return data

choice = input('Would you like to load or add pokemon to your pokedex (Load/Add/Remove): ').lower()

pokedex_file = input('Enter your pokedex: ')

if choice == 'load':
    data = json.dumps(load_pokedex(pokedex_file), indent=4)
    if data == '[]':
        print('The selected pokedex is empty.')
    else:
        print(data)

elif choice == 'add':
    pokemon = input('Enter the pokemon to add: ').lower()

    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon}/'

    catch_pokemon(url, pokedex_file)

elif choice == 'remove':
    pokemon = input('Enter the pokemon to remove: ').lower()
    
    remove_pokemon(pokedex_file, pokemon)

    data = json.dumps(load_pokedex(pokedex_file), indent=4)
    if data == '[]':
        print('The selected pokedex is empty.')
    else:
        print(data)