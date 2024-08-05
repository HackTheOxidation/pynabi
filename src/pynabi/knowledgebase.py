from .base import (
    CardColour,
    AbstractKnowledgeBase,
    AbstractHand,
    AbstractDeck,
    AbstractBoard,
)


class KnowledgeBase(AbstractKnowledgeBase):
    def __init__(self, hand: AbstractHand):
        self._hand = hand
        self._cards: list = [{"colour": False, "value": False} for _ in hand]

    def draw(self, deck: AbstractDeck, n_cards: int) -> bool:
        """
        Draws n cards from a deck.
        """
        for _ in range(n_cards):
            self._cards.append({"colour": False, "value": False})

        return self._hand.draw(deck, n_cards)

    def discard(self, deck: AbstractDeck, n_card: int):
        """
        Discards card with the index n from this hand into the deck pile.
        """
        discarded_card = self._hand.discard(deck, n_card)
        del self._cards[n_card]
        # Optionally, reveal the discarded card to the player
        print(f"You have discarded: {discarded_card}")
        return discarded_card

    def play_card(self, board: AbstractBoard, card_index: int):
        """
        Plays a card on the board.
        """
        self._hand.play_card(board, card_index)
        del self._cards[card_index]

    def get_knowledge(self, index: int) -> dict:
        if index not in range(len(self._cards)):
            raise ValueError("Invalid index - out of bounds.")

        return self._cards[index]

    def update_knowledge(self, index: int, **new_knowledge):
        if index not in range(len(self._cards)):
            raise ValueError("Invalid index - out of bounds.")

        self._cards[index] |= new_knowledge

    def remove_knowledge(self, index: int):
        if index not in range(len(self._cards)):
            raise ValueError("Invalid index - out of bounds.")

        del self._cards[index]

    def reveal_colour(self, colour: CardColour):
        for i, card in enumerate(self._hand):
            if card.colour == colour:
                self.update_knowledge(i, colour=True)

    def reveal_value(self, value: int):
        for i, card in enumerate(self._hand):
            if card.value == value:
                self.update_knowledge(i, value=True)

    def knowledge(self) -> float:
        def _acc(k: dict) -> int:
            return int(k.get("colour", 0)) + int(k.get("value", 0))

        return sum(map(_acc, self)) / len(self)

    def get_hand(self):
        """
        Displays the players hand based on the knowledge they
          have obtained about it.
        """
        return self._hand.get_hand(self)

    def __len__(self) -> int:
        return len(self._cards)

    def __getitem__(self, index: int) -> dict:
        return self._cards[index]

    def __iter__(self):
        yield from self._cards

    @property
    def hand(self) -> AbstractHand:
        """"""
        return self._hand
