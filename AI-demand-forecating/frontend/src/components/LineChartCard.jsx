import {

LineChart,
Line,
XAxis,
YAxis,
CartesianGrid,
Tooltip,
ResponsiveContainer

} from "recharts";

export default function LineChartCard({ data }) {

  const chartData = data.map(item => ({

    date: new Date(item.created_at)
      .toLocaleDateString(),

    demand: item.predicted_demand

  }));

  return (

    <div className="bg-white rounded-lg shadow p-5">

      <h2 className="text-xl font-bold mb-4">
        Demand Trend
      </h2>

      <ResponsiveContainer
        width="100%"
        height={300}
      >

        <LineChart data={chartData}>

          <CartesianGrid strokeDasharray="3 3" />

          <XAxis dataKey="date" />

          <YAxis />

          <Tooltip />

          <Line
            type="monotone"
            dataKey="demand"
            stroke="#2563eb"
            strokeWidth={3}
          />

        </LineChart>

      </ResponsiveContainer>

    </div>

  );

}