#!/usr/bin/python
"""Leaderboard manager.

Usage:
  leaderboard reset
  leaderboard show
  leaderboard tower <result>...
  leaderboard (-h | --help)
  leaderboard --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
from leaderboard.model import Player, MemoryPlayerRepository, player_rating_updater, Rating, PlayerRank, Rank
from leaderboard.infrastructure import JsonPlayerRepository
from leaderboard.tower_fall import Score, Match, compute_ranking


DATAFILE = "data.json"

def repository():
    return JsonPlayerRepository(DATAFILE)

def reset_leaderboard():
    print "Reseting leaderboard"
    open(DATAFILE, 'w').close()

def show_leaderboard():
    print "Leaderboard :"
    for player in repository().all_players_by_rating():
        print "  %-30s rating: %5d" % (player.pseudo, player.rating.value)

def update_towerfall(result):
    def to_score(result):
        iterator = iter(result)
        while True:
            yield Score(iterator.next(), int(iterator.next()))

    ranking = compute_ranking(Match(list(to_score(result))))
    print "Match ranking :"
    for player_rank in ranking:
        print "  %-30s rank: %2d" % (player_rank.pseudo, player_rank.rank.value)

    print "\nNew player rating :"
    updater = player_rating_updater(repository())
    result = updater(*ranking)
    for pseudo, rating, delta in sorted(result):
        print "  %-30s rating: %5d (%3d)" % (pseudo, rating.value, delta)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Leaderboard manager 1.0')
    if arguments['reset']:
        reset_leaderboard()
    if arguments['show']:
        show_leaderboard()
    elif arguments['tower']:
        update_towerfall(arguments['<result>'])
