import axios from "axios";
import { useAsync } from "../hooks/useAxiosAsync";
import { GameDifficulty, GameStatus } from "./createNewGame";

export enum BoardTileState {
  REVEALED = "revealed",
  FLAGGED = "flagged",
}

export interface BoardTile {
  gameId?: number;
  row: number;
  column: number;
  value: number;
  state: BoardTileState | null;
}

export interface FetchGameBoardResponse {
  tilesByRow: Record<number, BoardTile[]>;
  flagsCount: number;
  difficulty: GameDifficulty;
  gameStatus: GameStatus;
}

export const useFetchGameBoard = () => {
  const { loading, hasError, execute } = useAsync(async (gameId: string) => {
    const response = await axios.get<FetchGameBoardResponse>(
      `games/${gameId}/board`
    );
    return response.data;
  });

  return { loading, hasError, fetchGameBoard: execute };
};
