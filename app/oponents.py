from typing import Optional, TypeVar

import click
import random
from faker import Faker

from enums import ROCK, PAPER, SCISSORS


class BaseOpponent:

    def __init__(self, name: Optional[str] = None, **kwargs):
        self.name: str = name or Faker().name()

    def set_feedback(self, my_choice, is_winner):
        pass

    def make_choice(self):
        raise NotImplemented


class LuckyOpponent(BaseOpponent):
    def make_choice(self):
        return random.choice((ROCK, PAPER, SCISSORS))


class SmartOpponent(BaseOpponent):

    KEEPER = "keeper"
    LUCKY = "lucky"
    NO_REPEAT = "no_repeat"

    STRATEGIES = {
        KEEPER: (3, 5),
        LUCKY: (1, 2),
        NO_REPEAT: (4, 6)
    }

    def __init__(self, verbose: bool = False, **kwargs):
        super().__init__(**kwargs)
        click.echo("verbose %s" % verbose)
        self.reveal_strategy: bool = verbose
        self.current_strategy: Optional[str] = SmartOpponent.LUCKY
        self.strategy_remaining_rounds_num: Optional[int] = 0
        self.set_new_strategy()
        self.last_choice: Optional[str] = None

    def make_choice(self):
        if self.strategy_remaining_rounds_num == 0:
            self.set_new_strategy()
        choice_func = getattr(self, f"make_{self.current_strategy}_choice")
        choice = choice_func()
        self.strategy_remaining_rounds_num -= 1
        return choice

    def make_keeper_choice(self) -> str:
        if self.last_choice is not None:
            return self.last_choice
        return self.make_lucky_choice()

    def make_lucky_choice(self) -> str:
        return random.choice((ROCK, PAPER, SCISSORS))

    def make_no_repeat_choice(self):
        try:
            next_choices = {ROCK, PAPER, SCISSORS}
            next_choices.remove(self.last_choice)
            return random.choice(list(next_choices))
        except KeyError:
            return self.make_lucky_choice()

    def set_feedback(self, my_choice: str, is_winner: bool):
        self.last_choice = my_choice

    def set_new_strategy(self):
        self.current_strategy, rounds_count_range = random.choice(list(SmartOpponent.STRATEGIES.items()))
        self.strategy_remaining_rounds_num = random.randrange(*rounds_count_range)
        if self.reveal_strategy:
            click.secho(
                f"Now I'll use the {self.current_strategy} strategy "
                f"for next {self.strategy_remaining_rounds_num} rounds. HAHA!", fg="red"
            )


class HumanOpponent(BaseOpponent):
    """
    This opponent is handled by human. Choice is made by CLI enter.
    """
    CHOICES = (ROCK, PAPER, SCISSORS)

    def make_choice(self):
        return click.prompt(
            "Make a choice:",
            default=random.choice(HumanOpponent.CHOICES),
            type=click.Choice(HumanOpponent.CHOICES)
        )


class NetworkHumanOpponent(BaseOpponent):
    # FIXME to be implemented
    pass


TOpponent = TypeVar('TOpponent', bound=BaseOpponent)
