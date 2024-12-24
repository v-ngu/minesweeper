from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from board_tile.services import BoardTileService, BoardTileServiceUtils
from game.models import GameDifficulty, Game, GameStatus
from board_tile.models import BoardTile, BoardTileState


class RandomizeMinePositionsTest(TestCase):
    def test_difficulty_easy(self):
        utils = BoardTileServiceUtils(GameDifficulty.EASY)
        mine_positions_map = utils.randomize_mine_positions()
        total_mines = sum(len(y_list) for y_list in mine_positions_map.values())
        self.assertEqual(total_mines, 10)

    def test_difficulty_medium(self):
        utils = BoardTileServiceUtils(GameDifficulty.MEDIUM)
        mine_positions_map = utils.randomize_mine_positions()
        total_mines = sum(len(y_list) for y_list in mine_positions_map.values())
        self.assertEqual(total_mines, 40)

    def test_difficulty_hard(self):
        utils = BoardTileServiceUtils(GameDifficulty.HARD)
        mine_positions_map = utils.randomize_mine_positions()
        total_mines = sum(len(y_list) for y_list in mine_positions_map.values())
        self.assertEqual(total_mines, 99)

    def test_no_duplicates(self):
        utils = BoardTileServiceUtils(GameDifficulty.HARD)
        mine_positions_map = utils.randomize_mine_positions()
        all_positions = set()
        for x, y_list in mine_positions_map.items():
            for y in y_list:
                position = (x, y)
                self.assertNotIn(
                    position, all_positions, f"Found duplicate position {position}"
                )
                all_positions.add(position)


class CalculateAdjacentMinesTest(TestCase):
    def setUp(self):
        """
        Visual representation of the mine positions map:
        [
            [X, X, 0, 0, 0, 0, 0, 0],
            [X, 0, 0, 0, 0, 0, 0, 0],
            [X, 0, X, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        """
        self.utils = BoardTileServiceUtils(GameDifficulty.EASY)
        self.mine_positions_map = {
            0: [0, 1],
            1: [0],
            2: [0, 2],
        }

    def test_no_adjacent_mines(self):
        # Test #1
        tile_position = (3, 4)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 0)

        # Test #2
        tile_position = (5, 5)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 0)

    def test_one_adjacent_mine(self):
        # Test #1
        tile_position = (2, 3)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 1)

        # Test #2
        tile_position = (0, 2)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 1)

    def test_multiple_adjacent_mines(self):
        # Test #1
        tile_position = (1, 1)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 5)

        # Test #2
        tile_position = (2, 1)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 3)

        # Test #3
        tile_position = (3, 1)
        adjacent_mines = self.utils.calculate_adjacent_mines(
            tile_position, self.mine_positions_map
        )
        self.assertEqual(adjacent_mines, 2)


class GetAdjacentTilePositionsTest(TestCase):
    def setUp(self):
        self.utils = BoardTileServiceUtils()

    def test_get_adjacent_tile_positions(self):
        tile_position = (3, 4)
        inspected_tiles_positions = set()
        inspected_tiles_positions.add(tile_position)

        adjacent_tiles = self.utils.get_adjacent_tile_pos(
            tile_position, GameDifficulty.EASY, inspected_tiles_positions
        )
        self.assertEqual(
            adjacent_tiles,
            [(2, 3), (2, 4), (2, 5), (3, 3), (3, 5), (4, 3), (4, 4), (4, 5)],
        )

    def test_get_adjacent_tile_positions_edge(self):
        tile_position = (0, 0)
        inspected_tiles_positions = set()
        inspected_tiles_positions.add(tile_position)

        adjacent_tiles = self.utils.get_adjacent_tile_pos(
            tile_position, GameDifficulty.EASY, inspected_tiles_positions
        )
        self.assertEqual(adjacent_tiles, [(0, 1), (1, 0), (1, 1)])

        tile_position = (0, 3)
        inspected_tiles_positions = set()
        inspected_tiles_positions.add(tile_position)

        adjacent_tiles = self.utils.get_adjacent_tile_pos(
            tile_position, GameDifficulty.EASY, inspected_tiles_positions
        )
        self.assertEqual(adjacent_tiles, [(0, 2), (0, 4), (1, 2), (1, 3), (1, 4)])


class CreateBoardTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create()
        self.service = BoardTileService(GameDifficulty.EASY)
        self.service.create_board(self.game)

    def test_number_of_tiles(self):
        expected_tiles_count = 8 * 8
        actual_tiles_count = BoardTile.objects.filter(game=self.game).count()

        self.assertEqual(
            actual_tiles_count,
            expected_tiles_count,
            f"Expected {expected_tiles_count} tiles, but found {actual_tiles_count}.",
        )

    def test_number_of_mines(self):
        expected_mines_count = 10
        actual_mines_count = BoardTile.objects.filter(game=self.game, value=9).count()
        self.assertEqual(
            actual_mines_count,
            expected_mines_count,
            f"Expected {expected_mines_count} mines, but found {actual_mines_count}.",
        )


