export type Permission =
  | "infra.read"
  | "infra.write"
  | "ops.write"
  | "audit.read"
  | "admin.users.read"
  | "admin.users.manage"
  | "settings.manage"
  | "reports.export";

export interface RoleOut {
  id: number;
  name: string;
  description: string | null;
  permissions: string[];
}

export interface UserOut {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  role: RoleOut;
  last_login_at: string | null;
  created_at: string;
}

export interface HealthStatus {
  status: "ok" | "degraded";
  app: string;
  database: "ok" | "unavailable";
}

export interface ApiError {
  detail: string;
}
