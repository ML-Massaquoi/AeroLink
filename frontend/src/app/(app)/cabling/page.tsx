import { Cable } from "lucide-react";
import { ModulePage } from "@/components/shared/module-page";

export default function CablingPage() {
  return (
    <ModulePage
      title="Cabling & Fiber"
      description="Cable registry, fiber cores, ODF and termination records."
      icon={Cable}
      emptyTitle="No cables documented"
      emptyDescription="Copper and fiber cable records, terminations and verification status will be managed here (see docs/ROADMAP.md)."
    />
  );
}
