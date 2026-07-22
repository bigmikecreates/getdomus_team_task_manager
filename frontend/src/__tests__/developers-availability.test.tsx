import { render, screen, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, it, expect, vi } from "vitest";
import DevelopersPage from "@/app/(dashboard)/developers/page";
import { AuthProvider } from "@/lib/auth";
import { server } from "./mocks/server";

vi.mock("next/navigation", () => ({
  useRouter: () => ({
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    prefetch: vi.fn(),
  }),
}));

function TestWrapper({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>{children}</AuthProvider>
    </QueryClientProvider>
  );
}

describe("DevelopersPage", () => {
  it("shows heading", async () => {
    render(
      <TestWrapper>
        <DevelopersPage />
      </TestWrapper>
    );
    expect(screen.getByText("Developers")).toBeInTheDocument();
  });

  it("shows empty state when no developers", async () => {
    render(
      <TestWrapper>
        <DevelopersPage />
      </TestWrapper>
    );
    await waitFor(() => {
      expect(screen.getByText("No developers yet.")).toBeInTheDocument();
    });
  });

  it("shows availability columns in table", async () => {
    server.use(
      http.get("*/api/developers", () => {
        return HttpResponse.json([
          {
            id: "dev-1",
            name: "Alice",
            email: "alice@example.com",
            timezone: "America/New_York",
            working_hours_start: "09:00",
            working_hours_end: "17:00",
            created_at: "2026-01-01T00:00:00Z",
            updated_at: "2026-01-01T00:00:00Z",
            is_online: true,
            is_within_working_hours: true,
            local_time: "10:30 (UTC-04:00)",
          },
        ]);
      })
    );

    render(
      <TestWrapper>
        <DevelopersPage />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Alice")).toBeInTheDocument();
    });
    expect(screen.getByText("Local Time")).toBeInTheDocument();
    expect(screen.getByText("Availability")).toBeInTheDocument();
    expect(screen.getByText("10:30 (UTC-04:00)")).toBeInTheDocument();
    expect(screen.getByText("Within hours")).toBeInTheDocument();
  });

  it("shows offline indicator for offline developers", async () => {
    server.use(
      http.get("*/api/developers", () => {
        return HttpResponse.json([
          {
            id: "dev-2",
            name: "Bob",
            email: "bob@example.com",
            timezone: "UTC",
            working_hours_start: null,
            working_hours_end: null,
            created_at: "2026-01-01T00:00:00Z",
            updated_at: "2026-01-01T00:00:00Z",
            is_online: false,
            is_within_working_hours: false,
            local_time: "15:00 (UTC+00:00)",
          },
        ]);
      })
    );

    render(
      <TestWrapper>
        <DevelopersPage />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Bob")).toBeInTheDocument();
    });
    expect(screen.getByText("Outside hours")).toBeInTheDocument();
  });
});
