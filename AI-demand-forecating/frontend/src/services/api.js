import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Request Interceptor
api.interceptors.request.use(
  (config) => {
    console.log(
      `API Request: ${config.method?.toUpperCase()} ${config.url}`
    );
    return config;
  },
  (error) => Promise.reject(error)
);

// Response Interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error("API Error:", error.response || error.message);

    if (error.response) {
      switch (error.response.status) {
        case 400:
          alert("Bad Request");
          break;

        case 404:
          alert("Resource Not Found");
          break;

        case 500:
          alert("Internal Server Error");
          break;

        default:
          alert("Something went wrong");
      }
    }

    return Promise.reject(error);
  }
);

export default api;