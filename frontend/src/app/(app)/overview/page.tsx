import Link from "next/link";
import { cookies } from "next/headers";
import { ArrowRight, CircleCheck, Database, Server, ShieldCheck } from "lucide-react";
import { PageHeader } from "@/components/shared/page-header";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { EmptyState } from "@/components/shared/empty-state";
import { buttonVariants } from "@/components/ui/button";
import type { HealthStatus, UserOut } from "@/types/api";

const backendUrl = process.env.BACKEND_API_URL ?? "http://localhost:8000";

async function fetchJson<T>(path: string, cookieHeader: string): Promise<T | null> {
  try {
    const response = await fetch(`${backendUrl}/api/v1${path}`, {
      headers: cookieHeader ? { cookie: cookieHeader } : {},
      cache: "no-store",
    });
    if (!response.ok) return null;
    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export default async function OverviewPage() {
  const cookieStore = await cookies();
  const cookieHeader = cookieStore.toString();

  const [health, user] = await Promise.all([
    fetchJson<HealthStatus>("/health", cookieHeader),
    fetchJson<UserOut>("/auth/me", cookieHeader),
  ]);

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Overview"
        description="Operational infrastructure status for Freetown International Airport."
      />

      <div className="grid gap-4 sm:grid-cols-3">
        <SystemCard
          title="Application"
          icon={Server}
          status={health?.status === "ok" ? "ok" : health ? "degraded" : "unreachable"}
          detail={health ? `API ${health.status} · ${health.app}` : "API not reachable"}
        />
        <SystemCard
          title="Database"
          icon={Database}
          status={health?.database === "ok" ? "ok" : health ? "degraded" : "unreachable"}
          detail={
            health?.database === "ok"
              ? "PostgreSQL connected"
              : health
                ? "Database unavailable"
                : "Unknown — API not reachable"
          }
        />
        <SystemCard
          title="Session"
          icon={ShieldCheck}
          status={user ? "ok" : "degraded"}
          detail={
            user
              ? `${user.full_name} · ${user.role.name}`
              : "Not authenticated"
          }
        />
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Infrastructure inventory</CardTitle>
          <CardDescription>
            Real counts will appear here once locations, racks and devices are registered.
          </CardDescription>
        </CardHeader>
        <CardContent>
          <EmptyState
            icon={Database}
            title="No infrastructure recorded yet"
            description="AeroLink starts empty by design — no sample or fabricated data. Begin by registering buildings and technical rooms, then racks, switches and connections. See the roadmap in docs/ROADMAP.md."
            action={
              <Link href="/locations" className={buttonVariants({ variant: "secondary" })}>
                <span className="flex items-center gap-1.5">
                  Go to Locations <ArrowRight className="h-3.5 w-3.5" aria-hidden />
                </span>
              </Link>
            }
          />
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>System readiness</CardTitle>
          <CardDescription>Foundation checklist for this build stage.</CardDescription>
        </CardHeader>
        <CardContent>
          <ul className="grid gap-2 text-sm sm:grid-cols-2">
            <ReadyItem done label="Authentication & sessions" />
            <ReadyItem done label="Role-based access control (server-side)" />
            <ReadyItem done label="Audit log for changes" />
            <ReadyItem done label="Design system & application shell" />
            <ReadyItem done label="Health checks" />
            <ReadyItem done label="Database migrations" />
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}

function SystemCard({
  title,
  icon: Icon,
  status,
  detail,
}: {
  title: string;
  icon: React.ElementType;
  status: "ok" | "degraded" | "unreachable";
  detail: string;
}) {
  const badge =
    status === "ok" ? (
      <Badge variant="success">Operational</Badge>
    ) : status === "degraded" ? (
      <Badge variant="warning">Degraded</Badge>
    ) : (
      <Badge variant="critical">Offline</Badge>
    );

  return (
    <Card>
      <CardHeader className="flex-row items-center justify-between">
        <div className="flex items-center gap-2">
          <Icon className="h-4 w-4 text-forest" aria-hidden />
          <CardTitle>{title}</CardTitle>
        </div>
        {badge}
      </CardHeader>
      <CardContent>
        <p className="text-sm text-muted">{detail}</p>
      </CardContent>
    </Card>
  );
}

function ReadyItem({ label, done }: { label: string; done?: boolean }) {
  return (
    <li className="flex items-center gap-2 text-foreground">
      {done ? (
        <CircleCheck className="h-4 w-4 shrink-0 text-success" aria-hidden />
      ) : (
        <span className="h-4 w-4 shrink-0 rounded-full border border-border-strong" aria-hidden />
      )}
      {label}
    </li>
  );
}
