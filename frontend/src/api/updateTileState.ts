import axios from "axios";
import { useAsync } from "../hooks/useAxiosAsync";
import { GameStatus } from "./createNewGame";
import { BoardTile, BoardTileState } from "./fetchGameBoard";

interface UpdateTileStatePayload {
  gameId: number;
  row: number;
  column: number;
  state: BoardTileState | null;
}

export interface UpdateTileStateResponse {
  tiles: BoardTile[];
  flagsCount: number;
  gameStatus?: GameStatus;
}

export function useUpdateTileState() {
  const { loading, hasError, execute } = useAsync(
    async (payload: UpdateTileStatePayload) => {
      const url = "board-tiles/update-state/";
      const res = await axios.patch<UpdateTileStateResponse>(url, payload);
      return res.data;
    }
  );

  return { loading, hasError, updateTileState: execute };
}
