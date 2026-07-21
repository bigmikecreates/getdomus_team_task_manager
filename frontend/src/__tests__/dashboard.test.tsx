import { render, screen, waitFor } from "@testing-library/react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, it, expect, vi } from "vitest";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

vi.mock("@/lib/auth", () => ({
  useAuth: () => ({
    user: { id: "u1", email: "admin@example.com", role: "admin" },
    loading: false,
    login: vi.fn(),
    register: vi.fn(),
    logout: vi.fn(),
  }),
}));

import DashboardPage from "@/app/(dashboard)/page";

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

describe("Dashboard page", () => {
  it("renders the dashboard heading", async () => {
    renderWithQuery(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("Dashboard")).toBeInTheDocument();
    });
  });

  it("displays project health section", async () => {
    renderWithQuery(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("Project Health")).toBeInTheDocument();
    });
  });

  it("displays total tasks stat card", async () => {
    renderWithQuery(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("Total Tasks")).toBeInTheDocument();
    });
  });

  it("displays task board section", async () => {
    renderWithQuery(<DashboardPage />);
    await waitFor(() => {
      expect(screen.getByText("Task Board")).toBeInTheDocument();
    });
  });

  it("renders new task button", async () => {
    renderWithQuery(<DashboardPage />);
    await waitFor(() => {
      expect(
        screen.getByRole("link", { name: /\+ New Task/i })
      ).toHaveAttribute("href", "/tasks/new");
    });
  });
});
