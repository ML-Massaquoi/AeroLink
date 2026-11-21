import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center gap-1 rounded-[var(--radius-sm)] border px-1.5 py-0.5 text-xs font-medium",
  {
    variants: {
      variant: {
        neutral: "border-border bg-surface-secondary text-muted",
        success: "border-success/20 bg-success-bg text-success",
        warning: "border-warning/20 bg-warning-bg text-warning",
        critical: "border-critical/20 bg-critical-bg text-critical",
        forest: "border-forest/20 bg-accent-subtle text-forest",
        link: "border-link/20 bg-sky-50 text-link",
      },
    },
    defaultVariants: {
      variant: "neutral",
    },
  },
);

export interface BadgeProps
  extends React.HTMLAttributes<HTMLSpanElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ variant }), className)} {...props} />;
}

export { Badge, badgeVariants };
