from .base import AbstractTokens
from .exceptions import GameIsOver


class HanabiTokens(AbstractTokens):
    def __init__(self) -> None:
        self._hint_tokens = 8
        self._fuse_tokens = 3

    def use_hint_token(self):
        """
        Uses a hint token if possible.
        """
        if self._hint_tokens <= 0:
            return False

        print("Hint token was used!")
        self._hint_tokens -= 1
        return True

    def reclaim_hint_token(self):
        """
        Reclaims a hint token after having discarded a card.
        """
        if self._hint_tokens < 8:
            print("Hint token was reclaimed!")
            self._hint_tokens += 1
        else:
            print(
                "You already have the maximum amount of hint tokens. No hint token was added."
            )

    def use_fuse_token(self):
        """
        Uses a fuse token if a mistake is made.
        """
        print("The fuse is lit and it is getting shorter!")
        self._fuse_tokens -= 1
        if self._fuse_tokens <= 0:
            print("KABOOM!!!")
            raise GameIsOver

    @property
    def hint_tokens(self) -> int:
        return self._hint_tokens

    @property
    def fuse_tokens(self) -> int:
        return self._fuse_tokens
