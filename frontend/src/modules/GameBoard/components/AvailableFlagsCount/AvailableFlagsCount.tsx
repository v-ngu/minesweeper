import { IoFlagSharp as FlagIcon } from "react-icons/io5";
import { GameDifficulty } from "../../../../api/createNewGame";
import styles from "./AvailableFlagsCount.module.css";

const STARTING_FLAG_COUNT: Record<GameDifficulty, number> = {
  [GameDifficulty.EASY]: 10,
  [GameDifficulty.MEDIUM]: 40,
  [GameDifficulty.HARD]: 99,
};

interface AvailableFlagsCountProps {
  difficulty: GameDifficulty | null;
  usedFlagsCount: number;
}

export function AvailableFlagsCount({
  difficulty,
  usedFlagsCount,
}: AvailableFlagsCountProps) {
  return (
    <div className={styles.root}>
      <FlagIcon />
      <p>
        {difficulty
          ? STARTING_FLAG_COUNT[difficulty] - usedFlagsCount
          : "404 Not Found"}
      </p>
    </div>
  );
}
