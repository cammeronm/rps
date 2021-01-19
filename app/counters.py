from typing import List

import click
from oponents import TOpponent


class ScoreCounter:

    def __init__(self, players: List[TOpponent]):
        self.round_count = 0
        self.score = {player: 0 for player in players}

    def update_score(self, winner):
        self.score[winner] += 1
        self.round_count += 1
        self.print_score_inline()

    def print_score_inline(self):
        score_str = ", ".join([f"{player.name}: {score}" for player, score in self.score.items()])
        click.echo(score_str)
