import unittest

from pynabi.base import Card
from pynabi.deck import HanabiDeck


class TestHanabiDeck(unittest.TestCase):
    def setUp(self) -> None:
        self.deck = HanabiDeck(do_shuffle=False)

    def test_number_of_cards_is_correct(self):
        # Arrange
        expected = 45

        # Act
        actual = len(self.deck)

        # Assert
        self.assertEqual(expected, actual, "There are 45 cards in the deck.")

    def test_draw_on_nonempty_deck(self):
        # Arrange
        old_len = len(self.deck)

        # Act
        actual = self.deck.draw()
        new_len = len(self.deck)

        # Assert
        self.assertIsNotNone(actual)
        self.assertLess(new_len, old_len)

    def test_draw_on_empty_deck(self):
        # Arrange
        deck = HanabiDeck()
        deck._cards = []

        # Act
        actual = deck.draw()
        new_len = len(deck)

        # Assert
        self.assertIsNone(actual)
        self.assertEqual(0, new_len)
