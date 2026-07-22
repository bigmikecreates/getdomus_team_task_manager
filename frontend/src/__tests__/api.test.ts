import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { http, HttpResponse } from "msw";
import { server } from "./mocks/server";

let capturedUrl: string | undefined;
let capturedOptions: RequestInit | undefined;
let overrideResponse: (() => HttpResponse) | null = null;

const captureHandler = http.all("*", ({ request }) => {
  capturedUrl = request.url;
  capturedOptions = {
    method: request.method,
    headers: Object.fromEntries(request.headers.entries()),
  };
  if (overrideResponse) {
    return overrideResponse();
  }
  return HttpResponse.json({});
});

beforeEach(() => {
  capturedUrl = undefined;
  capturedOptions = undefined;
  overrideResponse = null;
  server.use(captureHandler);
  localStorage.clear();
});

afterEach(() => {
  server.resetHandlers();
  vi.unstubAllEnvs();
});

describe("apiFetch URL construction", () => {
  it("prepends NEXT_PUBLIC_API_URL to endpoint paths", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks");

    expect(capturedUrl).toBe("https://backend.example.com/api/tasks");
  });

  it("defaults to http://localhost:8000 when NEXT_PUBLIC_API_URL is unset", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", undefined);
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks");

    expect(capturedUrl).toBe("http://localhost:8000/api/tasks");
  });

  it("constructs full URL for nested paths", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks/task-123/assign");

    expect(capturedUrl).toBe(
      "https://backend.example.com/api/tasks/task-123/assign"
    );
  });
});

describe("apiFetch authentication headers", () => {
  it("includes Authorization header when token exists in localStorage", async () => {
    localStorage.setItem("token", "test-jwt-token");
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/auth/me");

    expect(capturedOptions?.headers).toEqual(
      expect.objectContaining({
        authorization: "Bearer test-jwt-token",
      })
    );
  });

  it("does not include Authorization header when no token exists", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks");

    expect(capturedOptions?.headers).not.toHaveProperty("authorization");
  });

  it("always includes Content-Type application/json", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks");

    expect(capturedOptions?.headers).toEqual(
      expect.objectContaining({
        "content-type": "application/json",
      })
    );
  });
});

describe("apiFetch request bodies", () => {
  it("sends POST with correct URL and method", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks", {
      method: "POST",
      body: JSON.stringify({ title: "Test task" }),
    });

    expect(capturedUrl).toBe("https://backend.example.com/api/tasks");
    expect(capturedOptions?.method).toBe("POST");
  });

  it("sends PUT with correct URL and method", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks/task-123", {
      method: "PUT",
      body: JSON.stringify({ status: "done" }),
    });

    expect(capturedUrl).toBe("https://backend.example.com/api/tasks/task-123");
    expect(capturedOptions?.method).toBe("PUT");
  });

  it("sends DELETE with correct URL and method", async () => {
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await apiFetch("/api/tasks/task-123/assignments/dev-456", {
      method: "DELETE",
    });

    expect(capturedUrl).toBe(
      "https://backend.example.com/api/tasks/task-123/assignments/dev-456"
    );
    expect(capturedOptions?.method).toBe("DELETE");
  });
});

describe("apiFetch error handling", () => {
  it("throws with detail message from error response", async () => {
    overrideResponse = () =>
      HttpResponse.json({ detail: "Invalid credentials" }, { status: 401 });
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await expect(apiFetch("/api/auth/login")).rejects.toThrow(
      "Invalid credentials"
    );
  });

  it("falls back to statusText when response body has no detail", async () => {
    overrideResponse = () =>
      HttpResponse.json({}, { status: 500, statusText: "Internal Server Error" });
    vi.stubEnv("NEXT_PUBLIC_API_URL", "https://backend.example.com");
    vi.resetModules();
    const { apiFetch } = await import("@/lib/api");

    await expect(apiFetch("/api/tasks")).rejects.toThrow(
      "Request failed: 500"
    );
  });
});
