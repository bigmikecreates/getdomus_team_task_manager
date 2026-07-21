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

import BoardPage from "@/app/(dashboard)/board/page";

function renderWithQuery(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>
  );
}

describe("Board page", () => {
  it("renders the board heading", async () => {
    renderWithQuery(<BoardPage />);
    await waitFor(() => {
      expect(screen.getByText("Board")).toBeInTheDocument();
    });
  });

  it("displays all four Kanban columns", async () => {
    renderWithQuery(<BoardPage />);
    await waitFor(() => {
      expect(screen.getByText(/To Do/)).toBeInTheDocument();
      expect(screen.getByText(/In Progress/)).toBeInTheDocument();
      expect(screen.getByText(/In Review/)).toBeInTheDocument();
      expect(screen.getByText(/Done/)).toBeInTheDocument();
    });
  });

  it("renders the new task button", async () => {
    renderWithQuery(<BoardPage />);
    await waitFor(() => {
      expect(
        screen.getByRole("link", { name: /\+ New Task/i })
      ).toHaveAttribute("href", "/tasks/new");
    });
  });
});
