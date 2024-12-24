import axios from "axios";

export function configureAxios() {
  axios.defaults.baseURL =
    import.meta.env.VITE_APP_API_BASE_URL ?? "http://localhost:8000/api/";
}
