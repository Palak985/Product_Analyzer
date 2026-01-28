import { DashboardHeader } from "@/components/dashboard-header";
import { DashboardSidebar } from "@/components/dashboard-sidebar";
import { StatCards } from "@/components/stat-cards";
import { ChartCards } from "@/components/chart-cards";

export default function Dashboard() {
  return (
    <div className="min-h-screen">
      {/* Header */}
      <DashboardHeader />

      {/* Main Content Area */}
      <div className="flex gap-6 p-6">
        {/* Sidebar */}
        <aside className="hidden lg:block shrink-0">
          <DashboardSidebar />
        </aside>

        {/* Main Dashboard Content */}
        <main className="flex-1 space-y-6 min-w-0">
          {/* Page Title */}
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-foreground tracking-tight">
                Dashboard Overview
              </h2>
              <p className="text-sm text-muted-foreground mt-1">
                AI-powered product review analysis and sentiment insights
              </p>
            </div>
            <div className="flex items-center gap-2">
              <span className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-secondary/10 text-secondary text-xs font-medium">
                <span className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
                Live Data
              </span>
            </div>
          </div>

          {/* Stats Row */}
          <StatCards />

          {/* Charts Grid */}
          <ChartCards />
        </main>
      </div>
    </div>
  );
}