class BoardTileViewTests(APITestCase):
    def setUp(self):
        self.game = Game.objects.create(difficulty=GameDifficulty.EASY)
        self.tile = BoardTile.objects.create(
            game=self.game, row=0, column=0, value=5, state=None
        )
        self.url = reverse("board-tile-update-state")

    def test_update_flagged_state(self):
        # Test #1
        data = {
            "game_id": self.game.pk,
            "row": 0,
            "column": 0,
            "state": BoardTileState.FLAGGED,
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["tiles"]), 1)  # type: ignore
        self.tile.refresh_from_db()
        self.assertEqual(self.tile.state, BoardTileState.FLAGGED)
        # Making sure the db is not updated, but the value is not revealed to client
        self.assertEqual(self.tile.value, 5)
        self.assertEqual(response.data["tiles"][0]["value"], -1)  # type: ignore

        # Test #2
        data = {
            "game_id": self.game.pk,
            "row": 0,
            "column": 0,
            "state": None,
        }
        response = self.client.patch(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["tiles"]), 1)  # type: ignore
        self.tile.refresh_from_db()
        self.assertEqual(self.tile.state, None)
        # Making sure the db is not updated, but the value is not revealed to client
        self.assertEqual(self.tile.value, 5)
        self.assertEqual(response.data["tiles"][0]["value"], -1)  # type: ignore


class RevealTileTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(difficulty=GameDifficulty.EASY)
        self.service_utils = BoardTileServiceUtils()

    def create_tile(self, row, column, value, state=None):
        return BoardTile.objects.create(
            game=self.game, row=row, column=column, value=value, state=state
        )

    def test_reveal_bomb(self):
        tiles = [
            self.create_tile(0, 0, 9),  # Bomb
            self.create_tile(0, 1, 9),  # Bomb
            self.create_tile(1, 0, 9, BoardTileState.FLAGGED),  # Bomb with flag
            self.create_tile(1, 1, 0),
        ]

        tiles_revealed, _ = self.service_utils.reveal_tile(tiles[0])

        self.game.refresh_from_db()
        for tile in tiles:
            tile.refresh_from_db()

        self.assertEqual(len(tiles_revealed), 2)
        self.assertEqual(tiles[0].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[1].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[2].state, BoardTileState.FLAGGED)
        self.assertEqual(tiles[3].state, None)
        self.assertEqual(self.game.status, GameStatus.LOST)

    def test_reveal_tile_with_adjacent_mines(self):
        tiles = [
            self.create_tile(0, 0, 9),
            self.create_tile(0, 1, 1),
        ]

        tiles_revealed, _ = self.service_utils.reveal_tile(tiles[1])

        self.game.refresh_from_db()
        for tile in tiles:
            tile.refresh_from_db()

        self.assertEqual(len(tiles_revealed), 1)
        self.assertEqual(tiles[1].state, BoardTileState.REVEALED)
        self.assertEqual(self.game.status, GameStatus.PLAYING)

    def test_reveal_empty_tile(self):
        """
        Visual representation of the mine positions map:
        [
            [0, 0, 2, 0, 0, 2, 0, 0],
            [0, 0, 2, 2, 2, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        """
        tiles = [
            self.create_tile(0, 2, 2),
            self.create_tile(0, 3, 0),
            self.create_tile(0, 4, 0),
            self.create_tile(0, 5, 2),
            self.create_tile(1, 2, 2),
            self.create_tile(1, 3, 2),
            self.create_tile(1, 4, 2),
            self.create_tile(1, 5, 9),
        ]

        tiles_revealed, _ = self.service_utils.reveal_tile(tiles[1])

        self.game.refresh_from_db()
        for tile in tiles:
            tile.refresh_from_db()

        self.assertEqual(len(tiles_revealed), 7)
        self.assertEqual(tiles[0].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[1].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[2].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[3].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[4].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[5].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[6].state, BoardTileState.REVEALED)
        self.assertEqual(tiles[7].state, None)


class CheckVictoryTest(TestCase):
    def setUp(self):
        self.game = Game.objects.create(difficulty=GameDifficulty.EASY)
        self.service = BoardTileServiceUtils()

    def create_tile(self, row, column, value, state=None):
        return BoardTile.objects.create(
            game=self.game, row=row, column=column, value=value, state=state
        )

    def test_check_victory(self):
        self.create_tile(0, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(0, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 1, 1, BoardTileState.REVEALED)

        check_victory = self.service.check_victory(self.game.pk)
        self.assertEqual(check_victory, GameStatus.WON)

    def test_too_many_flags(self):
        self.create_tile(0, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(0, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 1, 1, BoardTileState.FLAGGED)

        check_victory = self.service.check_victory(self.game.pk)
        self.assertEqual(check_victory, None)

    def test_no_state_tiles(self):
        self.create_tile(0, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(0, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 1, 1)

        check_victory = self.service.check_victory(self.game.pk)
        self.assertEqual(check_victory, None)

    def test_unflagged_mines(self):
        self.create_tile(0, 0, 9, BoardTileState.REVEALED)
        self.create_tile(0, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(2, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 0, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 1, 9, BoardTileState.FLAGGED)
        self.create_tile(3, 2, 9, BoardTileState.FLAGGED)
        self.create_tile(1, 1, 1, BoardTileState.FLAGGED)

        check_victory = self.service.check_victory(self.game.pk)
        self.assertEqual(check_victory, None)
