import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { Sidebar } from "@/components/layout/sidebar";
import { Topbar } from "@/components/layout/topbar";
import type { UserOut } from "@/types/api";

const backendUrl = process.env.BACKEND_API_URL ?? "http://localhost:8000";

async function fetchCurrentUser(): Promise<UserOut | null> {
  const cookieStore = await cookies();
  const cookieHeader = cookieStore.toString();

  try {
    const response = await fetch(`${backendUrl}/api/v1/auth/me`, {
      headers: cookieHeader ? { cookie: cookieHeader } : {},
      cache: "no-store",
    });
    if (!response.ok) return null;
    return (await response.json()) as UserOut;
  } catch {
    return null;
  }
}

export default async function AppLayout({ children }: { children: React.ReactNode }) {
  const user = await fetchCurrentUser();
  if (!user) {
    redirect("/login");
  }

  return (
    <div className="min-h-screen">
      <Sidebar />
      <div className="flex min-h-screen flex-col lg:pl-60">
        <Topbar user={user} />
        <main className="flex-1 px-4 py-6 sm:px-6 lg:px-8">
          <div className="mx-auto w-full max-w-7xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
