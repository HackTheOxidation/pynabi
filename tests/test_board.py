import unittest
from unittest.mock import Mock

from pynabi.base import Card, CardColour
from pynabi.board import HanabiBoard


class TestHanabiBoard(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_tokens = Mock()
        self.board = HanabiBoard(self.mock_tokens)

    def test_all_piles_are_initially_zero(self):
        # Arrange
        expected = 0

        # Act

        # Assert
        for actual in self.board._piles.values():
            self.assertEqual(expected, actual)

    def test_play_valid_card_is_ok(self):
        # Arrange
        card = Card(colour=CardColour.Red, value=1)

        # Act
        self.board.play_card(card)

        # Assert
        self.assertEqual(1, self.board._piles[CardColour.Red])

    def test_play_invalid_card_raises_error(self):
        # Arrange
        card = Card(colour=CardColour.Red, value=5)

        # Act & Assert
        with self.assertRaises(ValueError):
            self.board.play_card(card)

    def test_initial_points_equal_zero(self):
        # Arrange
        expected = 0

        # Act
        actual = self.board.calculate_points()

        # Assert
        self.assertEqual(expected, actual)

    def test_play_valid_card_gives_points(self):
        # Arrange
        value = 1
        card = Card(colour=CardColour.Red, value=value)
        expected = self.board.calculate_points() + value

        # Act
        self.board.play_card(card)
        actual = self.board.calculate_points()

        # Assert
        self.assertEqual(expected, actual)

    def test_play_invalid_card_preserves_points(self):
        # Arrange
        value = 5
        card = Card(colour=CardColour.Red, value=value)
        expected = self.board.calculate_points()

        # Act
        with self.assertRaises(ValueError):
            self.board.play_card(card)

        actual = self.board.calculate_points()

        # Assert
        self.assertEqual(expected, actual)
