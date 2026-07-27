import { useEffect, useState } from "react";
import { getPredictionHistory } from "../services/predictionService";
import LoadingSpinner from "../components/LoadingSpinner";

export default function History() {

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const data = await getPredictionHistory();
      setHistory(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner />;

  return (
    <div className="bg-white rounded-lg shadow p-6">

      <h1 className="text-2xl font-bold mb-6">
        Prediction History
      </h1>

      <table className="w-full">

        <thead className="bg-gray-100">

          <tr>
            <th className="p-3">Date</th>
            <th className="p-3">Demand</th>
            <th className="p-3">Recommended Stock</th>
            <th className="p-3">Status</th>
          </tr>

        </thead>

        <tbody>

          {history.map((item) => (

            <tr key={item.id} className="border-b">

              <td className="p-3">
                {new Date(item.created_at).toLocaleDateString()}
              </td>

              <td className="p-3">
                {item.predicted_demand}
              </td>

              <td className="p-3">
                {item.recommended_stock}
              </td>

              <td className="p-3">
                {item.stock_status}
              </td>

            </tr>

          ))}

        </tbody>

      </table>

    </div>
  );

}