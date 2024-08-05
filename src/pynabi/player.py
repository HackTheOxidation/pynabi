from .base import (
    HanabiGameState,
    AbstractGame,
    AbstractKnowledgeBase,
    AbstractHand,
    AbstractPlayer,
    CardColour,
)

from .engine import AIEngineType, DummyAI, ProbabilisticEngine


class HumanPlayer(AbstractPlayer):
    def __init__(
        self,
        player_id: int,
        knowledgebase: AbstractKnowledgeBase,
    ) -> None:
        self._player_id = int(player_id)
        self._knowledgebase = knowledgebase

    def take_turn(self, game: AbstractGame) -> None:
        print(f"Player: {self.player_id} - It's your turn!")

        print(self.get_hand())

        limit = self._print_choices(game.board.tokens.hint_tokens) + 1

        # Display options for the player
        # Get the player's choice
        match self._read_choice(
            "Choose your next step: ",
            "Invalid choice. Please try again.",
            valid_choices=set(range(1, limit)),
        ):
            case 1:  # Play a card
                card_to_play_index = self._read_choice(
                    "Which card would you like to play? (index): ",
                    f"Oops! Invalid card index (should be between 1-{len(self.knowledgebase.hand)}). Please try again.",
                    valid_choices=set(range(1, len(self.knowledgebase.hand) + 1)),
                )
                self.play_card(game.board, card_to_play_index - 1)
                self.draw(game.deck, 1)

            case 2:  # Discard a card
                card_to_discard_index = self._read_choice(
                    "Which card would you like to discard? (index): ",
                    f"Oops! Invalid card index (should be between 1-{len(self.knowledgebase.hand)}). Please try again.",
                    valid_choices=set(range(1, len(self.knowledgebase.hand) + 1)),
                )
                self.discard(game, card_to_discard_index - 1)
                self.draw(game.deck, 1)

            case 3:  # Give information to another player.
                print("The cards of other players:")
                game.print_game(player_id=self.player_id, board=False)

                # Select a player to give information to.
                player_ids = game.get_player_indices(exclude_id=self.player_id)
                print(
                    "Which player would you like to give a hint for?\n"
                    f"Write the index of the player ({player_ids})"
                )
                player_index = self._read_choice(
                    "Index of the player: ",
                    "Invalid player index. Try again",
                    valid_choices=player_ids,
                )

                other_player = game.players[player_index]

                # Select the type of information to give (Colour or Value).
                info_type = self._read_choice(
                    "What type of hint would you like to give? (colour: 1/value: 2): ",
                    "Invalid choice for value or colour. Try again",
                    valid_choices={1, 2},
                )

                match info_type:
                    case 1:
                        colour_list = list(
                            set(card.colour for card in other_player.knowledgebase.hand)
                        )
                        colour_text = "\n".join(
                            f"{i}: {str(c)}" for i, c in enumerate(colour_list)
                        )

                        colour_index = self._read_choice(
                            f"Which colour would you like to reveal?\n{colour_text}\nEnter index: ",
                            "Invalid colour. Try again",
                            valid_choices=set(i for i, _ in enumerate(colour_list)),
                        )

                        colour = colour_list[colour_index]
                        other_player.knowledgebase.reveal_colour(colour)
                    case 2:
                        valid_choices = set(
                            card.value for card in other_player.knowledgebase.hand
                        )
                        value = self._read_choice(
                            f"Which value would you like to hint?\nEnter a value among {valid_choices}: ",
                            "Invalid value. Try again",
                            valid_choices=valid_choices,
                        )
                        other_player.knowledgebase.reveal_value(value)
                    case _:
                        print(f"Wonky choice: {info_type}")
                game.board.tokens.use_hint_token()
            case _:
                pass

    def get_hand(self):
        return self.knowledgebase.get_hand()

    def _read_choice(
        self,
        prompt: str,
        error_text: str,
        valid_choices={1, 2, 3, 4, 5},
    ):
        choice = None
        while choice not in valid_choices:
            from_user = input(prompt)
            if from_user and from_user.isdigit():
                choice = int(from_user)
            else:
                print(error_text)
        return choice

    def _print_choices(self, tokens_left: int = 0) -> int:
        print("Options:")
        print("1: Play a card")
        print("2: Discard a card")

        if tokens_left:
            print("3: Give a hint")

        return 3 if tokens_left else 2

    @property
    def knowledgebase(self) -> AbstractKnowledgeBase:
        return self._knowledgebase

    @property
    def player_id(self) -> int:
        return self._player_id

    def __str__(self) -> str:
        hand = self.get_hand()
        return (
            f"HumanPlayer: {self._player_id}\n"
            f"All cards: {self.knowledgebase.hand}\n"
            f"Known cards: {hand}\n"
        )


class AIPlayer(AbstractPlayer):
    def __init__(
        self,
        player_id: int,
        knowledgebase: AbstractKnowledgeBase,
        ai_engine_type: AIEngineType = ProbabilisticEngine,
    ) -> None:
        self._player_id = int(player_id)
        self._knowledgebase = knowledgebase
        self._ai_engine_type = ai_engine_type

    def take_turn(self, game: AbstractGame) -> None:
        print(f"Player: {self.player_id} - It's your turn!")

        self.get_hand()

        # This is where we build the AI engine.
        ai_engine = self._ai_engine_type(game, self)
        move = ai_engine.make_move()

        move(game, self)

    def get_hand(self):
        return self.knowledgebase.get_hand()

    @property
    def player_id(self) -> int:
        return self._player_id

    @property
    def knowledgebase(self) -> AbstractKnowledgeBase:
        return self._knowledgebase

    def __str__(self) -> str:
        hand = self.get_hand()
        return (
            f"AIPlayer: {self._player_id}\n"
            f"All cards: {self.knowledgebase.hand}\n"
            f"Known cards: {hand}\n"
        )
