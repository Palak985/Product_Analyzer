"use client";

import { GlassCard } from "./glass-card";
import { cn } from "@/lib/utils";
import {
  BarChart3,
  Brain,
  FileText,
  Home,
  Layers,
  LineChart,
  PieChart,
  Settings,
  TrendingUp,
  Users,
  Zap,
} from "lucide-react";

const navItems = [
  { icon: Home, label: "Overview", active: true },
  { icon: TrendingUp, label: "Review Trends", badge: "Live" },
  { icon: BarChart3, label: "Analytics" },
  { icon: PieChart, label: "Sentiment Analysis" },
  { icon: LineChart, label: "Product Ratings" },
  { icon: Brain, label: "AI Insights", badge: "New" },
];

const secondaryItems = [
  { icon: Layers, label: "Data Sources" },
  { icon: FileText, label: "Reports" },
  { icon: Users, label: "Team" },
  { icon: Settings, label: "Settings" },
];

export function DashboardSidebar() {
  return (
    <GlassCard className="w-64 h-fit sticky top-6" hover={false}>
      <div className="p-4">
        <div className="mb-6">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3 px-3">
            Analytics
          </p>
          <nav className="space-y-1">
            {navItems.map((item) => (
              <button
                key={item.label}
                type="button"
                className={cn(
                  "w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                  item.active
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground hover:bg-muted/50"
                )}
              >
                <item.icon className="w-4 h-4" />
                {item.label}
                {item.badge && (
                  <span
                    className={cn(
                      "ml-auto text-[10px] font-semibold px-1.5 py-0.5 rounded-full",
                      item.active
                        ? "bg-primary-foreground/20 text-primary-foreground"
                        : item.badge === "Live"
                          ? "bg-secondary/20 text-secondary"
                          : "bg-primary/10 text-primary"
                    )}
                  >
                    {item.badge}
                  </span>
                )}
              </button>
            ))}
          </nav>
        </div>

        <div className="border-t border-border pt-4">
          <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-3 px-3">
            Workspace
          </p>
          <nav className="space-y-1">
            {secondaryItems.map((item) => (
              <button
                key={item.label}
                type="button"
                className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-muted/50 transition-all"
              >
                <item.icon className="w-4 h-4" />
                {item.label}
              </button>
            ))}
          </nav>
        </div>

        {/* AI Assistant CTA */}
        <div className="mt-6 p-4 rounded-lg bg-gradient-to-br from-primary/10 to-secondary/10 border border-primary/20">
          <div className="flex items-center gap-2 mb-2">
            <Zap className="w-4 h-4 text-primary" />
            <span className="text-sm font-semibold text-foreground">
              AI Assistant
            </span>
          </div>
          <p className="text-xs text-muted-foreground mb-3">
            Get instant insights and predictions powered by AI.
          </p>
          <button
            type="button"
            className="w-full py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:bg-primary/90 transition-colors"
          >
            Ask AI
          </button>
        </div>
      </div>
    </GlassCard>
  );
}
