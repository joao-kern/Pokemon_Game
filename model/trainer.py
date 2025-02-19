class Trainer:
    def __init__(self, username, password):
        self.__username =  username
        self.__password = password
        self.__battles = 0
        self.__victories = 0
        self.__defeats = 0

    def to_dict(self):
        return {
            "username": self.__username,
            "password": self.__password,
            "battles": self.__battles,
            "victories": self.__victories,
            "defeats": self.__defeats
        }