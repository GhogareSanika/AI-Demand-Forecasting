export default function PredictionResult({ result }) {
  if (!result) return null;

  return (
    <div className="bg-white shadow rounded-lg p-6 mt-6">

      <h2 className="text-2xl font-bold mb-5">
        Prediction Result
      </h2>

      <div className="grid grid-cols-2 gap-4">

        <div>
          <p className="text-gray-500">
            Predicted Demand
          </p>

          <h3 className="text-xl font-bold">
            {result.predicted_demand}
          </h3>
        </div>

        <div>
          <p className="text-gray-500">
            Recommended Stock
          </p>

          <h3 className="text-xl font-bold">
            {result.recommended_stock}
          </h3>
        </div>

        <div>
          <p className="text-gray-500">
            Safety Stock
          </p>

          <h3 className="text-xl font-bold">
            {result.safety_stock}
          </h3>
        </div>

        <div>
          <p className="text-gray-500">
            Reorder Quantity
          </p>

          <h3 className="text-xl font-bold">
            {result.reorder_quantity}
          </h3>
        </div>

        <div>
          <p className="text-gray-500">
            Status
          </p>

          <h3 className="text-xl font-bold text-blue-600">
            {result.stock_status}
          </h3>
        </div>

      </div>

    </div>
  );
}