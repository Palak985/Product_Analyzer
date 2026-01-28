"use client";

import { cn } from "@/lib/utils";
import { ButtonHTMLAttributes, forwardRef } from "react";

interface AuthButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary";
  loading?: boolean;
}

export const AuthButton = forwardRef<HTMLButtonElement, AuthButtonProps>(
  ({ children, variant = "primary", loading, className, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={loading}
        className={cn(
          "relative w-full py-3.5 px-6 rounded-xl font-semibold text-base",
          "transition-all duration-300 transform",
          "focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-transparent",
          variant === "primary" && [
            "bg-gradient-to-r from-primary via-accent to-secondary",
            "text-primary-foreground",
            "hover:shadow-[0_8px_30px_rgba(108,92,231,0.4)]",
            "hover:scale-[1.02]",
            "active:scale-[0.98]",
            "focus:ring-primary",
            "disabled:opacity-70 disabled:cursor-not-allowed disabled:hover:scale-100",
          ],
          variant === "secondary" && [
            "bg-background/50 backdrop-blur-sm",
            "border border-border hover:border-primary/50",
            "text-foreground",
            "hover:bg-background/70",
            "focus:ring-primary/50",
          ],
          className
        )}
        {...props}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg
              className="animate-spin h-5 w-5"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            Processing...
          </span>
        ) : (
          <>
            <span className="relative z-10">{children}</span>
            {variant === "primary" && (
              <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-primary via-accent to-secondary opacity-0 hover:opacity-100 transition-opacity duration-300 blur-xl -z-10" />
            )}
          </>
        )}
      </button>
    );
  }
);

AuthButton.displayName = "AuthButton";
