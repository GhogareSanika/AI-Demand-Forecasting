import api from "./api";

export const predict = async (data) => {
    const response = await api.post("/predict", data);
    return response.data;
};

export const getPredictionHistory = async () => {
    const response = await api.get("/predictions");
    return response.data;
};