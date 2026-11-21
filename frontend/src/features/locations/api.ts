import { apiFetch } from "@/lib/api";

export type LocationType =
  | "building"
  | "floor"
  | "area"
  | "room"
  | "technical_room";

export interface LocationOut {
  id: number;
  code: string;
  name: string;
  type: LocationType;
  parent_id: number | null;
  description: string | null;
  is_archived: boolean;
  created_at: string | null;
}

export interface LocationTreeNode {
  id: number;
  code: string;
  name: string;
  type: LocationType;
  is_archived: boolean;
  children: LocationTreeNode[];
}

export interface LocationList {
  items: LocationOut[];
  total: number;
}

export const LOCATION_TYPE_LABELS: Record<LocationType, string> = {
  building: "Building",
  floor: "Floor",
  area: "Area",
  room: "Room",
  technical_room: "Technical Room",
};

/** Which parent types may contain a child of the given type. */
export const ALLOWED_PARENTS: Record<LocationType, LocationType[]> = {
  building: [],
  floor: ["building"],
  area: ["building", "floor"],
  room: ["floor", "area"],
  technical_room: ["floor", "area"],
};

/** Which child types may be created under a parent of the given type. */
export function allowedChildren(parentType: LocationType): LocationType[] {
  return (Object.keys(ALLOWED_PARENTS) as LocationType[]).filter((t) =>
    ALLOWED_PARENTS[t].includes(parentType),
  );
}

export function fetchTree(includeArchived = false): Promise<LocationTreeNode[]> {
  return apiFetch(`/locations/tree?include_archived=${includeArchived}`);
}

export function fetchLocations(params: {
  parent_id?: number;
  q?: string;
  type?: LocationType;
  include_archived?: boolean;
}): Promise<LocationList> {
  const search = new URLSearchParams();
  if (params.parent_id !== undefined) search.set("parent_id", String(params.parent_id));
  if (params.q) search.set("q", params.q);
  if (params.type) search.set("type", params.type);
  if (params.include_archived) search.set("include_archived", "true");
  return apiFetch(`/locations?${search.toString()}`);
}

export function createLocation(payload: {
  code: string;
  name: string;
  type: LocationType;
  parent_id: number | null;
  description?: string | null;
}): Promise<LocationOut> {
  return apiFetch("/locations", { method: "POST", body: payload });
}

export function updateLocation(
  id: number,
  payload: { code?: string; name?: string; description?: string | null },
): Promise<LocationOut> {
  return apiFetch(`/locations/${id}`, { method: "PATCH", body: payload });
}

export function setArchived(id: number, archived: boolean): Promise<LocationOut> {
  return apiFetch(`/locations/${id}/${archived ? "archive" : "unarchive"}`, {
    method: "POST",
  });
}
