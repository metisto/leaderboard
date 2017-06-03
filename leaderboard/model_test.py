import unittest

from leaderboard.model import Rank, Rating, compute_rating_delta


class Tests(unittest.TestCase):

    def test_compute_rating_delta_for_two_players(self):
        self.assertEqual(
            compute_rating_delta(Rating(2000), Rank(1), Rating(1500), Rank(2), 2),
            2
        )
        self.assertEqual(
            compute_rating_delta(Rating(1500), Rank(1), Rating(2000), Rank(2), 2),
            30
        )

    def test_compute_rating_delta_for_three_players(self):
        self.assertEqual(
            compute_rating_delta(Rating(2000), Rank(1), Rating(1500), Rank(2), 3),
            1
        )
        self.assertEqual(
            compute_rating_delta(Rating(1500), Rank(1), Rating(2000), Rank(2), 3),
            15
        )
