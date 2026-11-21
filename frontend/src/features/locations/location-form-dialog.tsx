"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Modal } from "@/components/ui/modal";
import {
  ALLOWED_PARENTS,
  LOCATION_TYPE_LABELS,
  type LocationOut,
  type LocationType,
} from "./api";

const formSchema = z.object({
  code: z
    .string()
    .trim()
    .min(1, "Code is required")
    .max(64, "Max 64 characters")
    .regex(/^[A-Za-z0-9._/-]+$/, "Letters, digits, dots, dashes, underscores and slashes only"),
  name: z.string().trim().min(1, "Name is required").max(128, "Max 128 characters"),
  description: z.string().max(2000, "Max 2000 characters").optional(),
});

type FormValues = z.infer<typeof formSchema>;

interface LocationFormDialogProps {
  open: boolean;
  onClose: () => void;
  mode: "create" | "edit";
  /** For create: the type being created and its parent context. */
  createType?: LocationType;
  createParent?: { id: number | null; label: string } | null;
  /** For edit: the existing record. */
  location?: LocationOut | null;
  onSuccess: () => void;
}

export function LocationFormDialog({
  open,
  onClose,
  mode,
  createType,
  createParent,
  location,
  onSuccess,
}: LocationFormDialogProps) {
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    values:
      mode === "edit" && location
        ? {
            code: location.code,
            name: location.name,
            description: location.description ?? "",
          }
        : { code: "", name: "", description: "" },
  });
  const [serverError, setServerError] = useState<string | null>(null);

  async function submit(values: FormValues) {
    try {
      if (mode === "create" && createType) {
        const { createLocation } = await import("./api");
        await createLocation({
          code: values.code,
          name: values.name,
          type: createType,
          parent_id: createParent?.id ?? null,
          description: values.description || null,
        });
      } else if (location) {
        const { updateLocation } = await import("./api");
        await updateLocation(location.id, {
          code: values.code,
          name: values.name,
          description: values.description || null,
        });
      }
      reset();
      onSuccess();
      onClose();
    } catch (error) {
      const message =
        error instanceof Error ? error.message : "Save failed. Check your permissions.";
      setServerError(message);
    }
  }

  const title =
    mode === "create" ? `New ${LOCATION_TYPE_LABELS[createType ?? "room"]}` : "Edit location";
  const description =
    mode === "create"
      ? createParent
        ? `Parent: ${createParent.label}`
        : "Root-level location"
      : location
        ? `${location.code} · ${LOCATION_TYPE_LABELS[location.type]}`
        : undefined;

  return (
    <Modal open={open} onClose={onClose} title={title} description={description}>
      <form onSubmit={handleSubmit(submit)} noValidate className="flex flex-col gap-4">
        <div className="flex flex-col gap-1.5">
          <Label htmlFor="loc-code">Code</Label>
          <Input
            id="loc-code"
            placeholder="e.g. FIA-TR-01"
            aria-invalid={!!errors.code}
            {...register("code")}
          />
          <p className="text-[11px] text-muted">Unique identifier used for labels and QR codes.</p>
          {errors.code ? (
            <p className="text-xs text-critical" role="alert">
              {errors.code.message}
            </p>
          ) : null}
        </div>

        <div className="flex flex-col gap-1.5">
          <Label htmlFor="loc-name">Name</Label>
          <Input
            id="loc-name"
            placeholder="e.g. Telecom Room 01"
            aria-invalid={!!errors.name}
            {...register("name")}
          />
          {errors.name ? (
            <p className="text-xs text-critical" role="alert">
              {errors.name.message}
            </p>
          ) : null}
        </div>

        <div className="flex flex-col gap-1.5">
          <Label htmlFor="loc-desc">Description</Label>
          <textarea
            id="loc-desc"
            rows={3}
            className="flex w-full rounded-[var(--radius-md)] border border-border bg-surface px-3 py-2 text-sm text-foreground placeholder:text-muted focus-visible:outline-2 focus-visible:outline-forest"
            placeholder="Optional notes…"
            {...register("description")}
          />
          {errors.description ? (
            <p className="text-xs text-critical" role="alert">
              {errors.description.message}
            </p>
          ) : null}
        </div>

        {mode === "create" && createType && ALLOWED_PARENTS[createType].length > 0 && !createParent?.id ? (
          <p className="rounded-[var(--radius-md)] border border-warning/30 bg-warning-bg px-3 py-2 text-xs text-warning">
            Select a parent location in the tree before creating this type.
          </p>
        ) : null}

        {serverError ? (
          <div
            className="rounded-[var(--radius-md)] border border-critical/30 bg-critical-bg px-3 py-2 text-xs text-critical"
            role="alert"
          >
            {serverError}
          </div>
        ) : null}

        <div className="flex justify-end gap-2">
          <Button variant="secondary" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" disabled={isSubmitting}>
            {isSubmitting ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : null}
            {mode === "create" ? "Create" : "Save changes"}
          </Button>
        </div>
      </form>
    </Modal>
  );
}
