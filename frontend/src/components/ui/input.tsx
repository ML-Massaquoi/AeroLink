import * as React from "react";
import { cn } from "@/lib/utils";

const Input = React.forwardRef<HTMLInputElement, React.InputHTMLAttributes<HTMLInputElement>>(
  ({ className, type = "text", ...props }, ref) => (
    <input
      ref={ref}
      type={type}
      className={cn(
        "flex h-9 w-full rounded-[var(--radius-md)] border border-border bg-surface px-3 py-1 text-sm text-foreground shadow-[var(--shadow-card)] placeholder:text-muted",
        "focus-visible:outline-2 focus-visible:outline-offset-0 focus-visible:outline-forest",
        "disabled:cursor-not-allowed disabled:opacity-50",
        className,
      )}
      {...props}
    />
  ),
);
Input.displayName = "Input";

export { Input };
