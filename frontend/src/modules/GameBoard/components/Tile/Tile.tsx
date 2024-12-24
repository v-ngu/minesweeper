import cn from "classnames";
import { IoFlagSharp as FlagIcon } from "react-icons/io5";
import { GameStatus } from "../../../../api/createNewGame";
import { BoardTile, BoardTileState } from "../../../../api/fetchGameBoard";
import { useUpdateTileState } from "../../../../api/updateTileState";
import BombIcon from "../../../../components/BombIcon/BombIcon";
import styles from "./Tile.module.css";

type IMouseEvent = React.MouseEvent<HTMLButtonElement>;

type IOnUpdateTileState = (
  tiles: BoardTile[],
  usedFlagsCount: number,
  gameStatus?: GameStatus
) => void;

interface TileProps {
  column: number;
  isDisabled: boolean;
  row: number;
  value: number;
  state?: BoardTileState;
  gameId: number;
  onUpdateTileState: IOnUpdateTileState;
}

export default function Tile({
  column,
  gameId,
  isDisabled,
  row,
  state,
  value,
  onUpdateTileState,
}: TileProps) {
  const revealedClasses = cn(styles.root, {
    [styles.revealed]: state === BoardTileState.REVEALED,
  });

  const colorClasses = {
    [styles.value1]: value === 1,
    [styles.value2]: value === 2,
    [styles.value3]: value === 3,
    [styles.value4]: value === 4,
    [styles.value5]: value >= 5,
  };

  const { updateTileState } = useUpdateTileState();

  const handleUpdateTile = async (newState: BoardTileState | null) => {
    const payload = { gameId, row, column, state: newState };
    const data = await updateTileState(payload);
    if (data) {
      onUpdateTileState(data.tiles, data.flagsCount, data.gameStatus);
    }
  };

  const handleAddRemoveFlag = async (e: IMouseEvent) => {
    e.preventDefault();
    const newState =
      state === BoardTileState.FLAGGED ? null : BoardTileState.FLAGGED;
    await handleUpdateTile(newState);
  };

  const handleRevealTile = async (e: IMouseEvent) => {
    e.preventDefault();
    await handleUpdateTile(BoardTileState.REVEALED);
  };

  if (state === BoardTileState.FLAGGED) {
    return (
      <button
        className={cn(styles.root, styles.flagged)}
        disabled={isDisabled}
        type="button"
        onContextMenu={handleAddRemoveFlag}
      >
        <FlagIcon size={15} />
      </button>
    );
  }

  if (state !== BoardTileState.REVEALED) {
    return (
      <button
        className={cn(styles.root)}
        disabled={isDisabled}
        type="button"
        onClick={handleRevealTile}
        onContextMenu={handleAddRemoveFlag}
      >
        <div className={styles.tile} />
      </button>
    );
  }

  if (value === 9) {
    return (
      <button className={revealedClasses} disabled={isDisabled}>
        <BombIcon size={17} />
      </button>
    );
  }

  return (
    <button className={revealedClasses} disabled={isDisabled}>
      <div className={cn(colorClasses)}>{value !== 0 ? value : null}</div>
    </button>
  );
}
