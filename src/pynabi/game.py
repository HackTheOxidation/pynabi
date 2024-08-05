import os
from itertools import cycle

from .exceptions import GameIsOver, GameIsWon

from .base import (
    HanabiGameState,
    AbstractDeck,
    AbstractGame,
    AbstractBoard,
)


class InvalidGameState(BaseException):
    """"""


class HanabiGame(AbstractGame):
    def __init__(self, players: list, board, deck):
        self._players = list(players)
        self._state = HanabiGameState.Starting
        self._board = board
        self._deck = deck

    def play(self) -> None:
        """
        Starts the game.
        """

        if self.state != HanabiGameState.Starting:
            raise InvalidGameState(
                f"Invalid game state - Expected 'Starting' state, got: {self.state}"
            )

        self.state = HanabiGameState.Playing

        self._deal_at_startup()

        # Play the game
        last_round_countdown = len(self._players)
        try:
            for player in cycle(self._players):
                self.print_game(player_id=player.player_id)
                player.take_turn(self)

                if self.is_last_round:
                    if last_round_countdown:
                        last_round_countdown -= 1
                    else:
                        self.state = HanabiGameState.Won
                        break

        except GameIsWon:
            self.state = HanabiGameState.Won
        except GameIsOver:
            self.state = HanabiGameState.Lost

        match self.state:
            case HanabiGameState.Won:
                self.print_game()
                print(
                    f"Hurray, you won the game - You got {self.calculate_points()} points"
                )
            case HanabiGameState.Lost:
                self.print_game()
                print("You lost - 0 points for you!")
            case _:
                raise InvalidGameState("Invalid game state")

    def _deal_at_startup(self) -> None:
        """
        Deals each player five cards at game startup.
        """
        for player in self._players:
            player.draw(self._deck, n_cards=5)

    @property
    def is_last_round(self) -> bool:
        """
        Indicates whether the game is in its last round.
        """
        return len(self.deck) == 0

    @property
    def state(self) -> HanabiGameState:
        return self._state

    @state.setter
    def state(self, new_state: HanabiGameState) -> None:
        self._state = new_state

    @property
    def board(self) -> AbstractBoard:
        return self._board

    @property
    def deck(self) -> AbstractDeck:
        return self._deck

    @property
    def players(self) -> list:
        return self._players

    def calculate_points(self) -> int:
        return self.board.calculate_points()

    def get_player_indices(self, exclude_id=None):
        return set(p.player_id for p in self._players if p.player_id != exclude_id)

    def print_game(self, player_id=None, board=True) -> None:
        """
        Pretty(-ish) prints the state of the game.
        """
        os.system("cls" if os.name == "nt" else "clear")

        if board:
            print("The Game:\n")
            print(self.board)
            print(f"Is this the last round? {'Yes' if self.is_last_round else 'No'}")

        for player in filter(lambda p: p.player_id != player_id, self._players):
            print(player)
