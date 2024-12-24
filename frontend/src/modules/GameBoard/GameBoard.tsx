import cn from "classnames";
import { useParams } from "react-router-dom";
import { GameDifficulty, GameStatus } from "../../api/createNewGame";
import { BoardTile } from "../../api/fetchGameBoard";
import Loading from "../../components/Loading/Loading";
import { ToastSeverity, useToast } from "../../contexts/ToastContext";
import styles from "./GameBoard.module.css";
import { AvailableFlagsCount } from "./components/AvailableFlagsCount/AvailableFlagsCount";
import Tile from "./components/Tile/Tile";
import { useInitiateBoard } from "./hooks/useInitiateBoard";
import { findTile } from "./utils/findTile";

export type BoardSize = {
  rows: number;
  columns: number;
};

export function GameBoard() {
  const { gameId } = useParams();
  return gameId ? <Board key={`game-${gameId}`} gameId={gameId} /> : null;
}

function Board({ gameId }: { gameId: string }) {
  const { showToast } = useToast();

  const {
    board,
    gameDifficulty,
    gameStatus,
    loading,
    usedFlagsCount,
    setBoard,
    setGameStatus,
    setUsedFlagsCount,
  } = useInitiateBoard(gameId);

  const handleUpdateTileState = (
    tiles: BoardTile[],
    usedFlagsCount: number,
    gameStatus?: GameStatus
  ) => {
    setBoard((prevBoard) => {
      const newBoard = [...prevBoard];
      tiles.forEach((tile) => {
        const tileIndex = findTile(newBoard, tile);
        if (tileIndex !== -1) {
          newBoard[tileIndex] = tile;
        }
      });
      return newBoard;
    });
    setUsedFlagsCount(usedFlagsCount);

    if (gameStatus) {
      setGameStatus(gameStatus);
      if (gameStatus === GameStatus.WON) {
        showToast("You won!", ToastSeverity.SUCCESS);
      }
      if (gameStatus === GameStatus.LOST) {
        showToast("You lost!", ToastSeverity.WARNING);
      }
    }
  };

  const frameStyles = {
    [styles.frameEasy]: gameDifficulty === GameDifficulty.EASY,
    [styles.frameMedium]: gameDifficulty === GameDifficulty.MEDIUM,
    [styles.frameHard]: gameDifficulty === GameDifficulty.HARD,
  };

  const isGameOver =
    gameStatus === GameStatus.LOST || gameStatus === GameStatus.WON;

  if (loading) {
    return <Loading />;
  }

  return (
    <div className={styles.root}>
      <AvailableFlagsCount
        difficulty={gameDifficulty}
        usedFlagsCount={usedFlagsCount}
      />
      <div className={cn(frameStyles)}>
        {board.map((tile) => (
          <Tile
            key={`tile-${tile.row}-${tile.column}`}
            gameId={Number(gameId)}
            isDisabled={isGameOver}
            row={tile.row}
            column={tile.column}
            value={tile.value}
            state={tile.state ?? undefined}
            onUpdateTileState={handleUpdateTileState}
          />
        ))}
      </div>
    </div>
  );
}
