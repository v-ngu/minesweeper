import { GameDifficulty } from "../../../../api/createNewGame";
import {
  Select,
  StringValueOption,
} from "../../../../components/Select/Select";
import styles from "./Header.module.css";

interface HeaderProps {
  difficulty: StringValueOption;
  disableButton: boolean;
  handleChangeDifficulty: (difficulty: StringValueOption) => void;
  handleCreateNewGame: () => void;
}

export default function Header({
  difficulty,
  disableButton,
  handleChangeDifficulty,
  handleCreateNewGame,
}: HeaderProps) {
  return (
    <div className={styles.root}>
      <Select
        options={[
          { value: GameDifficulty.EASY, label: "Easy" },
          { value: GameDifficulty.MEDIUM, label: "Medium" },
          { value: GameDifficulty.HARD, label: "Hard" },
        ]}
        value={difficulty}
        onChange={handleChangeDifficulty}
      />
      <button
        type="button"
        onClick={handleCreateNewGame}
        disabled={disableButton}
      >
        Start New Game
      </button>
    </div>
  );
}
