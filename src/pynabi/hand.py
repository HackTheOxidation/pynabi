from .base import (
    Card,
    CardColour,
    AbstractBoard,
    AbstractDeck,
    AbstractHand,
    AbstractKnowledgeBase,
)


class PlayerHand(AbstractHand):
    """
    The hand of a player, which may contain at most 5 cards
    at a time.
    """

    def __init__(self):
        self._hand = []

    def draw(self, deck: AbstractDeck, n_cards=1) -> bool:
        """
        Tries to draw n cards from the deck.
        """
        if n_cards + len(self) > 5:
            raise ValueError("Cannot have more than 5 cards at a time!")

        new_cards = [card for _ in range(n_cards) if (card := deck.draw())]
        self._hand += new_cards

        return bool(new_cards)

    def discard(self, deck: AbstractDeck, n_cards: int) -> None:
        """
        Discard card with index n from the hand.
        """
        if n_cards > len(self):
            raise ValueError("Cannot discard more cards than in ones hand!")

        deck.discard(self._hand.pop(n_cards))

    def play_card(self, board: AbstractBoard, card_index: int):
        """
        Plays a card on the board.
        """
        card = self[card_index]

        board.play_card(card)
        del self[card_index]

    def get_hand(self, knowledgebase):
        """
        Displays the players hand based on the knowledge they
          have obtained about it.
        """

        def format_card(knowledge: dict, card: Card) -> str:
            value = str(card.value) if knowledge.get("value", False) else "*"
            colour = str(card.colour) if knowledge.get("colour", False) else "*"
            return f"({value},{colour})"

        return ", ".join(format_card(*x) for x in zip(knowledgebase, self._hand))

    def __iter__(self):
        yield from self._hand

    def __len__(self):
        return len(self._hand)

    def __getitem__(self, index: int) -> Card:
        return self._hand[index]

    def __delitem__(self, index: int):
        del self._hand[index]

    def __str__(self):
        return ", ".join(str(card) for card in self._hand)
