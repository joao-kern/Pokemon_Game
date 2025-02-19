import requests
import json

def get_weaknesses(types):
    weaknesses = set()
    for poke_type in types:
        type_response = requests.get(f"https://pokeapi.co/api/v2/type/{poke_type.lower()}")
        type_data = type_response.json()
        
        for weakness in type_data["damage_relations"]["double_damage_from"]:
            weaknesses.add(weakness["name"].capitalize())
    
    return list(weaknesses)

def get_hp(data):
    for stat in data["stats"]:
        if stat["stat"]["name"] == "hp":
            return stat["base_stat"]

def get_moves(data, pokemon_types):
    moves = []
    same_type_found = False

    for move in data["moves"]:
        move_name = move["move"]["name"].capitalize()
        move_id = move["move"]["url"].split("/")[-2]
        move_data = requests.get(f"https://pokeapi.co/api/v2/move/{move_id}").json()

        move_power = float(move_data["power"]) if move_data["power"] else 0
        if move_power == 0:
            continue

        move_type = move_data["type"]["name"].capitalize()
        moves.append({"name": move_name, "type": move_type, "damage": move_power})

        if move_type in pokemon_types:
            same_type_found = True

        if len(moves) == 4:
            break

    if not same_type_found:
        for move in data["moves"]:
            move_id = move["move"]["url"].split("/")[-2]
            move_data = requests.get(f"https://pokeapi.co/api/v2/move/{move_id}").json()
            move_type = move_data["type"]["name"].capitalize()

            if move_type in pokemon_types:
                move_name = move["move"]["name"].capitalize()
                move_power = float(move_data["power"]) if move_data["power"] else 0

                if not moves:
                    moves.append({"name": move_name, "type": move_type, "damage": move_power})
                else:
                    moves[0] = {"name": move_name, "type": move_type, "damage": move_power}
                break

    return moves

def get_attack(data):
    for stat in data["stats"]:
        if stat["stat"]["name"] == "attack":
            return stat["base_stat"]

def get_defense(data):
    for stat in data["stats"]:
        if stat["stat"]["name"] == "defense":
            return stat["base_stat"]

pokemons = []

for i in range(1, 152):
            response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{i}")
            data = response.json()

            types = [t["type"]["name"].capitalize() for t in data["types"]]

            weaknesses = get_weaknesses(types)

            hp = get_hp(data)

            moves = get_moves(data, types)

            attack = get_attack(data)

            defense = get_defense(data)

            pokemon = {
                "id": data["id"],
                "name": data["name"].capitalize(),
                "types": types,
                "weaknesses": weaknesses,
                "hp": float(hp),
                "attack": int(attack),
                "defense": int(defense),
                "sprite_front": data["sprites"]["front_default"],
                "sprite_back": data["sprites"]["back_default"],
                "moves": moves
            }
            pokemons.append(pokemon)
    
with open("pokedex.json", "w") as file:
    json.dump(pokemons, file, indent=4)
