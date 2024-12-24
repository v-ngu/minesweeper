import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import "./App.css";
import Dashboard from "./modules/Dashboard/Dashboard";
import { GameBoard } from "./modules/GameBoard/GameBoard";
import HomePage from "./modules/HomePage/HomePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />}>
          <Route index element={<HomePage />} />
          <Route path="games/:gameId" element={<GameBoard />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
