import { BoardTile } from "../../../api/fetchGameBoard";
import { BoardSize } from "../GameBoard";

/**
 * Show the busy tiles on the board.
 * A busy tile is one that is already revealed or flagged.
 */
export function arrangeTiles(
  boardSize: BoardSize,
  busyTilesByRow: Record<number, BoardTile[]>
) {
  const board: BoardTile[] = [];
  for (let row = 0; row < boardSize.rows; row++) {
    for (let col = 0; col < boardSize.columns; col++) {
      const busyRow = busyTilesByRow[row];

      if (!busyRow) {
        board.push(getAvailableTile(row, col));
        continue;
      }

      const busyTile = busyRow.find((tile) => tile.column === col);
      const tile = busyTile ?? getAvailableTile(row, col);
      board.push(tile);
    }
  }
  return board;
}

function getAvailableTile(row: number, column: number): BoardTile {
  return { row, column, value: -1, state: null };
}
