import { Wrench } from "lucide-react";
import { ModulePage } from "@/components/shared/module-page";

export default function OperationsPage() {
  return (
    <ModulePage
      title="Operations"
      description="Work orders, fault records and maintenance history."
      icon={Wrench}
      emptyTitle="No work orders or maintenance records"
      emptyDescription="Work order lifecycle, faults and maintenance linked to infrastructure will be implemented here (see docs/ROADMAP.md)."
    />
  );
}
