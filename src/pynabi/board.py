from typing import List

from .base import CardColour, Card, AbstractTokens, AbstractBoard
from .exceptions import GameIsWon


class HanabiBoard(AbstractBoard):
    def __init__(self, tokens: AbstractTokens) -> None:
        self._piles = {colour: 0 for colour in iter(CardColour)}
        self._tokens = tokens
        self._played_cards: List[Card] = []

    def play_card(self, card: Card):
        match (self._piles[card.colour], card.value):
            case (current, new) if new == current + 1 and new <= 5:
                self._piles[card.colour] = new
            case _:
                self._tokens.use_fuse_token()

        self._played_cards.append(card)

        if self._is_board_complete():
            raise GameIsWon

    def calculate_points(self) -> int:
        """
        Calculates all the points on board.
        """
        return sum(self._piles.values())

    @property
    def tokens(self) -> AbstractTokens:
        return self._tokens

    @property
    def played_cards(self) -> List[Card]:
        return self._played_cards

    def play_score(self, card: Card) -> int:
        """
        Calculates a score for playing a card on this board.
        """
        if self._piles[card.colour] + 1 == card.value:
            return 5 if card.value == 5 else 1

        return -(3 - (self.tokens.fuse_tokens - 1))

    def _is_board_complete(self) -> bool:
        return all(v == 5 for v in self._piles.values())

    def __getitem__(self, colour: CardColour) -> int:
        return self._piles[colour]

    def __str__(self):
        cards_str = "\n".join(
            f"{colour}: {value}" for colour, value in self._piles.items()
        )

        tokens_str = (
            f"\nHint tokens: {self._tokens.hint_tokens}\n"
            f"Fuse tokens: {self._tokens.fuse_tokens}"
        )

        return (
            "---------\n"
            "| Board |\n"
            "---------\n"
            f"{cards_str}\n {tokens_str}\n---------\n"
        )
