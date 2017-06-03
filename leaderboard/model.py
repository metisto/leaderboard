from collections import namedtuple, defaultdict
import itertools
import math


Player = namedtuple('Player', 'pseudo rating')
PlayerRank = namedtuple('PlayerRank', 'pseudo rank')
Rank = namedtuple('Rank', 'value')
Rating = namedtuple('Rating', 'value')

def default_rating():
    return Rating(1500)

class PlayerRepository(object):
    def find_player_by_pseudo(self, pseudo):
        pass

    def all_players(self):
        pass

    def save(self, player):
        pass


class MemoryPlayerRepository(object):
    def __init__(self, *players):
        self.players = dict(((p.pseudo, p) for p in players))

    def find_player_by_pseudo(self, pseudo):
        if pseudo in self.players:
            return self.players[pseudo]
        else:
            return Player(pseudo, default_rating())

    def all_players_by_rating(self):
        return sorted(
            self.players.values(),
            key=lambda x:x.rating.value,
            reverse=True)

    def save(self, player):
        self.players[player.pseudo] = player



def compute_rating_delta(rating_a, ranking_a, rating_b, ranking_b, player_count):
    def winner_coeficient(rank_a, rank_b):
        if rank_a < rank_b:
            return 1.0
        elif rank_a == rank_b:
            return 0.5
        else:
            return 0.0

    def multiplayer_coeficient(player_count):
        return 32 / (player_count - 1)

    EA = 1 / (1.0 + math.pow(10.0, (rating_b.value - rating_a.value) / 400.0))
    return int(round(multiplayer_coeficient(player_count) * (winner_coeficient(ranking_a, ranking_b) - EA)))


def player_rating_updater(repository):
    player_rating_updater = namedtuple('player_rating_updater', 'player rank')

    def retrieve_players(rankings):
        return [player_rating_updater(repository.find_player_by_pseudo(ranking.pseudo), ranking.rank) for ranking in rankings]

    def update_rating(player, delta):
        return Player(player.pseudo, Rating(player.rating.value + delta))

    def process(*rankings):
        deltas = defaultdict(lambda: 0)
        for a, b in itertools.combinations(retrieve_players(rankings), 2):
            delta = compute_rating_delta(a.player.rating, a.rank, b.player.rating, b.rank, len(rankings))
            deltas[a.player] += delta
            deltas[b.player] -= delta
        result = []
        for player, delta in deltas.iteritems():
            updated_player = update_rating(player, delta)
            repository.save(updated_player)
            result.append((player.pseudo, updated_player.rating, delta))
        return result

    return process
