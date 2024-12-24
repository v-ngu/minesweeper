from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Game, GameDifficulty
from board_tile.models import BoardTile, BoardTileState


class GameViewTests(APITestCase):
    def test_create_new_game(self):
        url = reverse("game-list")
        data = {"difficulty": GameDifficulty.EASY.value}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Game.objects.get().difficulty, GameDifficulty.EASY)
        self.assertEqual(Game.objects.count(), 1)
        self.assertEqual(BoardTile.objects.count(), 64)


class GameTilesTests(APITestCase):
    def setUp(self):
        self.game = Game.objects.create(difficulty=GameDifficulty.EASY)

        for row in range(8):
            for column in range(8):
                if column == 0:
                    state = BoardTileState.REVEALED
                elif column == 1:
                    state = BoardTileState.FLAGGED
                else:
                    state = None

                BoardTile.objects.create(
                    game=self.game,
                    row=row,
                    column=column,
                    value=0,
                    state=state,
                )

    def test_get_game_tiles(self):
        url = reverse("game-get-game-board", kwargs={"pk": self.game.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        total_count = sum(len(v) for v in response.data["tiles_by_row"].values())  # type: ignore
        self.assertEqual(total_count, 16)
        self.assertEqual(response.data["flags_count"], 8)  # type: ignore
