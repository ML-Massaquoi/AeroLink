"use client";

import { useState, useTransition } from "react";
import { useRouter } from "next/navigation";
import { ChevronDown, LogOut, UserRound } from "lucide-react";
import { apiFetch } from "@/lib/api";
import { cn } from "@/lib/utils";
import type { UserOut } from "@/types/api";

export function UserMenu({ user }: { user: UserOut }) {
  const [open, setOpen] = useState(false);
  const [isPending, startTransition] = useTransition();
  const router = useRouter();

  const initials = user.full_name
    .split(" ")
    .map((p) => p[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();

  function logout() {
    startTransition(async () => {
      try {
        await apiFetch("/auth/logout", { method: "POST" });
      } finally {
        router.push("/login");
        router.refresh();
      }
    });
  }

  return (
    <div className="relative">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        onBlur={() => window.setTimeout(() => setOpen(false), 120)}
        aria-expanded={open}
        aria-haspopup="menu"
        className="flex items-center gap-2 rounded-[var(--radius-md)] border border-border bg-surface px-2 py-1.5 text-sm hover:bg-surface-secondary"
      >
        <span className="flex h-6 w-6 items-center justify-center rounded-full bg-accent-subtle text-[10px] font-semibold text-forest">
          {initials}
        </span>
        <span className="hidden max-w-32 truncate text-left leading-tight sm:block">
          <span className="block text-xs font-medium text-foreground">{user.full_name}</span>
          <span className="block text-[11px] text-muted">{user.role.name}</span>
        </span>
        <ChevronDown className="h-3.5 w-3.5 text-muted" aria-hidden />
      </button>

      {open ? (
        <div
          role="menu"
          className="absolute right-0 top-full z-50 mt-1 w-56 rounded-[var(--radius-lg)] border border-border bg-surface p-1 shadow-[0_4px_16px_rgb(37_41_35/0.08)]"
        >
          <div className="border-b border-border px-3 py-2">
            <div className="truncate text-sm font-medium text-foreground">{user.email}</div>
            <div className="text-xs text-muted">{user.role.name}</div>
          </div>
          <div className="flex items-center gap-2 px-3 py-2 text-xs text-muted">
            <UserRound className="h-3.5 w-3.5" aria-hidden />
            {user.role.permissions.length} permissions
          </div>
          <button
            type="button"
            role="menuitem"
            onClick={logout}
            disabled={isPending}
            className={cn(
              "flex w-full items-center gap-2 rounded-[var(--radius-sm)] px-3 py-2 text-sm text-critical hover:bg-critical-bg",
              isPending && "opacity-50",
            )}
          >
            <LogOut className="h-3.5 w-3.5" aria-hidden />
            {isPending ? "Signing out…" : "Sign out"}
          </button>
        </div>
      ) : null}
    </div>
  );
}
