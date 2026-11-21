import Link from "next/link";
import { ChevronRight } from "lucide-react";

interface Breadcrumb {
  label: string;
  href?: string;
}

export function Breadcrumbs({ items }: { items: Breadcrumb[] }) {
  if (items.length === 0) return null;

  return (
    <nav aria-label="Breadcrumb" className="flex items-center gap-1 text-xs text-muted">
      {items.map((item, index) => {
        const isLast = index === items.length - 1;
        return (
          <span key={`${item.label}-${index}`} className="flex items-center gap-1">
            {index > 0 ? <ChevronRight className="h-3 w-3" aria-hidden /> : null}
            {item.href && !isLast ? (
              <Link href={item.href} className="hover:text-foreground hover:underline">
                {item.label}
              </Link>
            ) : (
              <span
                className={isLast ? "font-medium text-foreground" : "hover:text-foreground"}
                aria-current={isLast ? "page" : undefined}
              >
                {item.label}
              </span>
            )}
          </span>
        );
      })}
    </nav>
  );
}
