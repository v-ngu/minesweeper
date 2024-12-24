import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import App from "./App.tsx";
import { configureAxios } from "./configs/axiosConfigs.ts";
import { ToastProvider } from "./contexts/ToastContext.tsx";
import "./index.css";

configureAxios();
createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ToastProvider>
      <App />
    </ToastProvider>
  </StrictMode>
);
