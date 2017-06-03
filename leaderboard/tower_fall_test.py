import unittest

from tower_fall import Match, Score, compute_ranking
from leaderboard.model import Rank, PlayerRank


class Tests(unittest.TestCase):

    def test_should_rank_on_kills_count(self):
        ranking = compute_ranking(Match(scores=[
            Score(pseudo='jim', kills=8),
            Score(pseudo='jam', kills=10),
            Score(pseudo='jon', kills=2),
            Score(pseudo='mrjmad', kills=0),
        ]))
        self.assertListEqual(ranking, [
            PlayerRank('jam', Rank(1)),
            PlayerRank('jim', Rank(2)),
            PlayerRank('jon', Rank(3)),
            PlayerRank('mrjmad', Rank(4)),
        ])

    def test_should_rank_on_kills_count_with_exaeco(self):
        ranking = compute_ranking(Match(scores=[
            Score(pseudo='jim', kills=8),
            Score(pseudo='jam', kills=10),
            Score(pseudo='jon', kills=8),
            Score(pseudo='mrjmad', kills=0),
        ]))
        self.assertListEqual(ranking, [
            PlayerRank('jam', Rank(1)),
            PlayerRank('jim', Rank(2)),
            PlayerRank('jon', Rank(2)),
            PlayerRank('mrjmad', Rank(4)),
        ])
