import { ScrollText } from "lucide-react";
import { ModulePage } from "@/components/shared/module-page";

export default function ReportsPage() {
  return (
    <ModulePage
      title="Reports"
      description="Inventory, port utilization, faults and export."
      icon={ScrollText}
      emptyTitle="No report data yet"
      emptyDescription="Reports generate from real infrastructure records once the registry has data (see docs/ROADMAP.md)."
    />
  );
}
