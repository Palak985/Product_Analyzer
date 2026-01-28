"use client";

import { useEffect, useRef } from "react";

export function LiveAnalyticsVisual() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;

    const resizeCanvas = () => {
      const parent = canvas.parentElement;
      if (parent) {
        canvas.width = parent.clientWidth;
        canvas.height = parent.clientHeight;
      }
    };

    interface DataPoint {
      angle: number;
      radius: number;
      opacity: number;
      speed: number;
    }

    const dataPoints: DataPoint[] = Array.from({ length: 24 }, (_, i) => ({
      angle: (i * Math.PI * 2) / 24,
      radius: 0.3 + Math.random() * 0.4,
      opacity: 0.3 + Math.random() * 0.7,
      speed: 0.5 + Math.random() * 1.5,
    }));

    const draw = (time: number) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const centerX = canvas.width / 2;
      const centerY = canvas.height / 2;
      const maxRadius = Math.min(canvas.width, canvas.height) * 0.4;

      // Draw radar circles
      for (let i = 1; i <= 4; i++) {
        const radius = (maxRadius * i) / 4;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
        ctx.strokeStyle = `rgba(108, 92, 231, ${0.1 - i * 0.02})`;
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Draw radar lines
      for (let i = 0; i < 8; i++) {
        const angle = (i * Math.PI) / 4;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY);
        ctx.lineTo(
          centerX + Math.cos(angle) * maxRadius,
          centerY + Math.sin(angle) * maxRadius
        );
        ctx.strokeStyle = "rgba(108, 92, 231, 0.08)";
        ctx.lineWidth = 1;
        ctx.stroke();
      }

      // Draw sweeping radar beam
      const sweepAngle = (time * 0.001) % (Math.PI * 2);
      const gradient = ctx.createConicGradient(sweepAngle, centerX, centerY);
      gradient.addColorStop(0, "rgba(108, 92, 231, 0.3)");
      gradient.addColorStop(0.1, "rgba(108, 92, 231, 0.1)");
      gradient.addColorStop(0.2, "rgba(108, 92, 231, 0)");
      gradient.addColorStop(1, "rgba(108, 92, 231, 0)");

      ctx.beginPath();
      ctx.moveTo(centerX, centerY);
      ctx.arc(centerX, centerY, maxRadius, sweepAngle, sweepAngle + Math.PI / 3);
      ctx.closePath();
      ctx.fillStyle = gradient;
      ctx.fill();

      // Draw data points
      dataPoints.forEach((point, i) => {
        const pulsePhase = time * 0.002 * point.speed + i;
        const pulse = 0.5 + Math.sin(pulsePhase) * 0.5;
        const currentRadius = point.radius * maxRadius;
        
        const x = centerX + Math.cos(point.angle + time * 0.0002) * currentRadius;
        const y = centerY + Math.sin(point.angle + time * 0.0002) * currentRadius;

        // Glow
        const glowGradient = ctx.createRadialGradient(x, y, 0, x, y, 12);
        glowGradient.addColorStop(0, `rgba(0, 184, 148, ${point.opacity * pulse * 0.6})`);
        glowGradient.addColorStop(0.5, `rgba(108, 92, 231, ${point.opacity * pulse * 0.3})`);
        glowGradient.addColorStop(1, "rgba(108, 92, 231, 0)");

        ctx.beginPath();
        ctx.arc(x, y, 12, 0, Math.PI * 2);
        ctx.fillStyle = glowGradient;
        ctx.fill();

        // Core
        ctx.beginPath();
        ctx.arc(x, y, 3, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(0, 184, 148, ${point.opacity * pulse})`;
        ctx.fill();
      });

      // Draw center pulse
      const centerPulse = 0.5 + Math.sin(time * 0.003) * 0.5;
      const centerGradient = ctx.createRadialGradient(
        centerX,
        centerY,
        0,
        centerX,
        centerY,
        30
      );
      centerGradient.addColorStop(0, `rgba(108, 92, 231, ${0.8 * centerPulse})`);
      centerGradient.addColorStop(0.5, `rgba(0, 184, 148, ${0.4 * centerPulse})`);
      centerGradient.addColorStop(1, "rgba(108, 92, 231, 0)");

      ctx.beginPath();
      ctx.arc(centerX, centerY, 30, 0, Math.PI * 2);
      ctx.fillStyle = centerGradient;
      ctx.fill();

      ctx.beginPath();
      ctx.arc(centerX, centerY, 6, 0, Math.PI * 2);
      ctx.fillStyle = "#6c5ce7";
      ctx.fill();

      animationFrameId = requestAnimationFrame(draw);
    };

    resizeCanvas();
    draw(0);

    window.addEventListener("resize", resizeCanvas);

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", resizeCanvas);
    };
  }, []);

  return (
    <div className="relative w-full h-full min-h-[300px]">
      <canvas ref={canvasRef} className="w-full h-full" />
      <div className="absolute bottom-4 left-4 right-4">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <span className="w-2 h-2 rounded-full bg-secondary animate-pulse" />
          Live data processing...
        </div>
      </div>
    </div>
  );
}
