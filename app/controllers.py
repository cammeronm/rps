from collections import defaultdict
from typing import Dict, List

import click
import emoji
from enums import CHOICE_TO_EMOJI_MAPPING, PAPER, ROCK, SCISSORS
from oponents import TOpponent


class GameController:

    # Keeping RPS order is mandatory
    RULES = {
        # combination => winning choice
        (ROCK, PAPER, SCISSORS): None,
        (ROCK, None, None): None,
        (None, PAPER, None): None,
        (None, None, SCISSORS): None,
        (ROCK, PAPER, None): PAPER,
        (ROCK, None, SCISSORS): ROCK,
        (None, PAPER, SCISSORS): SCISSORS,
    }

    def evaluate_winner(self, players: List[TOpponent]) -> TOpponent:
        """
        returns the winning opponent
        """
        choices_to_players_map = defaultdict(list)

        for player in players:
            choices_to_players_map[player.make_choice()].append(player)

        self.print_players_choices(choices_to_players_map)

        rule_key = tuple([
            choice_type
            if len(choices_to_players_map.get(choice_type, [])) > 0
            else None for choice_type in (ROCK, PAPER, SCISSORS)
        ])
        winning_choice = GameController.RULES[rule_key]
        if winning_choice is None:
            remaining_players = players
        else:
            remaining_players = choices_to_players_map.pop(winning_choice)

        # Send feedbacks
        self.send_feedback_to_players(remaining_players, winning_choice, is_winner=True)
        for choice, players in choices_to_players_map.items():
            self.send_feedback_to_players(players, choice, is_winner=False)

        if len(remaining_players) > 1:
            return self.evaluate_winner(remaining_players)

        return remaining_players.pop()

    def send_feedback_to_players(self, players: List[TOpponent], choice: str, is_winner: bool):
        for player in players:
            player.set_feedback(choice, is_winner)

    def print_players_choices(self, choices_to_players_map: Dict[str, list]):
        choice_strs = []
        for choice, players in choices_to_players_map.items():
            choice_strs.append(
                f"{emoji.emojize(CHOICE_TO_EMOJI_MAPPING[choice], use_aliases=True)}: "
                f"{', '.join([player.name for player in players])}"
            )
        click.echo(" | ".join(choice_strs))
