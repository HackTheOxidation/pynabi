from typing import List
from .base import AbstractGame, AbstractPlayer, Card


def _get_known_cards(
    game: AbstractGame,
    player: AbstractPlayer,
    condition=lambda _: True,
) -> list:
    played_cards = [card for card in game.board.played_cards if condition(card)]

    discarded_cards = [card for card in game.deck.discarded_pile if condition(card)]

    other_players = [
        game.players[player_id]
        for player_id in game.get_player_indices(exclude_id=player.player_id)
    ]

    other_players_cards = [
        card
        for player in other_players
        for card in player.knowledgebase.hand
        if condition(card)
    ]

    return played_cards + discarded_cards + other_players_cards


def get_possible_cards(
    game: AbstractGame,
    player: AbstractPlayer,
    card_index: int,
):
    knowledge = player.knowledgebase.get_knowledge(card_index)

    knows_colour = knowledge.get("colour", False)
    knows_value = knowledge.get("value", False)

    if knows_colour and knows_value:
        return [player.knowledgebase.hand[card_index]]

    if knows_colour:
        condition = (
            lambda card: card.colour == player.knowledgebase.hand[card_index].colour
        )
    elif knows_value:
        condition = (
            lambda card: card.value == player.knowledgebase.hand[card_index].value
        )
    else:
        condition = lambda _: True

    possible_cards = [card for card in game.deck.create_deck() if condition(card)]

    known_cards = _get_known_cards(game, player, condition)

    for card in known_cards:
        possible_cards.remove(card)

    return possible_cards


def card_probability(card: Card, possible_cards: List[Card]) -> float:
    return possible_cards.count(card) / len(possible_cards)


def potential_score(
    card: Card,
    game: AbstractGame,
    possible_cards: List[Card],
) -> int:
    if card.value < game.board[card.colour]:
        return 1
    if card.value > game.board[card.colour] and possible_cards.count(card) == 1:
        return -2 if card.value == 5 else -1
    return 0
