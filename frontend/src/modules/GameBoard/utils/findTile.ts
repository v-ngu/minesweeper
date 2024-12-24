import { BoardTile } from "../../../api/fetchGameBoard";

export function findTile(board: BoardTile[], tile: BoardTile) {
  return board.findIndex((t) => t.row === tile.row && t.column === tile.column);
}
