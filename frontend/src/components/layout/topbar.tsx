"use client";

import { usePathname } from "next/navigation";
import { Breadcrumbs } from "@/components/layout/breadcrumbs";
import { UserMenu } from "@/components/layout/user-menu";
import { navItems } from "@/lib/nav";
import type { UserOut } from "@/types/api";

function buildBreadcrumbs(pathname: string): { label: string; href?: string }[] {
  const match = navItems.find(
    (item) => pathname === item.href || pathname.startsWith(`${item.href}/`),
  );
  if (!match) return [{ label: "Overview", href: "/overview" }];

  const crumbs = [{ label: "AeroLink", href: "/overview" }, { label: match.label }];

  const remainder = pathname.slice(match.href.length).replace(/^\//, "");
  if (remainder) {
    remainder.split("/").forEach((segment, index, all) => {
      const label = segment
        .split("-")
        .map((w) => w.charAt(0).toUpperCase() + w.slice(1))
        .join(" ");
      crumbs.push({
        label,
        href: index < all.length - 1 ? `${match.href}/${segment}` : undefined,
      });
    });
  }
  return crumbs;
}

export function Topbar({ user }: { user: UserOut }) {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-20 flex h-14 items-center justify-between gap-4 border-b border-border bg-surface/95 px-4 backdrop-blur sm:px-6 lg:px-8">
      <Breadcrumbs items={buildBreadcrumbs(pathname)} />
      <UserMenu user={user} />
    </header>
  );
}
