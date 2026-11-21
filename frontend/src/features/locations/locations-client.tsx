"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import {
  Archive,
  ArchiveRestore,
  ChevronDown,
  ChevronRight,
  FolderTree,
  Loader2,
  Pencil,
  Plus,
  Search,
} from "lucide-react";
import { PageHeader } from "@/components/shared/page-header";
import { EmptyState } from "@/components/shared/empty-state";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Modal } from "@/components/ui/modal";
import { cn } from "@/lib/utils";
import {
  allowedChildren,
  fetchLocations,
  fetchTree,
  LOCATION_TYPE_LABELS,
  setArchived,
  type LocationList,
  type LocationOut,
  type LocationTreeNode,
  type LocationType,
} from "./api";
import { LocationFormDialog } from "./location-form-dialog";

interface LocationsClientProps {
  canWrite: boolean;
}

export function LocationsClient({ canWrite }: LocationsClientProps) {
  const [tree, setTree] = useState<LocationTreeNode[]>([]);
  const [children, setChildren] = useState<LocationList>({ items: [], total: 0 });
  const [search, setSearch] = useState("");
  const [includeArchived, setIncludeArchived] = useState(false);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<LocationTreeNode | null>(null);
  const [expanded, setExpanded] = useState<Set<number>>(new Set());

  const [formOpen, setFormOpen] = useState(false);
  const [createType, setCreateType] = useState<LocationType | null>(null);
  const [editing, setEditing] = useState<LocationOut | null>(null);
  const [archiveTarget, setArchiveTarget] = useState<LocationOut | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const refresh = useCallback(async () => {
    const [nextTree, nextChildren] = await Promise.all([
      fetchTree(includeArchived),
      fetchLocations({
        parent_id: selected?.id,
        q: search || undefined,
        include_archived: includeArchived,
      }),
    ]);
    setTree(nextTree);
    setChildren(nextChildren);
    if (selected) {
      const stillExists = nextTree.some((n) => n.id === selected.id);
      if (!stillExists) setSelected(null);
    }
  }, [includeArchived, search, selected]);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      setLoading(true);
      try {
        const [nextTree, nextChildren] = await Promise.all([
          fetchTree(includeArchived),
          fetchLocations({
            parent_id: selected?.id,
            q: search || undefined,
            include_archived: includeArchived,
          }),
        ]);
        if (!cancelled) {
          setTree(nextTree);
          setChildren(nextChildren);
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [includeArchived, search]);

  const createContext = useMemo(() => {
    if (!createType) return { parent: null as null | { id: number | null; label: string } };
    const needsParent = allowedChildren("building").includes(createType)
      ? createType !== "building"
      : true;
    if (createType === "building") return { parent: { id: null, label: "Root level" } };
    if (selected && needsParent) {
      return { parent: { id: selected.id, label: `${selected.name} (${selected.code})` } };
    }
    return { parent: null };
  }, [createType, selected]);

  function openCreate(type: LocationType) {
    setEditing(null);
    setCreateType(type);
    setFormOpen(true);
    setActionError(null);
  }

  function openCreateUnderSelected() {
    const types = selected ? allowedChildren(selected.type) : (["building"] as LocationType[]);
    if (types.length === 0) return;
    openCreate(types[0]);
  }

  function openEdit(row: LocationOut) {
    setCreateType(null);
    setEditing(row);
    setFormOpen(true);
    setActionError(null);
  }

  async function handleArchiveConfirm() {
    if (!archiveTarget) return;
    setBusy(true);
    setActionError(null);
    try {
      await setArchived(archiveTarget.id, !archiveTarget.is_archived);
      setArchiveTarget(null);
      await refresh();
    } catch (error) {
      setActionError(error instanceof Error ? error.message : "Archive failed");
    } finally {
      setBusy(false);
    }
  }

  const typeOptions = selected
    ? allowedChildren(selected.type)
    : (["building"] as LocationType[]);

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Locations"
        description="Buildings, floors, areas, rooms and technical rooms — the root of the infrastructure hierarchy."
        actions={
          canWrite ? (
            <Button onClick={openCreateUnderSelected} disabled={typeOptions.length === 0}>
              <Plus className="h-4 w-4" aria-hidden />
              New location
            </Button>
          ) : null
        }
      />

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="relative w-full sm:max-w-xs">
          <Search
            className="pointer-events-none absolute left-2.5 top-2.5 h-4 w-4 text-muted"
            aria-hidden
          />
          <Input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search code or name…"
            className="pl-8"
            aria-label="Search locations"
          />
        </div>
        <label className="flex items-center gap-2 text-sm text-muted">
          <input
            type="checkbox"
            checked={includeArchived}
            onChange={(e) => setIncludeArchived(e.target.checked)}
            className="h-4 w-4 rounded border-border-strong accent-[var(--color-forest)]"
          />
          Include archived
        </label>
        {selected ? (
          <Button variant="ghost" size="sm" onClick={() => setSelected(null)}>
            Clear selection
          </Button>
        ) : null}
      </div>

      {actionError ? (
        <div
          className="rounded-[var(--radius-md)] border border-critical/30 bg-critical-bg px-3 py-2 text-sm text-critical"
          role="alert"
        >
          {actionError}
        </div>
      ) : null}

      {loading ? (
        <div className="flex items-center gap-2 text-sm text-muted">
          <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> Loading locations…
        </div>
      ) : tree.length === 0 && !search ? (
        <EmptyState
          icon={FolderTree}
          title="No locations registered"
          description={
            canWrite
              ? "Start by creating a building (e.g. Main Terminal), then add floors, rooms and technical rooms beneath it."
              : "No locations have been registered yet. An IT Administrator or Network Administrator can create the first building."
          }
          action={
            canWrite ? (
              <Button onClick={() => openCreate("building")}>
                <Plus className="h-4 w-4" aria-hidden />
                Create first building
              </Button>
            ) : null
          }
        />
      ) : (
        <div className="grid gap-4 lg:grid-cols-[300px_1fr]">
          <div className="rounded-[var(--radius-lg)] border border-border bg-surface">
            <div className="border-b border-border px-3 py-2 text-xs font-semibold uppercase tracking-wide text-muted">
              Hierarchy
            </div>
            <div className="max-h-[560px] overflow-y-auto p-2">
              {tree.length === 0 ? (
                <p className="px-2 py-4 text-sm text-muted">No matching locations.</p>
              ) : (
                <TreeNodes
                  nodes={tree}
                  selectedId={selected?.id ?? null}
                  expanded={expanded}
                  onToggle={(id) =>
                    setExpanded((prev) => {
                      const next = new Set(prev);
                      if (next.has(id)) next.delete(id);
                      else next.add(id);
                      return next;
                    })
                  }
                  onSelect={(node) => setSelected(node)}
                />
              )}
            </div>
          </div>

          <div className="rounded-[var(--radius-lg)] border border-border bg-surface">
            <div className="flex items-center justify-between border-b border-border px-4 py-2">
              <div className="text-xs font-semibold uppercase tracking-wide text-muted">
                {selected
                  ? `Children of ${selected.name}`
                  : search
                    ? "Search results"
                    : "Top-level locations"}
              </div>
              <div className="text-xs text-muted">{children.total} record(s)</div>
            </div>

            {children.items.length === 0 ? (
              <div className="p-4">
                <EmptyState
                  icon={FolderTree}
                  title={search ? "No matches" : "No child locations"}
                  description={
                    search
                      ? "Try a different code or name."
                      : selected
                        ? canWrite
                          ? `No locations nested under ${selected.name} yet.`
                          : `No locations nested under ${selected.name} yet.`
                        : "Create a building to get started."
                  }
                  className="border-0 py-8"
                />
              </div>
            ) : (
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Code</TableHead>
                    <TableHead>Name</TableHead>
                    <TableHead>Type</TableHead>
                    <TableHead>Status</TableHead>
                    {canWrite ? <TableHead className="w-24">Actions</TableHead> : null}
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {children.items.map((row) => (
                    <TableRow key={row.id}>
                      <TableCell className="font-mono text-xs">{row.code}</TableCell>
                      <TableCell>
                        <button
                          type="button"
                          className="text-left font-medium hover:text-forest hover:underline"
                          onClick={() => {
                            const node = findNode(tree, row.id);
                            if (node) {
                              setSelected(node);
                              setExpanded((prev) => new Set(prev).add(row.id));
                            }
                          }}
                        >
                          {row.name}
                        </button>
                      </TableCell>
                      <TableCell>
                        <Badge variant="neutral">{LOCATION_TYPE_LABELS[row.type]}</Badge>
                      </TableCell>
                      <TableCell>
                        {row.is_archived ? (
                          <Badge variant="warning">Archived</Badge>
                        ) : (
                          <Badge variant="success">Active</Badge>
                        )}
                      </TableCell>
                      {canWrite ? (
                        <TableCell>
                          <div className="flex gap-1">
                            <Button
                              variant="ghost"
                              size="icon"
                              aria-label={`Edit ${row.name}`}
                              onClick={() => openEdit(row)}
                            >
                              <Pencil className="h-3.5 w-3.5" aria-hidden />
                            </Button>
                            <Button
                              variant="ghost"
                              size="icon"
                              aria-label={row.is_archived ? `Restore ${row.name}` : `Archive ${row.name}`}
                              onClick={() => setArchiveTarget(row)}
                            >
                              {row.is_archived ? (
                                <ArchiveRestore className="h-3.5 w-3.5" aria-hidden />
                              ) : (
                                <Archive className="h-3.5 w-3.5" aria-hidden />
                              )}
                            </Button>
                          </div>
                        </TableCell>
                      ) : null}
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            )}
          </div>
        </div>
      )}

      {canWrite && formOpen ? (
        <LocationFormDialog
          open={formOpen}
          onClose={() => setFormOpen(false)}
          mode={editing ? "edit" : "create"}
          createType={editing ? undefined : createType ?? undefined}
          createParent={createContext.parent}
          location={editing}
          onSuccess={() => void refresh()}
        />
      ) : null}

      <Modal
        open={!!archiveTarget}
        onClose={() => setArchiveTarget(null)}
        title={archiveTarget?.is_archived ? "Restore location" : "Archive location"}
        description="Archiving hides the record from default views but preserves history and relationships."
      >
        <p className="text-sm text-foreground">
          {archiveTarget?.is_archived
            ? `Restore ${archiveTarget.name} (${archiveTarget.code})?`
            : `Archive ${archiveTarget?.name} (${archiveTarget?.code})?`}
        </p>
        <div className="mt-4 flex justify-end gap-2">
          <Button variant="secondary" onClick={() => setArchiveTarget(null)}>
            Cancel
          </Button>
          <Button variant="danger" onClick={() => void handleArchiveConfirm()} disabled={busy}>
            {busy ? <Loader2 className="h-4 w-4 animate-spin" aria-hidden /> : null}
            {archiveTarget?.is_archived ? "Restore" : "Archive"}
          </Button>
        </div>
      </Modal>
    </div>
  );
}

function findNode(nodes: LocationTreeNode[], id: number): LocationTreeNode | null {
  for (const node of nodes) {
    if (node.id === id) return node;
    const found = findNode(node.children, id);
    if (found) return found;
  }
  return null;
}

function TreeNodes({
  nodes,
  selectedId,
  expanded,
  onToggle,
  onSelect,
  depth = 0,
}: {
  nodes: LocationTreeNode[];
  selectedId: number | null;
  expanded: Set<number>;
  onToggle: (id: number) => void;
  onSelect: (node: LocationTreeNode) => void;
  depth?: number;
}) {
  return (
    <ul className="flex flex-col gap-0.5">
      {nodes.map((node) => {
        const hasChildren = node.children.length > 0;
        const isOpen = expanded.has(node.id);
        const isSelected = node.id === selectedId;
        return (
          <li key={node.id}>
            <div
              className={cn(
                "group flex items-center gap-1 rounded-[var(--radius-md)] px-1.5 py-1.5 text-sm",
                isSelected ? "bg-accent-subtle" : "hover:bg-surface-secondary",
              )}
              style={{ paddingLeft: `${depth * 14 + 6}px` }}
            >
              <button
                type="button"
                aria-label={isOpen ? "Collapse" : "Expand"}
                className={cn(
                  "flex h-5 w-5 shrink-0 items-center justify-center rounded-[var(--radius-sm)] text-muted hover:bg-border",
                  !hasChildren && "invisible",
                )}
                onClick={() => onToggle(node.id)}
              >
                {isOpen ? (
                  <ChevronDown className="h-3.5 w-3.5" aria-hidden />
                ) : (
                  <ChevronRight className="h-3.5 w-3.5" aria-hidden />
                )}
              </button>
              <button
                type="button"
                onClick={() => onSelect(node)}
                className={cn(
                  "flex min-w-0 flex-1 items-center gap-2 rounded-[var(--radius-sm)] px-1.5 py-1 text-left",
                  isSelected ? "font-medium text-forest" : "text-foreground",
                  node.is_archived && "opacity-60",
                )}
              >
                <span className="truncate">{node.name}</span>
                <span className="shrink-0 font-mono text-[10px] text-muted">{node.code}</span>
              </button>
            </div>
            {hasChildren && isOpen ? (
              <TreeNodes
                nodes={node.children}
                selectedId={selectedId}
                expanded={expanded}
                onToggle={onToggle}
                onSelect={onSelect}
                depth={depth + 1}
              />
            ) : null}
          </li>
        );
      })}
    </ul>
  );
}
