import { Share2 } from "lucide-react";
import { ModulePage } from "@/components/shared/module-page";

export default function TopologyPage() {
  return (
    <ModulePage
      title="Topology"
      description="Connection tracing from endpoints through panels and switches."
      icon={Share2}
      emptyTitle="No connections documented"
      emptyDescription="Tracing and topology views appear once cables, patch panels and port assignments are recorded (see docs/ROADMAP.md)."
    />
  );
}
