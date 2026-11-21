import type { ApiError } from "@/types/api";

export class ApiException extends Error {
  status: number;
  detail: string;

  constructor(status: number, detail: string) {
    super(detail);
    this.status = status;
    this.detail = detail;
  }
}

interface RequestOptions extends Omit<RequestInit, "body"> {
  body?: unknown;
}

/**
 * Same-origin API client. Requests go through the Next.js rewrite to the
 * backend so the httpOnly session cookie is first-party in development.
 */
export async function apiFetch<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { body, headers, ...rest } = options;

  const response = await fetch(`/api/v1${path}`, {
    ...rest,
    credentials: "include",
    headers: {
      ...(body !== undefined ? { "Content-Type": "application/json" } : {}),
      ...headers,
    },
    body: body !== undefined ? JSON.stringify(body) : undefined,
  });

  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const payload = (await response.json()) as Partial<ApiError>;
      if (payload.detail) detail = payload.detail;
    } catch {
      // non-JSON error body — keep generic detail
    }
    throw new ApiException(response.status, detail);
  }

  return (await response.json()) as T;
}
