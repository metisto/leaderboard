import json
from leaderboard.model import Player, default_rating, Rating, sort_player_by_rating


class JsonPlayerRepository(object):
    def __init__(self, filename):
        self.__filename = filename
        self.__data = self.__load()

    def find_player_by_pseudo(self, pseudo):
        if pseudo in self.__data:
            return self.__hydrate(pseudo, self.__data[pseudo])
        else:
            return Player(pseudo, default_rating())

    def all_players_by_rating(self):
        return sort_player_by_rating([self.__hydrate(pseudo, data) for pseudo, data in self.__data.iteritems()])

    def save(self, player):
        self.__data[player.pseudo] = {'rating': player.rating.value}
        self.__save()

    def __hydrate(self, pseudo, data):
        return Player(pseudo, Rating(data['rating']))

    def __load(self):
        try:
            with open(self.__filename, "r") as fp:
                return json.load(fp)
        except ValueError:
            return {}

    def __save(self):
        try:
            with open(self.__filename, "w") as fp:
                return json.dump(self.__data, fp, ensure_ascii=True, indent=True)
        except ValueError:
            return {}
