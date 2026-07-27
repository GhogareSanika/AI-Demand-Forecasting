import { useState } from "react";

export default function PredictionForm({ onPredict }) {
  const [formData, setFormData] = useState({
    product_id: "",
    current_stock: "",
    temperature: "",
    fuel_price: "",
    holiday: "",
    cpi: "",
    unemployment: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    onPredict(formData);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white p-6 rounded-lg shadow space-y-4"
    >
      <h2 className="text-2xl font-bold">
        Demand Prediction
      </h2>

      <input
        name="current_stock"
        placeholder="Current Stock"
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />

      <input
        name="temperature"
        placeholder="Temperature"
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />

      <input
        name="fuel_price"
        placeholder="Fuel Price"
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />

      <input
        name="holiday"
        placeholder="Holiday (0/1)"
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />

      <input
        name="cpi"
        placeholder="CPI"
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />

      <input
        name="unemployment"
        placeholder="Unemployment"
        onChange={handleChange}
        className="w-full border p-2 rounded"
      />

      <button
        className="bg-blue-600 text-white px-6 py-2 rounded"
      >
        Predict
      </button>
    </form>
  );
}