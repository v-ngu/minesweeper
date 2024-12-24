import BombIcon from "../BombIcon/BombIcon";
import styles from "./Loading.module.css";

export default function Loading() {
  return (
    <div className={styles.root}>
      <BombIcon size={25} />
      <span>Loading...</span>
    </div>
  );
}
