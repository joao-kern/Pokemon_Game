class Pokemon:
    def __init__(self, pokemon):
        self.__name = pokemon["name"]
        self.__type = pokemon["types"]
        self.__weaknesses = pokemon["weaknesses"]
        self.__hp_max = pokemon["hp"]
        self.__hp = self.__hp_max
        self.__attack = pokemon["attack"]
        self.__defense = pokemon["defense"]
        self.__sprite_front = pokemon["sprite_front"]
        self.__sprite_back = pokemon["sprite_back"]
        self.__moves = pokemon["moves"]
    
    def get_name(self):
        return self.__name
    
    def get_type(self):
        return self.__type

    def get_weaknesses(self):
        return self.__weaknesses
    
    def get_hp_max(self):
        return self.__hp_max

    def get_hp(self):
        return self.__hp

    def get_attack(self):
        return self.__attack

    def get_defense(self):
        return self.__defense

    def get_sprite_front(self):
        return self.__sprite_front
    
    def get_sprite_back(self):
        return self.__sprite_back
    
    def get_moves(self):
        return self.__moves
    
    def set_hp(self, damage):
        self.__hp -= damage
        if self.__hp < 0:
            self.__hp = 0

    def restore_hp(self):
        self.__hp = self.__hp_max