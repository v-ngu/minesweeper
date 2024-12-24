import { useState } from "react";
import { Outlet, useNavigate } from "react-router-dom";
import { GameDifficulty, useCreateNewGame } from "../../api/createNewGame";
import Loading from "../../components/Loading/Loading";
import { StringValueOption } from "../../components/Select/Select";
import Header from "./components/Header/Header";
import styles from "./Dashboard.module.css";

export default function Dashboard() {
  const navigate = useNavigate();

  const { loading, createNewGame } = useCreateNewGame();
  const [selectedDifficulty, setSelectedDifficulty] =
    useState<StringValueOption | null>(null);

  const handleChangeDifficulty = (difficulty: StringValueOption) => {
    setSelectedDifficulty(difficulty);
  };
  const handleCreateNewGame = async () => {
    if (!selectedDifficulty) {
      return;
    }

    const data = await createNewGame(
      selectedDifficulty?.value as GameDifficulty
    );
    if (data) {
      navigate(`/games/${data?.id}`);
    }
  };

  return (
    <div className={styles.root}>
      <Header
        difficulty={selectedDifficulty}
        disableButton={loading || !selectedDifficulty}
        handleChangeDifficulty={handleChangeDifficulty}
        handleCreateNewGame={handleCreateNewGame}
      />
      {loading ? <Loading /> : <Outlet />}
    </div>
  );
}
