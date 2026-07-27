import { useState } from "react";

import PredictionForm from "../components/PredictionForm";
import PredictionResult from "../components/PredictionResult";

import { predict } from "../services/predictionService";

export default function Prediction() {
  const [result, setResult] = useState(null);

  const handlePrediction = async (formData) => {
    try {
      const predictionRequest = {
        product_id: formData.product_id,
        current_stock: Number(formData.current_stock),

        safety_stock_percentage: 0.2,

        features: {
          temperature: Number(formData.temperature),
          fuel_price: Number(formData.fuel_price),
          holiday: Number(formData.holiday),
          cpi: Number(formData.cpi),
          unemployment: Number(formData.unemployment),
        },
      };

      const response = await predict(
        predictionRequest
      );

      setResult(response);

      loadDashboard();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="space-y-6">

      <PredictionForm
        onPredict={handlePrediction}
      />

      <PredictionResult
        result={result}
      />

    </div>
  );
}