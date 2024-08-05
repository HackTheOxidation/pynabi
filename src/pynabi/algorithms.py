import copy
import random
import time
import math
from dataclasses import dataclass, field
from typing import Dict, Union, Self

from .base import (
    HanabiGameState,
    AbstractGame,
    AbstractPlayer,
    PlayerMove,
    Action,
)


@dataclass
class Node:
    move: tuple
    player: AbstractPlayer
    parent: Union[Self, None] = None
    visits: int = 0
    wins: int = 0
    children: Dict[PlayerMove, Self] = field(default_factory=dict)
    constant: float = 1.42

    def add_children(self, children: list) -> None:
        for child in children:
            self.children[child.move] = child

    def ucb_value(self):
        """
        Calculates the UCB value for the current node.
        """
        if self.visits == 0:
            return 0

        winning_ratio = self.wins / self.visits
        visit_ratio = math.sqrt(math.log(self.parent.visits) / self.visits)

        return winning_ratio + self.constant * visit_ratio
