import sys

from .base import AbstractPlayer
from .board import HanabiBoard
from .deck import HanabiDeck
from .game import HanabiGame
from .hand import PlayerHand
from .knowledgebase import KnowledgeBase
from .player import HumanPlayer, AIPlayer
from .tokens import HanabiTokens


def format_welcome_message() -> str:
    """
    Creates a fancy welcome message!
    """
    return (
        "Welcome to: \n"
        " __    __                                __        __ \n"
        "/  |  /  |                              /  |      /  |\n"
        "$$ |  $$ |  ______   _______    ______  $$ |____  $$/ \n"
        "$$ |__$$ | /      \\ /       \\  /      \\ $$      \\ /  |\n"
        "$$    $$ | $$$$$$  |$$$$$$$  | $$$$$$  |$$$$$$$  |$$ |\n"
        "$$$$$$$$ | /    $$ |$$ |  $$ | /    $$ |$$ |  $$ |$$ |\n"
        "$$ |  $$ |/$$$$$$$ |$$ |  $$ |/$$$$$$$ |$$ |__$$ |$$ |\n"
        "$$ |  $$ |$$    $$ |$$ |  $$ |$$    $$ |$$    $$/ $$ |\n"
        "$$/   $$/  $$$$$$$/ $$/   $$/  $$$$$$$/ $$$$$$$/  $$/ \n\n"
        "a cooperative game of fireworks."
    )


def prompt_players() -> int:
    n_players = 0

    while n_players < 3 or n_players > 5:
        try:
            from_user = input("How many will be playing the game [3-5]: ")
            if from_user and from_user.isdigit():
                n_players = int(from_user)
            else:
                print("Nah, that can't be quite right. Try again...")
        except KeyboardInterrupt:
            sys.exit(-1)

    return n_players


def create_players(n_players: int) -> list[AbstractPlayer]:
    def _create_player(player_id: int) -> AbstractPlayer:
        while True:
            try:
                from_user = input(
                    f"Shall I, the computer, be in control of player {player_id}? [y/n]: "
                ).lower()

                match from_user:
                    case "y" | "yes":
                        return AIPlayer(player_id, KnowledgeBase(PlayerHand()))
                    case "n" | "no":
                        return HumanPlayer(player_id, KnowledgeBase(PlayerHand()))
                    case _:
                        print("Nah, that can't be quite right. Try again...")
            except KeyboardInterrupt:
                sys.exit(-1)

    return [_create_player(player_id) for player_id in range(n_players)]


def main() -> None:
    print(format_welcome_message())

    n_players = prompt_players()

    players = create_players(n_players)

    tokens = HanabiTokens()
    board = HanabiBoard(tokens)
    deck = HanabiDeck()

    hanabi = HanabiGame(players=players, board=board, deck=deck)

    try:
        hanabi.play()
    except KeyboardInterrupt:
        print("Someone quit the game...")
        sys.exit(-1)


if __name__ == "__main__":
    main()
