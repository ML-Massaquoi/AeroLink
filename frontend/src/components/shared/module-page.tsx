import type { LucideIcon } from "lucide-react";
import { PageHeader } from "@/components/shared/page-header";
import { EmptyState } from "@/components/shared/empty-state";

interface ModulePageProps {
  title: string;
  description: string;
  icon: LucideIcon;
  emptyTitle: string;
  emptyDescription: string;
}

/**
 * Honest placeholder for modules scheduled in docs/ROADMAP.md.
 * Deliberately shows a real empty state — never fake records.
 */
export function ModulePage({ title, description, icon, emptyTitle, emptyDescription }: ModulePageProps) {
  return (
    <div className="flex flex-col gap-6">
      <PageHeader title={title} description={description} />
      <EmptyState icon={icon} title={emptyTitle} description={emptyDescription} />
    </div>
  );
}
