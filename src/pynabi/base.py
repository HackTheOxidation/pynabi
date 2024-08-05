from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Iterator, List


class CardColour(Enum):
    """
    Representation of a card colour.
    """

    Red = "Red"
    Blue = "Blue"
    Green = "Green"
    Yellow = "Yellow"
    White = "White"

    def __str__(self) -> str:
        match self:
            case CardColour.Red:
                return "Red"
            case CardColour.Blue:
                return "Blue"
            case CardColour.Green:
                return "Green"
            case CardColour.Yellow:
                return "Yellow"
            case CardColour.White:
                return "White"


@dataclass(frozen=True)
class Card:
    """
    A Hanabi card has a numerical value between 1-5,
      and a colour.
    """

    value: int
    colour: CardColour

    def __str__(self) -> str:
        return f"({self.value},{self.colour})"

    def censor(self, show_value=False, show_colour=False) -> str:
        """
        Formats a string representation of the card based on acquired
          knowledge.
        """
        value = self.value if show_value else "*"
        colour = self.colour if show_colour else "*"
        return f"({value},{colour})"


class HanabiGameState(Enum):
    """
    Representation of the game state.
    """

    Starting = "Starting"
    Playing = "Playing"
    Won = "Won"
    Lost = "Lost"


class Action(Enum):
    PLAY = "play"
    DISCARD = "discard"
    INFO = "info"


class AbstractTokens(ABC):
    """
    A collection of all the tokens in the game.

    It is responsible for issueing, consuming and
      reclaiming said tokens.
    """

    @abstractmethod
    def use_hint_token(self):
        """
        Uses a hint token if possible.
        """

    @abstractmethod
    def reclaim_hint_token(self):
        """
        Reclaims a hint token after having discarded a card.
        """

    @abstractmethod
    def use_fuse_token(self):
        """
        Uses a fuse token if a mistake is made.
        """

    @property
    @abstractmethod
    def hint_tokens(self) -> int:
        """
        Getter for the number of hint tokens.
        """

    @property
    @abstractmethod
    def fuse_tokens(self) -> int:
        """
        Getter for the number of fuse tokens.
        """


class AbstractBoard(ABC):
    """
    The board is responsible for the five coloured
      card piles. That is, updating the state of
      the piles correctly whenever a card is played.
    """

    @abstractmethod
    def play_card(self, card: Card):
        """
        Plays a card on this board.
        """

    @abstractmethod
    def calculate_points(self) -> int:
        """
        Calculates the points achieved in the game so far.
        """

    @property
    @abstractmethod
    def tokens(self) -> AbstractTokens:
        """
        Getter for tokens.
        """

    @property
    @abstractmethod
    def played_cards(self) -> List[Card]:
        """
        Gets all cards that have been played on the board.
        """

    @abstractmethod
    def play_score(self, card: Card) -> int:
        """
        Calculates a score for playing a card on this board.
        """

    @abstractmethod
    def __getitem__(self, colour: CardColour) -> int:
        pass


class AbstractDeck(ABC):
    """
    The deck contains a collection of all cards in
      the game. This includes discarded cards.
      The only cards that the deck is not aware
      of are those in the hands of the players.
    """

    @abstractmethod
    def draw(self) -> Card:
        """
        Draws a card from this deck.
        """

    @abstractmethod
    def discard(self, *cards):
        """
        Discards the cards into the discarded pile of this deck.
        """

    @abstractmethod
    def __len__(self) -> int:
        pass

    @property
    @abstractmethod
    def discarded_pile(self) -> list:
        """
        Gets all the cards in the discarded_pile
        """

    @abstractmethod
    def create_deck(self) -> List[Card]:
        """
        Creates a (non-shuffled) standard deck of Hanabi Cards.
        """


class AbstractHand(ABC):
    """
    The hand represents the collection of playable
      cards by some entity participating in the game
      (most likely a player).
    """

    @abstractmethod
    def draw(self, deck: AbstractDeck, n_cards: int):
        """
        Draws n cards from a deck.
        """

    @abstractmethod
    def discard(self, deck: AbstractDeck, n_cards: int):
        """
        Discards a cards with index 'n_cards' from this hand
          and puts it in the deck pile.
        """

    @abstractmethod
    def play_card(self, board: AbstractBoard, card_index: int):
        """
        Plays a card on the board.
        """

    @abstractmethod
    def get_hand(self, knowledgebase) -> str:
        """
        Displays the players hand based on the knowledge they
          have obtained about it.
        """

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> Card:
        pass

    @abstractmethod
    def __iter__(self):
        pass


