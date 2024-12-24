import { useState } from "react";
import { ToastSeverity, useToast } from "../contexts/ToastContext";

export function useAsync<T, A extends any[]>(
  asyncFunction: (...args: A) => Promise<T>
) {
  const { showToast } = useToast();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const execute = async (...args: A) => {
    if (loading) {
      return;
    }

    setLoading(true);
    setError(null);
    try {
      return await asyncFunction(...args);
    } catch (err) {
      setError("An error occurred");
      showToast("An error occurred", ToastSeverity.ERROR);
    } finally {
      setLoading(false);
    }
  };

  const isLoading = loading && !error;
  const hasError = !!error && !loading;

  return { loading: isLoading, hasError, execute };
}
