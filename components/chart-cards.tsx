"use client";

import { GlassCard } from "./glass-card";
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const areaData = [
  { month: "Jan", revenue: 4000, forecast: 4200 },
  { month: "Feb", revenue: 3000, forecast: 3500 },
  { month: "Mar", revenue: 5000, forecast: 4800 },
  { month: "Apr", revenue: 4500, forecast: 4600 },
  { month: "May", revenue: 6000, forecast: 5800 },
  { month: "Jun", revenue: 5500, forecast: 5900 },
  { month: "Jul", revenue: 7000, forecast: 6800 },
];

const barData = [
  { name: "Tech", value: 85 },
  { name: "Finance", value: 72 },
  { name: "Health", value: 68 },
  { name: "Energy", value: 54 },
  { name: "Retail", value: 48 },
];

const pieData = [
  { name: "Positive", value: 62, color: "var(--secondary)" },
  { name: "Neutral", value: 25, color: "var(--chart-3)" },
  { name: "Negative", value: 13, color: "var(--destructive)" },
];

export function ChartCards() {
  return (
    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      {/* Revenue Trend Chart */}
      <GlassCard className="lg:col-span-2 p-6">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-lg font-semibold text-foreground">
              Revenue Trend
            </h3>
            <p className="text-sm text-muted-foreground">
              Actual vs AI Forecast
            </p>
          </div>
          <div className="flex items-center gap-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-primary" />
              <span className="text-muted-foreground">Actual</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-3 h-3 rounded-full bg-secondary" />
              <span className="text-muted-foreground">Forecast</span>
            </div>
          </div>
        </div>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={areaData}>
              <defs>
                <linearGradient id="colorRevenue" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="oklch(0.55 0.18 285)"
                    stopOpacity={0.3}
                  />
                  <stop
                    offset="95%"
                    stopColor="oklch(0.55 0.18 285)"
                    stopOpacity={0}
                  />
                </linearGradient>
                <linearGradient id="colorForecast" x1="0" y1="0" x2="0" y2="1">
                  <stop
                    offset="5%"
                    stopColor="oklch(0.65 0.15 175)"
                    stopOpacity={0.3}
                  />
                  <stop
                    offset="95%"
                    stopColor="oklch(0.65 0.15 175)"
                    stopOpacity={0}
                  />
                </linearGradient>
              </defs>
              <XAxis
                dataKey="month"
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
              />
              <YAxis
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                tickFormatter={(value) => `$${value / 1000}k`}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  backdropFilter: "blur(12px)",
                }}
                labelStyle={{ color: "var(--foreground)" }}
              />
              <Area
                type="monotone"
                dataKey="revenue"
                stroke="oklch(0.55 0.18 285)"
                strokeWidth={2}
                fillOpacity={1}
                fill="url(#colorRevenue)"
              />
              <Area
                type="monotone"
                dataKey="forecast"
                stroke="oklch(0.65 0.15 175)"
                strokeWidth={2}
                strokeDasharray="5 5"
                fillOpacity={1}
                fill="url(#colorForecast)"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>

      {/* Sentiment Analysis */}
      <GlassCard className="p-6">
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-foreground">
            Market Sentiment
          </h3>
          <p className="text-sm text-muted-foreground">AI Analysis Results</p>
        </div>
        <div className="h-48 flex items-center justify-center">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={pieData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={70}
                paddingAngle={5}
                dataKey="value"
              >
                {pieData.map((entry) => (
                  <Cell key={`cell-${entry.name}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  backdropFilter: "blur(12px)",
                }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
        <div className="flex justify-center gap-4 mt-4">
          {pieData.map((item) => (
            <div key={item.name} className="flex items-center gap-2 text-xs">
              <div
                className="w-2.5 h-2.5 rounded-full"
                style={{ backgroundColor: item.color }}
              />
              <span className="text-muted-foreground">
                {item.name} ({item.value}%)
              </span>
            </div>
          ))}
        </div>
      </GlassCard>

      {/* Sector Performance */}
      <GlassCard className="lg:col-span-2 p-6">
        <div className="mb-6">
          <h3 className="text-lg font-semibold text-foreground">
            Sector Performance
          </h3>
          <p className="text-sm text-muted-foreground">Market Index Scores</p>
        </div>
        <div className="h-48">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={barData} layout="vertical">
              <XAxis
                type="number"
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                domain={[0, 100]}
              />
              <YAxis
                type="category"
                dataKey="name"
                axisLine={false}
                tickLine={false}
                tick={{ fontSize: 12, fill: "var(--muted-foreground)" }}
                width={60}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "var(--card)",
                  border: "1px solid var(--border)",
                  borderRadius: "8px",
                  backdropFilter: "blur(12px)",
                }}
              />
              <Bar
                dataKey="value"
                fill="oklch(0.55 0.18 285)"
                radius={[0, 4, 4, 0]}
                barSize={20}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </GlassCard>

      {/* Quick Insights */}
      <GlassCard className="p-6">
        <div className="mb-4">
          <h3 className="text-lg font-semibold text-foreground">
            AI Insights
          </h3>
          <p className="text-sm text-muted-foreground">Latest Predictions</p>
        </div>
        <div className="space-y-4">
          {[
            {
              title: "Tech Sector Surge",
              desc: "Expected 15% growth in Q3",
              type: "positive",
            },
            {
              title: "Energy Volatility",
              desc: "Monitor oil price fluctuations",
              type: "warning",
            },
            {
              title: "Healthcare Stable",
              desc: "Consistent performance expected",
              type: "neutral",
            },
          ].map((insight) => (
            <div
              key={insight.title}
              className="p-3 rounded-lg bg-muted/30 border border-border/50"
            >
              <div className="flex items-center gap-2 mb-1">
                <div
                  className={`w-2 h-2 rounded-full ${
                    insight.type === "positive"
                      ? "bg-secondary"
                      : insight.type === "warning"
                        ? "bg-chart-4"
                        : "bg-chart-3"
                  }`}
                />
                <span className="text-sm font-medium text-foreground">
                  {insight.title}
                </span>
              </div>
              <p className="text-xs text-muted-foreground pl-4">
                {insight.desc}
              </p>
            </div>
          ))}
        </div>
      </GlassCard>
    </div>
  );
}
