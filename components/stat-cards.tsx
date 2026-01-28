"use client";

import { GlassCard } from "./glass-card";
import { ArrowDown, ArrowUp, Activity, DollarSign, TrendingUp, Users } from "lucide-react";

const stats = [
  {
    label: "Total Revenue",
    value: "$2.4M",
    change: "+12.5%",
    trend: "up",
    icon: DollarSign,
    color: "text-primary",
    bgColor: "bg-primary/10",
  },
  {
    label: "Active Markets",
    value: "847",
    change: "+8.2%",
    trend: "up",
    icon: Activity,
    color: "text-secondary",
    bgColor: "bg-secondary/10",
  },
  {
    label: "Market Growth",
    value: "+23.4%",
    change: "+2.1%",
    trend: "up",
    icon: TrendingUp,
    color: "text-chart-3",
    bgColor: "bg-chart-3/10",
  },
  {
    label: "Active Users",
    value: "12.8K",
    change: "-3.2%",
    trend: "down",
    icon: Users,
    color: "text-chart-4",
    bgColor: "bg-chart-4/10",
  },
];

export function StatCards() {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      {stats.map((stat) => (
        <GlassCard key={stat.label} className="p-5">
          <div className="flex items-start justify-between mb-4">
            <div className={`p-2.5 rounded-lg ${stat.bgColor}`}>
              <stat.icon className={`w-5 h-5 ${stat.color}`} />
            </div>
            <div
              className={`flex items-center gap-1 text-xs font-medium ${
                stat.trend === "up" ? "text-secondary" : "text-destructive"
              }`}
            >
              {stat.trend === "up" ? (
                <ArrowUp className="w-3 h-3" />
              ) : (
                <ArrowDown className="w-3 h-3" />
              )}
              {stat.change}
            </div>
          </div>
          <div>
            <p className="text-2xl font-bold text-foreground tracking-tight">
              {stat.value}
            </p>
            <p className="text-sm text-muted-foreground mt-1">{stat.label}</p>
          </div>
        </GlassCard>
      ))}
    </div>
  );
}
