import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
}

export function GlassCard({
  children,
  className,
  hover = true,
}: GlassCardProps) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-xl",
        "bg-card backdrop-blur-xl",
        "border border-border",
        "shadow-[0_8px_30px_rgba(0,0,0,0.05)]",
        hover &&
          "transition-all duration-300 hover:shadow-[0_12px_40px_rgba(108,92,231,0.1)] hover:border-primary/20",
        className
      )}
    >
      {/* Subtle gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/[0.02] via-transparent to-secondary/[0.02] pointer-events-none" />
      <div className="relative z-10">{children}</div>
    </div>
  );
}
