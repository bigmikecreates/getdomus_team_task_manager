import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
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

import TaskListPage from "@/app/(dashboard)/tasks/page";

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

describe("Task list page", () => {
  it("renders the tasks heading", () => {
    renderWithQuery(<TaskListPage />);
    expect(screen.getByText("Tasks")).toBeInTheDocument();
  });

  it("renders search input for filtering", () => {
    renderWithQuery(<TaskListPage />);
    expect(
      screen.getByPlaceholderText(/search tasks or assignees/i)
    ).toBeInTheDocument();
  });

  it("renders status filter dropdown", () => {
    renderWithQuery(<TaskListPage />);
    expect(screen.getByText("All Statuses")).toBeInTheDocument();
  });

  it("renders priority filter dropdown", () => {
    renderWithQuery(<TaskListPage />);
    expect(screen.getByText("All Priorities")).toBeInTheDocument();
  });

  it("allows typing in the search box", async () => {
    const user = userEvent.setup();
    renderWithQuery(<TaskListPage />);
    const searchInput = screen.getByPlaceholderText(/search tasks or assignees/i);
    await user.type(searchInput, "bug fix");
    expect(searchInput).toHaveValue("bug fix");
  });
});
