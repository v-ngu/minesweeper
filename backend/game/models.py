from django.db import models
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from board_tile.models import BoardTile


class GameDifficulty(models.TextChoices):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class GameStatus(models.TextChoices):
    PLAYING = "playing"
    WON = "won"
    LOST = "lost"


class Game(models.Model):
    difficulty = models.CharField(max_length=50, choices=GameDifficulty.choices)
    status = models.CharField(
        max_length=50, choices=GameStatus.choices, default=GameStatus.PLAYING
    )

    # Type hinting for board_tiles
    board_tiles: models.Manager["BoardTile"]
