import random
from collections import defaultdict
from .serializers import TileUpdatesSerializer
from game.models import Game, GameDifficulty, GameStatus
from board_tile.models import BoardTile, BoardTileState
from dataclasses import dataclass
from django.db import transaction
from django.db.models import Q
from functools import reduce
from operator import or_


@dataclass
class DifficultyConfig:
    board_size: tuple
    mines_count: int


MinePositionMap = dict[int, list[int]]
difficulty_configs = {
    GameDifficulty.EASY: DifficultyConfig(board_size=(8, 8), mines_count=10),
    GameDifficulty.MEDIUM: DifficultyConfig(board_size=(16, 16), mines_count=40),
    GameDifficulty.HARD: DifficultyConfig(board_size=(16, 30), mines_count=99),
}


class BoardTileService:
    def __init__(self, difficulty: GameDifficulty | None = None):
        self.utils = BoardTileServiceUtils(difficulty)

    def create_board(self, game):
        if not self.utils.board_size:
            raise ValueError("Board size is not set")

        board_size = self.utils.board_size
        mine_positions = self.utils.randomize_mine_positions()

        tiles = []
        for x in range(board_size[0]):
            for y in range(board_size[1]):
                tile_value = (
                    9
                    if x in mine_positions and y in mine_positions[x]
                    else self.utils.calculate_adjacent_mines((x, y), mine_positions)
                )
                tiles.append(BoardTile(game=game, row=x, column=y, value=tile_value))

        BoardTile.objects.bulk_create(tiles)

    def update_tile_state(
        self, tile: BoardTile, new_state: BoardTileState, game_id: int
    ):
        if new_state == BoardTileState.FLAGGED or new_state == None:
            tile.state = new_state
            tile.save()
            tile.refresh_from_db()
            BoardTile.handle_value_visibility(tile)
            response_data = {
                "tiles": [tile],
                "flags_count": BoardTile.get_flagged_count(game_id),
            }
            return TileUpdatesSerializer(response_data)

        elif new_state == BoardTileState.REVEALED:
            tiles, game_status = self.utils.reveal_tile(tile)

            response_data = {
                "tiles": tiles,
                "flags_count": BoardTile.get_flagged_count(game_id),
                "game_status": (
                    game_status if game_status else self.utils.check_victory(game_id)
                ),
            }
            return TileUpdatesSerializer(response_data)


class BoardTileServiceUtils:
    def __init__(self, difficulty: GameDifficulty | None = None):
        if difficulty:
            self.config = difficulty_configs[difficulty]
            self.board_size = self.config.board_size
        else:
            self.config = None
            self.board_size = None

    def calculate_adjacent_mines(
        self, tile_position: tuple[int, int], mine_positions_map: MinePositionMap
    ) -> int:
        x, y = tile_position
        adjacent_mines = 0

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbor_x = x + x_offset
                neighbor_y = y + y_offset

                if (
                    neighbor_x in mine_positions_map
                    and neighbor_y in mine_positions_map[neighbor_x]
                ):
                    adjacent_mines += 1

        return adjacent_mines

    def check_victory(self, game_id: int):
        game = Game.objects.get(id=game_id)
        difficulty = GameDifficulty(game.difficulty)
        self.config = difficulty_configs[difficulty]
        number_of_mines = self.config.mines_count
        tiles = game.board_tiles.all()

        no_states_count = tiles.filter(state__isnull=True).count()
        if no_states_count > 0:
            return None

        unflagged_mines_count = (
            tiles.filter(value=9).exclude(state=BoardTileState.FLAGGED).count()
        )
        if unflagged_mines_count > 0:
            return None

        flags_count = tiles.filter(state=BoardTileState.FLAGGED).count()
        if flags_count != number_of_mines:
            return None

        game.status = GameStatus.WON
        game.save()
        game.refresh_from_db()

        return game.status

    def randomize_mine_positions(self) -> MinePositionMap:
        if not self.config or not self.board_size:
            raise ValueError("Difficulty config is not set")

        number_of_mines = self.config.mines_count

        positions = set()
        x_to_y_map = defaultdict(list)

        while len(positions) < number_of_mines:
            new_pos = (
                random.randint(0, self.board_size[0] - 1),
                random.randint(0, self.board_size[1] - 1),
            )

            if new_pos not in positions:
                positions.add(new_pos)
                x_to_y_map[new_pos[0]].append(new_pos[1])

        return x_to_y_map

    def get_adjacent_tile_pos(
        self,
        tile_position: tuple[int, int],
        game_difficulty: GameDifficulty,
        inspected_tiles_positions: set[tuple[int, int]],
    ) -> list[tuple[int, int]]:
        x, y = tile_position
        board_size = difficulty_configs[game_difficulty].board_size
        positions = []

        for x_offset in range(-1, 2):
            for y_offset in range(-1, 2):
                neighbor_x = x + x_offset
                neighbor_y = y + y_offset

                # Check if the neighbor is within the bounds of the board
                if (
                    0 <= neighbor_x < board_size[0]
                    and 0 <= neighbor_y < board_size[1]
                    and (neighbor_x, neighbor_y) not in inspected_tiles_positions
                ):
                    positions.append((neighbor_x, neighbor_y))

        return positions

    def reveal_tile(self, tile: BoardTile):
        tiles_list = set()
        game_status = None

        game_id = tile.game.id
        game = Game.objects.get(id=game_id)

        # Handle mine tile
        if tile.value == 9:
            with transaction.atomic():
                game.status = GameStatus.LOST
                game.save()
                game.refresh_from_db()

                updated_tiles = BoardTile.objects.filter(
                    game_id=game_id, value=9
                ).exclude(state=BoardTileState.FLAGGED)
                updated_tiles.update(state=BoardTileState.REVEALED)

                game_status = game.status
                tiles_list.update(updated_tiles)

        # Handle non-mine tile
        if tile.value < 9:
            tile.state = BoardTileState.REVEALED
            tile.save()
            tile.refresh_from_db()
            tiles_list.add(tile)

        # Handle empty tile
        if tile.value == 0:
            inspected_tiles_positions = set()
            tile_position = (tile.row, tile.column)
            inspected_tiles_positions.add(tile_position)

            adjacent_tiles_positions = self.get_adjacent_tile_pos(
                tile_position,
                GameDifficulty(game.difficulty),
                inspected_tiles_positions,
            )

            base_q_condition = Q(game_id=game_id, state__isnull=True)
            q_conditions = [
                base_q_condition & Q(row=pos[0], column=pos[1]) & ~Q(value=9)
                for pos in adjacent_tiles_positions
            ]

            adjacent_tiles = BoardTile.objects.filter(reduce(or_, q_conditions))
            mines = [tile for tile in adjacent_tiles if tile.value == 9]

            if len(mines) == 0:
                for tile in adjacent_tiles:
                    revealed_tiles, _ = self.reveal_tile(tile)
                    tiles_list.update(revealed_tiles)

        return tiles_list, game_status