class AbstractKnowledgeBase(ABC):
    """
    The knowledge base serves as a player's memory about the cards
      currently in their hand.

    The knowledge base also keeps track of the state of the game in
      terms of uncertainty, for example how many green cards are left
      in the game, etc.
    """

    @abstractmethod
    def draw(self, deck: AbstractDeck, n_cards: int):
        """
        Draws n cards from a deck.
        """

    @abstractmethod
    def discard(self, deck: AbstractDeck, n_cards: int):
        """
        Discards n cards from this hand into the deck pile.
        """

    @abstractmethod
    def play_card(self, board: AbstractBoard, card_index: int):
        """
        Plays a card on the board.
        """

    @abstractmethod
    def get_knowledge(self, index: int) -> dict:
        """ """

    @abstractmethod
    def update_knowledge(self, index: int, **new_knowledge):
        """ """

    @abstractmethod
    def remove_knowledge(self, index: int):
        """ """

    @abstractmethod
    def reveal_colour(self, colour: CardColour):
        """ """

    @abstractmethod
    def reveal_value(self, value: int):
        """ """

    @abstractmethod
    def get_hand(self) -> str:
        """
        Displays the players hand based on the knowledge they
          have obtained about it.
        """

    @abstractmethod
    def knowledge(self) -> float:
        """
        Calculates the amount of knowledge/certainty about the
          current hand of cards.
        """

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, index: int) -> dict:
        pass

    @abstractmethod
    def __iter__(self):
        pass

    @property
    @abstractmethod
    def hand(self) -> AbstractHand:
        """"""


class AbstractGame(ABC):
    """ """

    @abstractmethod
    def play(self) -> None:
        """
        Plays the game by letting each player take their turn and
          thus affect the state of the game.
        """

    @abstractmethod
    def calculate_points(self) -> int:
        """
        Calculates the points achieved in the game so far.
        """

    @abstractmethod
    def get_player_indices(self, exclude_id=None):
        """
        Returns a collection of ids for all players in the game.
        """

    @property
    @abstractmethod
    def state(self) -> HanabiGameState:
        """
        Gets the current state of the game.
        """

    @state.setter
    @abstractmethod
    def state(self, new_state: HanabiGameState):
        """
        Sets the current state of the game to new_state.
        """

    @property
    @abstractmethod
    def board(self) -> AbstractBoard:
        """
        Getter for board.
        """

    @property
    @abstractmethod
    def deck(self) -> AbstractDeck:
        """
        Getter for deck.
        """

    @property
    @abstractmethod
    def players(self) -> list:
        """
        Getter for players.
        """

    @property
    @abstractmethod
    def is_last_round(self):
        """
        Abstract property that indicates
        whether the game is in its last round.
        """

    @abstractmethod
    def print_game(self, player_id=None, board=True) -> None:
        """
        Pretty(-ish) prints the state of the game.
        """


class AbstractPlayer(ABC):
    """
    A player is an entity participating in a game.
      The player can make move that are legal according
      to the game rules and thus affect the state of the
      game.
    """

    @abstractmethod
    def take_turn(self, game: AbstractGame):
        """
        Let the player take their turn. This means making a choice
          as to how to affect the state of the game.
        """

    def play_card(self, board, card_index=1):
        self.knowledgebase.play_card(board, card_index)

    def draw(self, deck, n_cards=1) -> bool:
        return self.knowledgebase.draw(deck, n_cards)

    def discard(self, game, n_cards=1) -> None:
        game.board.tokens.reclaim_hint_token()
        self.knowledgebase.discard(game.deck, n_cards)

    def get_hand(self):
        """
        Displays the players hand based on the knowledge they
          have obtained about it.
        """
        return self.knowledgebase.get_hand()

    def get_legal_moves(self, game: AbstractGame) -> Iterator:
        """
        Returns an iterator with all the legal moves that
          a player may make.
        """
        for card_index, _ in enumerate(self.knowledgebase.hand):
            yield (Action.PLAY, card_index)
            yield (Action.DISCARD, card_index)

        if game.board.tokens.hint_tokens:
            for player_index in game.get_player_indices(exclude_id=self.player_id):
                other_player_hand = game.players[player_index].knowledgebase.hand

                for colour in set(card.colour for card in other_player_hand):
                    yield (Action.INFO, player_index, colour)

                for value in set(card.value for card in other_player_hand):
                    yield (Action.INFO, player_index, value)

    @property
    @abstractmethod
    def player_id(self) -> int:
        """
        Getter for player ID.
        """

    @property
    @abstractmethod
    def knowledgebase(self) -> AbstractKnowledgeBase:
        """
        Getter for knowledge base.
        """


# A player move is a higher-order function, which takes a game and
# the knowledge base of a player, and updates the game.
PlayerMove = Callable[[AbstractGame, AbstractPlayer], None]


class AbstractAIEngine(ABC):
    """
    The AI engine serves as a common strategy interface for
      various AI algorithms that can aid a consumer of the
      interface in selecting the next move based on its
      implementation of the strategy.
    """

    @abstractmethod
    def __init__(
        self,
        game: AbstractGame,
        player: AbstractPlayer,
    ):
        pass

    @abstractmethod
    def make_move(self) -> PlayerMove:
        """
        Runs the algorithm to decide the best possible move.

        :returns: A move function that updates the game.
        """

    @abstractmethod
    def selection(self) -> tuple:
        """ """

    @abstractmethod
    def expansion(self, parent, state: AbstractGame) -> bool:
        """ """

    @abstractmethod
    def simulation(self, state: AbstractGame, node):
        """ """

    @abstractmethod
    def update(self, node, outcome: int):
        """ """
