from model.pokemon import Pokemon
import json

class Pokedex:
    def __init__(self, file_path):        
        self.__read_file(file_path)

    def get_pokemons(self):
        return self.__pokemons
    
    def get_types(self):
        return self.__types

    def get_pokemons_by_type(self, pkmn_type):
        try:
            return self.__pokemons_by_type[pkmn_type]
        except:
            return []

    def __read_file(self, file_path):
        self.__pokemons = []
        self.__types = set()
        self.__pokemons_by_type = {}
        with open(file_path) as file:
            pokedex = json.load(file)
        for pokemon in pokedex:
            self.__pokemons.append(Pokemon(pokemon))
            for pkmn_type in pokemon['types']:
                self.__types.add(pkmn_type)
                pokemons = self.__pokemons_by_type.setdefault(pkmn_type, [])
                pokemons.append(Pokemon(pokemon))
        self.__types = sorted(self.__types)
