import json
from leaderboard.model import Player, default_rating, Rating


class JsonPlayerRepository(object):
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__load()

    def find_player_by_pseudo(self, pseudo):
        if pseudo in self.__data:
            return Player(pseudo, Rating(self.__data[pseudo]['rating']))
        else:
            return Player(pseudo, default_rating())

    def all_players_by_rating(self):
        return sorted(
            [Player(pseudo, Rating(data['rating'])) for pseudo, data in self.__data.iteritems()],
            key=lambda x:x.rating.value,
            reverse=True)

    def save(self, player):
        self.__data[player.pseudo] = {'rating': player.rating.value }
        self.__save()

    def __load(self):
        try:
            with file(self.__filename, "r") as fp:
                return json.load(fp)
        except ValueError:
            return {}

    def __save(self):
        try:
            with file(self.__filename, "w") as fp:
                return json.dump(self.__data, fp, ensure_ascii=True, indent=True)
        except ValueError:
            return {}
