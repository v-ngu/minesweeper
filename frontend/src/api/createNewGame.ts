import axios from "axios";
import { useAsync } from "../hooks/useAxiosAsync";

export enum GameDifficulty {
  EASY = "easy",
  MEDIUM = "medium",
  HARD = "hard",
}

export enum GameStatus {
  PLAYING = "playing",
  LOST = "lost",
  WON = "won",
}

export interface CreateNewGamePayload {
  difficulty: GameDifficulty;
}

export interface CreateNewGameResponse {
  id: string;
  status: GameStatus;
}

export const useCreateNewGame = () => {
  const { loading, hasError, execute } = useAsync(
    async (difficulty: GameDifficulty) => {
      const payload: CreateNewGamePayload = { difficulty };
      const res = await axios.post<CreateNewGameResponse>("games/", payload);
      return res.data;
    }
  );

  return { loading, hasError, createNewGame: execute };
};
