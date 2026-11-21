import { LayoutGrid } from "lucide-react";
import { ModulePage } from "@/components/shared/module-page";

export default function RacksPage() {
  return (
    <ModulePage
      title="Racks & Cabinets"
      description="Rack inventory, U-position management and elevation views."
      icon={LayoutGrid}
      emptyTitle="No racks registered"
      emptyDescription="Rack and cabinet management with graphical elevation views will be built here (see docs/ROADMAP.md)."
    />
  );
}
