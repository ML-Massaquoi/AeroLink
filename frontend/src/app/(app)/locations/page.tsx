import { cookies } from "next/headers";
import { LocationsClient } from "@/features/locations/locations-client";
import type { UserOut } from "@/types/api";

const backendUrl = process.env.BACKEND_API_URL ?? "http://localhost:8000";

export const metadata = { title: "Locations" };

async function getCurrentUser(): Promise<UserOut | null> {
  const cookieStore = await cookies();
  try {
    const response = await fetch(`${backendUrl}/api/v1/auth/me`, {
      headers: cookieStore.toString() ? { cookie: cookieStore.toString() } : {},
      cache: "no-store",
    });
    if (!response.ok) return null;
    return (await response.json()) as UserOut;
  } catch {
    return null;
  }
}

export default async function LocationsPage() {
  const user = await getCurrentUser();
  const canWrite = user?.role.permissions.includes("infra.write") ?? false;

  return <LocationsClient canWrite={canWrite} />;
}
