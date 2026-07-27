import { useEffect, useState } from "react";

import StatCard from "../components/Card";
import LineChartCard from "../components/LineChartCard";
import PieChartCard from "../components/PieChartCard";
import LoadingSpinner from "../components/LoadingSpinner";

import { getDashboardSummary } from "../services/dashboardService";
import { getPredictionHistory } from "../services/predictionService";

export default function Dashboard() {

  const [summary, setSummary] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {

    try {

      const summaryData = await getDashboardSummary();
      const historyData = await getPredictionHistory();

      setSummary(summaryData);
      setHistory(historyData);

    } catch (err) {
      console.error(err);
    }

    setLoading(false);

  };

  if (loading) return <LoadingSpinner />;

    if (!summary) {
    return (
        <div className="text-red-500 p-6">
        Unable to load dashboard.
        </div>
    );
    }

  return (

    <div className="space-y-8">

      <div className="grid grid-cols-4 gap-5">

        <StatCard
          title="Predictions"
          value={summary.total_predictions}
        />

        <StatCard
          title="Reorders"
          value={summary.reorder_count}
        />

        <StatCard
          title="High Risk"
          value={summary.high_risk_count}
        />

        <StatCard
          title="Overstock"
          value={summary.overstock_count}
        />

      </div>

      <div className="grid grid-cols-2 gap-6">

        <LineChartCard
          data={history}
        />

        <PieChartCard
          summary={summary}
        />

      </div>

    </div>

  );

}