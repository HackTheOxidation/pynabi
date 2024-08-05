from itertools import product
from random import shuffle
from typing import List

from .base import Card, CardColour


class HanabiDeck:
    """
    A standard Hanabi Deck contains the following distribution of cards:

    - 2 x Values 1-4 for all five colors
    - 1 x Value 5 for all five colors

    That is, there are 45 cards in total.
    """

    def __init__(self, do_shuffle=True):
        cards = self.create_deck()

        if do_shuffle:
            shuffle(cards)

        self._cards = list(cards)
        self._discarded = []

    def create_deck(self) -> List[Card]:
        """
        Creates a (non-shuffled) standard deck of Hanabi Cards.
        """
        fives = list(product((5,), iter(CardColour)))
        ones_to_fours = list(product(range(1, 5), iter(CardColour)))
        all_cards = 2 * ones_to_fours + fives
        return [Card(value=value, colour=colour) for value, colour in all_cards]

    def __iter__(self):
        yield from self._cards

    def __len__(self):
        return len(self._cards)

    def draw(self):
        """
        Try drawing a card from the deck.
        """
        return self._cards.pop() if self._cards else None

    def discard(self, *cards):
        self._discarded += list(cards)

    @property
    def discarded_pile(self) -> list:
        return self._discarded
