from collections import namedtuple, defaultdict
from leaderboard.model import Rank, PlayerRank


Score = namedtuple('Score', 'pseudo kills')
Match = namedtuple('Match', 'scores')


def compute_ranking(match):
    def player_by_kills():
        result = defaultdict(list)
        for score in match.scores:
            result[score.kills].append(score.pseudo)
        return result

    ranking = []
    rank = 1
    for kills, pseudos in sorted(player_by_kills().iteritems(), reverse=True):
        ranking.extend([PlayerRank(pseudo, Rank(rank)) for pseudo in pseudos])
        rank += len(pseudos)
    return ranking
