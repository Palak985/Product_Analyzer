"use client";

import { useEffect, useState } from "react";

export function AiPulseIcon({ className }: { className?: string }) {
  const [pulse, setPulse] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setPulse((p) => (p + 1) % 360);
    }, 16);
    return () => clearInterval(interval);
  }, []);

  const pulseOpacity = 0.3 + Math.sin((pulse * Math.PI) / 180) * 0.3;

  return (
    <div className={className}>
      <svg
        width="48"
        height="48"
        viewBox="0 0 48 48"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        {/* Outer glow ring */}
        <circle
          cx="24"
          cy="24"
          r="20"
          stroke="url(#pulseGradient)"
          strokeWidth="1"
          opacity={pulseOpacity}
        />
        <circle
          cx="24"
          cy="24"
          r="16"
          stroke="url(#pulseGradient)"
          strokeWidth="0.5"
          opacity={pulseOpacity * 0.7}
        />

        {/* Neural network pattern */}
        <path
          d="M24 8L24 16M24 32L24 40M8 24L16 24M32 24L40 24"
          stroke="url(#lineGradient)"
          strokeWidth="1.5"
          strokeLinecap="round"
        />
        <path
          d="M12 12L18 18M30 30L36 36M12 36L18 30M30 18L36 12"
          stroke="url(#lineGradient)"
          strokeWidth="1"
          strokeLinecap="round"
          opacity="0.6"
        />

        {/* Central AI core */}
        <circle cx="24" cy="24" r="6" fill="url(#coreGradient)" />
        <circle
          cx="24"
          cy="24"
          r="8"
          stroke="url(#pulseGradient)"
          strokeWidth="1"
          opacity={0.5 + pulseOpacity * 0.5}
        />

        {/* Data nodes */}
        <circle cx="24" cy="12" r="2" fill="url(#nodeGradient)" />
        <circle cx="24" cy="36" r="2" fill="url(#nodeGradient)" />
        <circle cx="12" cy="24" r="2" fill="url(#nodeGradient)" />
        <circle cx="36" cy="24" r="2" fill="url(#nodeGradient)" />

        <defs>
          <linearGradient
            id="pulseGradient"
            x1="0"
            y1="0"
            x2="48"
            y2="48"
          >
            <stop stopColor="#6c5ce7" />
            <stop offset="1" stopColor="#00b894" />
          </linearGradient>
          <linearGradient
            id="lineGradient"
            x1="0"
            y1="0"
            x2="48"
            y2="48"
          >
            <stop stopColor="#6c5ce7" />
            <stop offset="0.5" stopColor="#63b3ed" />
            <stop offset="1" stopColor="#00b894" />
          </linearGradient>
          <radialGradient id="coreGradient" cx="0.5" cy="0.5" r="0.5">
            <stop stopColor="#6c5ce7" />
            <stop offset="1" stopColor="#00b894" />
          </radialGradient>
          <radialGradient id="nodeGradient" cx="0.5" cy="0.5" r="0.5">
            <stop stopColor="#63b3ed" />
            <stop offset="1" stopColor="#6c5ce7" />
          </radialGradient>
        </defs>
      </svg>
    </div>
  );
}
