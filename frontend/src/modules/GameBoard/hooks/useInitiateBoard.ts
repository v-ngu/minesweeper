import { useCallback, useEffect, useState } from "react";
import { GameDifficulty, GameStatus } from "../../../api/createNewGame";
import { BoardTile, useFetchGameBoard } from "../../../api/fetchGameBoard";
import { BoardSize } from "../GameBoard";
import { arrangeTiles } from "../utils/arrangeTiles";

const BOARD_SIZES: Record<GameDifficulty, BoardSize> = {
  [GameDifficulty.EASY]: { rows: 8, columns: 8 },
  [GameDifficulty.MEDIUM]: { rows: 16, columns: 16 },
  [GameDifficulty.HARD]: { rows: 16, columns: 30 },
};

export function useInitiateBoard(gameId: string) {
  const { loading, fetchGameBoard } = useFetchGameBoard();
  const [board, setBoard] = useState<BoardTile[]>([]);
  const [usedFlagsCount, setUsedFlagsCount] = useState(0);
  const [gameStatus, setGameStatus] = useState<GameStatus>();
  const [gameDifficulty, setGameDifficulty] = useState<GameDifficulty | null>(
    null
  );
  const handleFetchBoard = useCallback(async () => {
    if (!gameId) {
      return;
    }
    const data = await fetchGameBoard(gameId);
    if (!data) {
      return;
    }
    const {
      tilesByRow: busyTilesByRow,
      flagsCount,
      difficulty,
      gameStatus,
    } = data;

    const boardSize = BOARD_SIZES[difficulty];
    const arrangedBoard = arrangeTiles(boardSize, busyTilesByRow);
    setBoard(arrangedBoard);
    setUsedFlagsCount(flagsCount);
    setGameDifficulty(difficulty);
    setGameStatus(gameStatus);
  }, [gameId, fetchGameBoard]);

  useEffect(() => {
    handleFetchBoard();
  }, []);

  return {
    board,
    gameDifficulty,
    gameStatus,
    loading,
    usedFlagsCount,
    setBoard,
    setGameStatus,
    setUsedFlagsCount,
  };
}
