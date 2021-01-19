import atexit
from typing import List

from faker import Faker

import click

from oponents import LuckyOpponent, SmartOpponent, HumanOpponent, TOpponent
from controllers import GameController
from counters import ScoreCounter

LUCKY_OPPONENT = "Lucky"
SMART_OPPONENT = "Smart"

AVAILABLE_OPPONENT_TYPES = {
    LUCKY_OPPONENT: LuckyOpponent,
    SMART_OPPONENT: SmartOpponent,
}


def prepare_players(
        number_of_computers: int = 1,
        use_smart_opponent: bool = True,
        verbose_opponents: bool = False,
) -> List[TOpponent]:
    player_name = click.prompt(
        "Type your name:",
        default=Faker().name(),
        type=str,
    )
    players = [HumanOpponent(name=player_name), ]
    opponent_class = SmartOpponent if use_smart_opponent else LuckyOpponent
    players += [opponent_class(verbose=verbose_opponents) for _ in range(number_of_computers)]
    return players


@click.command()
@click.option(
    "--opponent-type", "-o",
    type=click.Choice([LUCKY_OPPONENT, SMART_OPPONENT], case_sensitive=False),
    default=SMART_OPPONENT,
)
@click.option(
    "--number-of-computers", "-n",
    type=click.IntRange(1, 6),
    default=1,
)
@click.option(
    "--verbose-opponents", "-v",
    type=bool,
    default=False,
    is_flag=True,
)
def run(opponent_type: str, number_of_computers: int, verbose_opponents: bool):
    """
    Simple RPS game.
    This version supports only one human player, which would be you, and one computer's opponent of your chosen type.
    Enjoy the game!
    """
    players = prepare_players(
        number_of_computers=number_of_computers,
        use_smart_opponent=opponent_type == SMART_OPPONENT,
        verbose_opponents=verbose_opponents,
    )
    controller = GameController()
    score_counter = ScoreCounter(players)

    @atexit.register
    def end_game():
        click.echo("The final score is:")
        score_counter.print_score_inline()
        click.echo("Thanks for the game!")

    while True:
        winner = controller.evaluate_winner(players)
        click.echo(click.style(f"This round wins {winner.name}", fg="green"))
        score_counter.update_score(winner)


if __name__ == '__main__':
    run()
