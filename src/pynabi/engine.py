from copy import deepcopy
import random
from statistics import fmean
import time
from typing import Type

from .base import (
    Action,
    CardColour,
    HanabiGameState,
    AbstractAIEngine,
    AbstractGame,
    AbstractPlayer,
    PlayerMove,
)

from .algorithms import Node
from .exceptions import GameIsWon, GameIsOver
from .probability import (
    get_possible_cards,
    card_probability,
    potential_score,
)


AIEngineType = Type[AbstractAIEngine]


def create_move(move: tuple | None) -> PlayerMove:
    match move:
        case [Action.PLAY, card_index]:

            def _move(game, player):
                player.play_card(game.board, card_index)
                player.draw(game.deck)

            return _move
        case [Action.DISCARD, card_index]:

            def _move(game, player):
                player.discard(game, card_index)
                player.draw(game.deck)

            return _move
        case [Action.INFO, player_id, int(info)]:

            def _move(game, _):
                game.players[player_id].knowledgebase.reveal_value(info)
                game.board.tokens.use_hint_token()

            return _move

        case [Action.INFO, player_id, CardColour() as info]:

            def _move(game, _):
                game.players[player_id].knowledgebase.reveal_colour(info)
                game.board.tokens.use_hint_token()

            return _move
        case _:
            raise ValueError(f"Cannot construct move from {move}")


class DummyAI(AbstractAIEngine):
    """
    This is a dummy AI, which always decides to discard a random card.

    Honestly, this is more like Artificial Stupidity (AS) rather than AI.
    """

    def __init__(
        self,
        game: AbstractGame,
        player: AbstractPlayer,
    ):
        self._game = game
        self._player = player

    def make_move(self) -> PlayerMove:
        """
        Decides on the 'best' move. This AI always tries to discard a card.
        """

        def _move(game: AbstractGame, player: AbstractPlayer):
            player.discard(game.deck, n_cards=1)
            player.draw(game.deck, n_cards=1)

        return _move

    def selection(self):
        """ """

    def expansion(self, *_):
        """ """

    def simulation(self, *_):
        """ """

    def update(self, *_):
        """ """


class ProbabilisticEngine(AbstractAIEngine):
    """
    An AI that uses a probabilistic heuristic
    to search a (very shallow) tree to select the 'best' move.

    In the spirit of Hanabi, we call this 'The Foggy Fireworker',
    since it tries to make fireworks with limited knowledge
    (it is a pun on 'the fog of war').

    In order to respect partial observability, it does
    not inspect its own hand or the deck like an oracle.
    Rather, it generates all possible cards based on the
    knowledge it has about its own hand and observing the
    cards of the other players along with the discarded/played
    cards.
    """

    def __init__(
        self,
        game: AbstractGame,
        player: AbstractPlayer,
    ):
        self._game = game
        self._player = player

    def make_move(self) -> PlayerMove:
        """
        Decides on the 'best' move.

        This AI uses a probabilistic heuristic.
        """

        best_move = max(self._player.get_legal_moves(self._game), key=self._heurisitic)

        return create_move(best_move)

    def _heurisitic(self, move: tuple) -> float:
        match move:
            case [Action.PLAY, card_index]:
                return self._play_card_heuristic(card_index)
            case [Action.DISCARD, card_index]:
                return self._discard_heuristic(card_index)
            case [Action.INFO, player_id, info] if player_id != self._player.player_id:
                return self._info_heuristic(player_id, info)
            case _:
                return -10.0

    def _play_card_heuristic(self, card_index: int) -> float:
        """
        Calculates the heuristic for playing a card.
        """
        possible_cards = get_possible_cards(self._game, self._player, card_index)
        play_score = self._game.board.play_score
        return fmean(
            [
                prob * play_score(card)
                for card in possible_cards
                if (prob := card_probability(card, possible_cards))
            ]
        )

    def _discard_heuristic(self, card_index: int) -> float:
        """
        Calculates the heuristic for discarding a card.
        """
        tokens = self._game.board.tokens.hint_tokens
        delta_t = 1 if tokens < 8 else 0

        possible_cards = get_possible_cards(self._game, self._player, card_index)
        return delta_t * fmean(
            [
                prob * potential_score(card, self._game, possible_cards)
                for card in possible_cards
                if (prob := card_probability(card, possible_cards))
            ]
        )

    def _info_heuristic(self, player_id: int, info: int | CardColour) -> float:
        """
        Calculates the heuristic for giving information to another player.
        """
        kb = self._game.players[player_id].knowledgebase
        old_knowledge = kb.knowledge()

        kb = deepcopy(kb)
        if isinstance(info, CardColour):
            kb.reveal_colour(info)
        else:
            kb.reveal_value(info)

        return kb.knowledge() - old_knowledge

    def selection(self):
        """ """

    def expansion(self, *_):
        """ """

    def simulation(self, *_):
        """ """

    def update(self, *_):
        """ """
