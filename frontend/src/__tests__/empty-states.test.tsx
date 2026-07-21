import { render, screen, waitFor } from "@testing-library/react";
import { http, HttpResponse } from "msw";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { describe, it, expect } from "vitest";
import TaskListPage from "@/app/(dashboard)/tasks/page";
import { server } from "./mocks/server";

function TestWrapper({ children }: { children: React.ReactNode }) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } },
  });
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

describe("EmptyStates", () => {
  it("task list shows empty state when no tasks", async () => {
    render(
      <TestWrapper>
        <TaskListPage />
      </TestWrapper>
    );
    await waitFor(() => {
      expect(
        screen.getByText("No tasks yet. Create one to get started.")
      ).toBeInTheDocument();
    });
  });

  it("task list shows filtered empty state", async () => {
    server.use(
      http.get("*/api/tasks", () => {
        return HttpResponse.json({
          tasks: [
            {
              id: "1",
              title: "Existing task",
              description: null,
              status: "todo",
              priority: "medium",
              due_date: null,
              created_by: null,
              created_at: "2026-01-01T00:00:00Z",
              updated_at: "2026-01-01T00:00:00Z",
              developers: [],
            },
          ],
          total: 1,
        });
      })
    );

    render(
      <TestWrapper>
        <TaskListPage />
      </TestWrapper>
    );

    await waitFor(() => {
      expect(screen.getByText("Existing task")).toBeInTheDocument();
    });

    const selects = screen.getAllByRole("combobox");
    const statusSelect = selects[0] as HTMLSelectElement;
    statusSelect.value = "done";
    statusSelect.dispatchEvent(new Event("change", { bubbles: true }));

    await waitFor(() => {
      expect(screen.getByText("No tasks match your filters.")).toBeInTheDocument();
    });
  });
});
