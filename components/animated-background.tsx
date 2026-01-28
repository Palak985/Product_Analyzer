"use client";

import { useEffect, useRef } from "react";

interface DataNode {
  x: number;
  y: number;
  vx: number;
  vy: number;
  radius: number;
  opacity: number;
  pulsePhase: number;
}

export function AnimatedBackground() {
  const canvasRef = useRef<HTMLCanvasElement>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    let animationFrameId: number;
    let nodes: DataNode[] = [];

    const resizeCanvas = () => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    };

    const initNodes = () => {
      nodes = [];
      const nodeCount = Math.floor((canvas.width * canvas.height) / 25000);

      for (let i = 0; i < nodeCount; i++) {
        nodes.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          vx: (Math.random() - 0.5) * 0.3,
          vy: (Math.random() - 0.5) * 0.3,
          radius: Math.random() * 2 + 1,
          opacity: Math.random() * 0.4 + 0.1,
          pulsePhase: Math.random() * Math.PI * 2,
        });
      }
    };

    const drawGrid = () => {
      const gridSize = 60;
      ctx.strokeStyle = "rgba(108, 92, 231, 0.04)";
      ctx.lineWidth = 1;

      for (let x = 0; x <= canvas.width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, canvas.height);
        ctx.stroke();
      }

      for (let y = 0; y <= canvas.height; y += gridSize) {
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(canvas.width, y);
        ctx.stroke();
      }
    };

    const drawGraphLines = (time: number) => {
      // Primary graph line (purple)
      ctx.beginPath();
      ctx.strokeStyle = "rgba(108, 92, 231, 0.08)";
      ctx.lineWidth = 2;

      const points1: { x: number; y: number }[] = [];
      for (let x = 0; x <= canvas.width; x += 20) {
        const y =
          canvas.height * 0.7 +
          Math.sin((x * 0.003 + time * 0.001) * 2) * 40 +
          Math.sin((x * 0.008 + time * 0.002) * 3) * 20;
        points1.push({ x, y });
      }

      ctx.moveTo(points1[0].x, points1[0].y);
      for (let i = 1; i < points1.length; i++) {
        ctx.lineTo(points1[i].x, points1[i].y);
      }
      ctx.stroke();

      // Secondary graph line (teal)
      ctx.beginPath();
      ctx.strokeStyle = "rgba(0, 184, 148, 0.06)";
      ctx.lineWidth = 2;

      const points2: { x: number; y: number }[] = [];
      for (let x = 0; x <= canvas.width; x += 20) {
        const y =
          canvas.height * 0.4 +
          Math.cos((x * 0.004 + time * 0.0008) * 2) * 50 +
          Math.sin((x * 0.006 + time * 0.001) * 2) * 25;
        points2.push({ x, y });
      }

      ctx.moveTo(points2[0].x, points2[0].y);
      for (let i = 1; i < points2.length; i++) {
        ctx.lineTo(points2[i].x, points2[i].y);
      }
      ctx.stroke();

      // Third graph line (light blue)
      ctx.beginPath();
      ctx.strokeStyle = "rgba(99, 179, 237, 0.05)";
      ctx.lineWidth = 1.5;

      const points3: { x: number; y: number }[] = [];
      for (let x = 0; x <= canvas.width; x += 25) {
        const y =
          canvas.height * 0.55 +
          Math.sin((x * 0.005 + time * 0.0015) * 1.5) * 35 +
          Math.cos((x * 0.01 + time * 0.0012) * 2) * 15;
        points3.push({ x, y });
      }

      ctx.moveTo(points3[0].x, points3[0].y);
      for (let i = 1; i < points3.length; i++) {
        ctx.lineTo(points3[i].x, points3[i].y);
      }
      ctx.stroke();
    };

    const drawNodes = (time: number) => {
      nodes.forEach((node, i) => {
        // Update position
        node.x += node.vx;
        node.y += node.vy;

        // Wrap around edges
        if (node.x < 0) node.x = canvas.width;
        if (node.x > canvas.width) node.x = 0;
        if (node.y < 0) node.y = canvas.height;
        if (node.y > canvas.height) node.y = 0;

        // Pulsing opacity
        const pulse = Math.sin(time * 0.002 + node.pulsePhase) * 0.3 + 0.7;
        const currentOpacity = node.opacity * pulse;

        // Draw node glow
        const gradient = ctx.createRadialGradient(
          node.x,
          node.y,
          0,
          node.x,
          node.y,
          node.radius * 4
        );
        gradient.addColorStop(
          0,
          `rgba(108, 92, 231, ${currentOpacity * 0.6})`
        );
        gradient.addColorStop(0.5, `rgba(0, 184, 148, ${currentOpacity * 0.3})`);
        gradient.addColorStop(1, "rgba(108, 92, 231, 0)");

        ctx.beginPath();
        ctx.fillStyle = gradient;
        ctx.arc(node.x, node.y, node.radius * 4, 0, Math.PI * 2);
        ctx.fill();

        // Draw node core
        ctx.beginPath();
        ctx.fillStyle = `rgba(108, 92, 231, ${currentOpacity})`;
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fill();

        // Draw connections to nearby nodes
        nodes.slice(i + 1).forEach((otherNode) => {
          const dx = otherNode.x - node.x;
          const dy = otherNode.y - node.y;
          const distance = Math.sqrt(dx * dx + dy * dy);

          if (distance < 150) {
            const connectionOpacity =
              ((1 - distance / 150) * currentOpacity) / 3;
            ctx.beginPath();
            ctx.strokeStyle = `rgba(108, 92, 231, ${connectionOpacity})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(node.x, node.y);
            ctx.lineTo(otherNode.x, otherNode.y);
            ctx.stroke();
          }
        });
      });
    };

    const animate = (time: number) => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      drawGrid();
      drawGraphLines(time);
      drawNodes(time);

      animationFrameId = requestAnimationFrame(animate);
    };

    resizeCanvas();
    initNodes();
    animate(0);

    window.addEventListener("resize", () => {
      resizeCanvas();
      initNodes();
    });

    return () => {
      cancelAnimationFrame(animationFrameId);
      window.removeEventListener("resize", resizeCanvas);
    };
  }, []);

  return (
    <canvas
      ref={canvasRef}
      className="fixed inset-0 pointer-events-none"
      style={{ zIndex: 0 }}
    />
  );
}
