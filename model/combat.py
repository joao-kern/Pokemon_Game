from random import randint

class Combat:
    def __init__(self, pokemon_trainer, pokemon_bot):
        self.__player_pokemon = pokemon_trainer
        self.__opponet_pokemon = pokemon_bot
        self.__winner = None
    
    def attack(self, attacker, attack, target):
        combat_stats_calc = ((2 * 10 + 10) / 250) * (attacker.get_attack() / target.get_defense())
        damage = attack["damage"] * combat_stats_calc
        for weakness in attack["type"]:
            for type in attacker.get_type():
                if weakness == type:
                    target.set_hp(damage * 2)
                    self.calc_hp()
                    return
        
        target.set_hp(damage)
        self.calc_hp()
    
    def sort_attack(self):
        moves = self.__opponet_pokemon.get_moves()
        x = randint(0, len(moves) - 1)
        return moves[x]
    
    def calc_hp(self):
        if self.__player_pokemon.get_hp() <= 0:
            self.__winner = self.__opponet_pokemon
        elif self.__opponet_pokemon.get_hp() <= 0:
            self.__winner = self.__player_pokemon
    
    def get_winner(self):
        return self.__winner
        