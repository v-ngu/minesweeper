import BombIcon from "../../components/BombIcon/BombIcon";
import styles from "./HomePage.module.css";

export default function HomePage() {
  return (
    <div className={styles.root}>
      <BombIcon size={100} />
      <h1>Minesweeper</h1>
    </div>
  );
}
