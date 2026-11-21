import {
  Cable,
  FolderTree,
  Gauge,
  LayoutGrid,
  Package,
  ScrollText,
  Settings,
  Share2,
  Wrench,
} from "lucide-react";
import type { LucideIcon } from "lucide-react";

export interface NavItem {
  href: string;
  label: string;
  icon: LucideIcon;
  description: string;
}

/**
 * Top-level navigation — 10 modules per docs/DECISIONS.md (D3).
 * Network Discovery stays hidden until Phase 3 enables it.
 */
export const navItems: NavItem[] = [
  {
    href: "/overview",
    label: "Overview",
    icon: Gauge,
    description: "Operational infrastructure dashboard",
  },
  {
    href: "/locations",
    label: "Locations",
    icon: FolderTree,
    description: "Buildings, floors, areas and rooms",
  },
  {
    href: "/infrastructure",
    label: "Infrastructure",
    icon: Package,
    description: "Equipment, switches, ports, panels, endpoints",
  },
  {
    href: "/topology",
    label: "Topology",
    icon: Share2,
    description: "Connection tracing and network relationships",
  },
  {
    href: "/racks",
    label: "Racks & Cabinets",
    icon: LayoutGrid,
    description: "Rack inventory and elevation views",
  },
  {
    href: "/cabling",
    label: "Cabling & Fiber",
    icon: Cable,
    description: "Cable registry, fiber and ODF records",
  },
  {
    href: "/operations",
    label: "Operations",
    icon: Wrench,
    description: "Work orders and maintenance",
  },
  {
    href: "/reports",
    label: "Reports",
    icon: ScrollText,
    description: "Inventory, utilization and fault reports",
  },
  {
    href: "/settings",
    label: "Settings",
    icon: Settings,
    description: "Users, roles and application settings",
  },
];
