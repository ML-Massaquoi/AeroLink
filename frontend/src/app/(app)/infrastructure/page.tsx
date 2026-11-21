import { Package } from "lucide-react";
import { ModulePage } from "@/components/shared/module-page";

export default function InfrastructurePage() {
  return (
    <ModulePage
      title="Infrastructure"
      description="Equipment, switches and ports, patch panels and endpoints."
      icon={Package}
      emptyTitle="No equipment registered"
      emptyDescription="Equipment, switch inventory with automatic port generation, patch panels and endpoint records will live here (see docs/ROADMAP.md)."
    />
  );
}
