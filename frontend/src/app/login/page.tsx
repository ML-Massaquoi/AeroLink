"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";
import { apiFetch, ApiException } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

const loginSchema = z.object({
  email: z.string().email("Enter a valid email address"),
  password: z.string().min(1, "Password is required"),
});

type LoginForm = z.infer<typeof loginSchema>;

export default function LoginPage() {
  const router = useRouter();
  const [serverError, setServerError] = useState<string | null>(null);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginForm>({ resolver: zodResolver(loginSchema) });

  async function onSubmit(values: LoginForm) {
    setServerError(null);
    try {
      await apiFetch("/auth/login", { method: "POST", body: values });
      router.push("/overview");
      router.refresh();
    } catch (error) {
      if (error instanceof ApiException) {
        setServerError(error.detail);
      } else {
        setServerError("Unable to reach the server. Try again.");
      }
    }
  }

  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-12">
      <div className="w-full max-w-sm">
        <div className="mb-6 flex flex-col items-center text-center">
          <div className="mb-3 flex h-10 w-10 items-center justify-center rounded-[var(--radius-md)] bg-forest text-sm font-bold text-white">
            AL
          </div>
          <h1 className="text-lg font-semibold text-foreground">AeroLink</h1>
          <p className="mt-1 text-sm text-muted">
            Airport Network Infrastructure Management
            <br />
            Freetown International Airport
          </p>
        </div>

        <div className="rounded-[var(--radius-lg)] border border-border bg-surface p-5 shadow-[var(--shadow-card)]">
          <h2 className="text-sm font-semibold text-foreground">Sign in</h2>
          <p className="mb-4 mt-1 text-xs text-muted">
            Use your AeroLink account to continue.
          </p>

          <form onSubmit={handleSubmit(onSubmit)} noValidate className="flex flex-col gap-4">
            <div className="flex flex-col gap-1.5">
              <Label htmlFor="email">Email</Label>
              <Input
                id="email"
                type="email"
                autoComplete="email"
                placeholder="you@aerolink.dev"
                aria-invalid={!!errors.email}
                {...register("email")}
              />
              {errors.email ? (
                <p className="text-xs text-critical" role="alert">
                  {errors.email.message}
                </p>
              ) : null}
            </div>

            <div className="flex flex-col gap-1.5">
              <Label htmlFor="password">Password</Label>
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                placeholder="••••••••"
                aria-invalid={!!errors.password}
                {...register("password")}
              />
              {errors.password ? (
                <p className="text-xs text-critical" role="alert">
                  {errors.password.message}
                </p>
              ) : null}
            </div>

            {serverError ? (
              <div
                className="rounded-[var(--radius-md)] border border-critical/30 bg-critical-bg px-3 py-2 text-xs text-critical"
                role="alert"
              >
                {serverError}
              </div>
            ) : null}

            <Button type="submit" disabled={isSubmitting} className="w-full">
              {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : null}
              {isSubmitting ? "Signing in…" : "Sign in"}
            </Button>
          </form>
        </div>

        <p className="mt-4 text-center text-[11px] text-muted">
          Infrastructure data is restricted to authorized airport IT personnel.
        </p>
      </div>
    </main>
  );
}
