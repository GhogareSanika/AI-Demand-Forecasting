import {

PieChart,
Pie,
Cell,
Tooltip,
Legend,
ResponsiveContainer

} from "recharts";

const COLORS = [

"#3B82F6",
"#EF4444",
"#10B981"

];

export default function PieChartCard({ summary }) {

  const data = [

    {
      name: "High Risk",
      value: summary.high_risk_count
    },

    {
      name: "Overstock",
      value: summary.overstock_count
    },

    {
      name: "Reorders",
      value: summary.reorder_count
    }

  ];

  return (

    <div className="bg-white rounded-lg shadow p-5">

      <h2 className="text-xl font-bold mb-4">

        Stock Distribution

      </h2>

      <ResponsiveContainer
        width="100%"
        height={300}
      >

        <PieChart>

          <Pie
            data={data}
            dataKey="value"
            outerRadius={100}
            label
          >

            {

              data.map((entry, index) => (

                <Cell
                  key={index}
                  fill={COLORS[index]}
                />

              ))

            }

          </Pie>

          <Tooltip />

          <Legend />

        </PieChart>

      </ResponsiveContainer>

    </div>

  );

}