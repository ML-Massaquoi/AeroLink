import { cookies } from "next/headers";
import { KeyRound, ScrollText, ShieldCheck } from "lucide-react";
import { PageHeader } from "@/components/shared/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { UserOut } from "@/types/api";

const backendUrl = process.env.BACKEND_API_URL ?? "http://localhost:8000";

export default async function SettingsPage() {
  const cookieStore = await cookies();
  let user: UserOut | null = null;
  try {
    const response = await fetch(`${backendUrl}/api/v1/auth/me`, {
      headers: cookieStore.toString() ? { cookie: cookieStore.toString() } : {},
      cache: "no-store",
    });
    if (response.ok) user = (await response.json()) as UserOut;
  } catch {
    user = null;
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Settings"
        description="Users, roles, permissions and application configuration."
      />

      <div className="grid gap-4 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <ShieldCheck className="h-4 w-4 text-forest" aria-hidden />
              <CardTitle>Your access</CardTitle>
            </div>
            <CardDescription>
              Roles and permissions are enforced on the server, not just hidden in the UI.
            </CardDescription>
          </CardHeader>
          <CardContent className="flex flex-col gap-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted">Role</span>
              <Badge variant="forest">{user?.role.name ?? "—"}</Badge>
            </div>
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted">Account</span>
              <span className="font-medium text-foreground">{user?.email ?? "—"}</span>
            </div>
            <div>
              <div className="mb-2 flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-muted">
                <KeyRound className="h-3.5 w-3.5" aria-hidden />
                Granted permissions
              </div>
              <div className="flex flex-wrap gap-1.5">
                {user?.role.permissions.length ? (
                  user.role.permissions.map((p) => (
                    <Badge key={p} variant="neutral">
                      {p}
                    </Badge>
                  ))
                ) : (
                  <span className="text-sm text-muted">No permissions loaded</span>
                )}
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center gap-2">
              <ScrollText className="h-4 w-4 text-forest" aria-hidden />
              <CardTitle>User management</CardTitle>
            </div>
            <CardDescription>
              Creating and editing users, roles and permission assignments.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <EmptyState
              icon={KeyRound}
              title="User management UI not built yet"
              description="The backend already exposes /users and /roles with admin permissions enforced. The management interface arrives with the settings module build (see docs/ROADMAP.md)."
            />
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
