from django.db import models
from django.db.models import UniqueConstraint


class BoardTileState(models.TextChoices):
    REVEALED = "revealed"
    FLAGGED = "flagged"


class BoardTile(models.Model):
    game = models.ForeignKey(
        "game.Game", on_delete=models.CASCADE, related_name="board_tiles"
    )
    row = models.IntegerField()
    column = models.IntegerField()
    value = models.IntegerField()  # 9 if mine, 0-8 if not mine
    state = models.CharField(
        max_length=50,
        choices=BoardTileState.choices,
        null=True,
        blank=True,
        db_index=True,
    )

    class Meta:
        constraints = [
            UniqueConstraint(
                fields=["game", "row", "column"], name="unique_game_row_column"
            )
        ]

    @staticmethod
    def get_flagged_count(game_id: int):
        return BoardTile.objects.filter(
            game_id=game_id, state=BoardTileState.FLAGGED
        ).count()

    @staticmethod
    def handle_value_visibility(tile):
        """
        If tile is flagged or hidden, set value to -1 so the real value is not revealed
        """
        if tile.state == BoardTileState.FLAGGED or tile.state is None:
            tile.value = -1
            # !!! IMPORTANT !!!
            # The tile's value is set to -1, but it is not saved to the database.
            # Ensure no save() method is called on this tile instance.
