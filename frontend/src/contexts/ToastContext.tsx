import Alert from "@mui/material/Alert";
import Snackbar from "@mui/material/Snackbar";
import { createContext, ReactNode, useContext, useState } from "react";

export enum ToastSeverity {
  ERROR = "error",
  WARNING = "warning",
  INFO = "info",
  SUCCESS = "success",
}
interface IToastContext {
  showToast: (message: string, severity: ToastSeverity) => void;
}

const ToastContext = createContext<IToastContext | undefined>(undefined);

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return context;
}

interface ToastProviderProps {
  children: ReactNode;
}

export function ToastProvider({ children }: ToastProviderProps) {
  const [open, setOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [severity, setSeverity] = useState(ToastSeverity.SUCCESS);

  const showToast = (message: string, severity: ToastSeverity) => {
    setToastMessage(message);
    setSeverity(severity);
    setOpen(true);
  };

  const handleClose = (_: React.SyntheticEvent | Event, reason?: string) => {
    if (reason === "clickaway") {
      return;
    }
    setOpen(false);
  };

  return (
    <ToastContext.Provider value={{ showToast }}>
      <Snackbar
        open={open}
        anchorOrigin={{ vertical: "top", horizontal: "center" }}
        autoHideDuration={6000}
        onClose={handleClose}
      >
        <Alert severity={severity} variant="filled" onClose={handleClose}>
          {toastMessage}
        </Alert>
      </Snackbar>
      {children}
    </ToastContext.Provider>
  );
}
