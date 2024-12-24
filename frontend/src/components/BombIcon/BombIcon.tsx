import { FaBomb } from "react-icons/fa6";
import styles from "./BombIcon.module.css";

export default function BombIcon({ size }: { size?: number }) {
  return <FaBomb className={styles.bombIcon} size={size} />;
}
