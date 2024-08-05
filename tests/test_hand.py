import unittest

from pynabi.base import Card
from pynabi.board import HanabiBoard
from pynabi.deck import HanabiDeck
from pynabi.hand import PlayerHand


class TestPlayerHand(unittest.TestCase):
    def setUp(self):
        self.deck = HanabiDeck()
        self.hand = PlayerHand()

    def test_draw_on_empty_hand_is_ok(self):
        # Arrange
        expected_length = 1
        self.assertEqual(0, len(self.hand))

        # Act
        self.hand.draw(self.deck, n_cards=1)
        actual_length = len(self.hand)

        # Assert
        self.assertEqual(expected_length, actual_length)

    def test_draw_on_full_hand_fails(self):
        # Arrange
        expected_length = 5
        self.hand.draw(self.deck, n_cards=5)
        self.assertEqual(expected_length, len(self.hand))

        # Act & Assert
        with self.assertRaises(ValueError):
            self.hand.draw(self.deck, n_cards=1)

        self.assertEqual(expected_length, len(self.hand))

    def test_discard_on_non_empty_hand_is_ok(self):
        # Arrange
        expected_length = 0
        self.hand.draw(self.deck, n_cards=1)
        self.assertEqual(1, len(self.hand))

        # Act
        self.hand.discard(self.deck)
        actual_length = len(self.hand)

        # Assert
        self.assertEqual(expected_length, actual_length)

    def test_discard_on_empty_hand_fails(self):
        # Arrange
        self.assertEqual(0, len(self.hand))

        # Act & Assert
        with self.assertRaises(ValueError):
            self.hand.discard(self.deck)
