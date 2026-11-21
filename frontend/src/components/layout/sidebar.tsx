"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { navItems } from "@/lib/nav";
import { cn } from "@/lib/utils";

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed inset-y-0 left-0 z-30 hidden w-60 flex-col border-r border-border bg-surface lg:flex">
      <div className="flex h-14 items-center gap-2 border-b border-border px-4">
        <div className="flex h-7 w-7 items-center justify-center rounded-[var(--radius-sm)] bg-forest text-xs font-bold text-white">
          AL
        </div>
        <div className="leading-tight">
          <div className="text-sm font-semibold text-foreground">AeroLink</div>
          <div className="text-[11px] text-muted">Freetown International Airport</div>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto px-2 py-3" aria-label="Main navigation">
        <ul className="flex flex-col gap-0.5">
          {navItems.map((item) => {
            const active = pathname === item.href || pathname.startsWith(`${item.href}/`);
            const Icon = item.icon;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  title={item.description}
                  aria-current={active ? "page" : undefined}
                  className={cn(
                    "flex items-center gap-2.5 rounded-[var(--radius-md)] px-2.5 py-2 text-sm transition-colors",
                    active
                      ? "bg-accent-subtle font-medium text-forest"
                      : "text-muted hover:bg-surface-secondary hover:text-foreground",
                  )}
                >
                  <Icon className="h-4 w-4 shrink-0" aria-hidden />
                  {item.label}
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      <div className="border-t border-border px-4 py-3 text-[11px] text-muted">
        MVP foundation · v0.1.0
      </div>
    </aside>
  );
}
