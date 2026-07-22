"use client";

import { useState, useMemo } from "react";
import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { tasks, type Task } from "@/lib/api";
import { statusLabels, priorityLabels, statusOrder, priorityOrder } from "@/lib/labels";

const statusColors: Record<string, string> = {
  todo: "bg-gray-100 text-gray-700",
  in_progress: "bg-blue-100 text-blue-700",
  in_review: "bg-yellow-100 text-yellow-700",
  done: "bg-green-100 text-green-700",
};

const priorityColors: Record<string, string> = {
  low: "text-gray-500",
  medium: "text-blue-600",
  high: "text-orange-600",
  critical: "text-red-600",
};

const allStatuses = ["todo", "in_progress", "in_review", "done"];
const allPriorities = ["low", "medium", "high", "critical"];

type SortKey = "status" | "priority" | "due_date" | "assigned";
type SortDir = "asc" | "desc";

function SortIcon({ active, dir }: { active: boolean; dir: SortDir }) {
  if (!active) return <span className="ml-1 text-gray-300">&#8597;</span>;
  return (
    <span className="ml-1 text-blue-600">
      {dir === "asc" ? "\u25B2" : "\u25BC"}
    </span>
  );
}

function TaskRow({ task }: { task: Task }) {
  return (
    <tr className="border-b border-gray-100 hover:bg-gray-50">
      <td className="px-4 py-3">
        <span className="font-mono text-xs text-gray-400">
          {task.id.slice(0, 8)}
        </span>
      </td>
      <td className="px-4 py-3">
        <Link
          href={`/tasks/${task.id}`}
          className="font-medium text-blue-600 hover:underline"
        >
          {task.title}
        </Link>
      </td>
      <td className="px-4 py-3">
        <span
          className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[task.status] || ""}`}
        >
          {statusLabels[task.status] || task.status}
        </span>
      </td>
      <td
        className={`px-4 py-3 text-sm font-medium ${priorityColors[task.priority] || ""}`}
      >
        {priorityLabels[task.priority] || task.priority}
      </td>
      <td className="px-4 py-3 text-sm text-gray-500">
        {task.due_date
          ? new Date(task.due_date).toLocaleDateString()
          : "\u2014"}
      </td>
      <td className="px-4 py-3">
        <div className="flex flex-wrap gap-1">
          {task.developers.map((dev) => (
            <span
              key={dev.id}
              className="inline-block rounded bg-gray-100 px-2 py-0.5 text-xs text-gray-600"
            >
              {dev.name}
            </span>
          ))}
        </div>
      </td>
    </tr>
  );
}

export default function TaskListPage() {
  const [statusFilter, setStatusFilter] = useState<string>("all");
  const [priorityFilter, setPriorityFilter] = useState<string>("all");
  const [search, setSearch] = useState("");
  const [sortKey, setSortKey] = useState<SortKey | null>(null);
  const [sortDir, setSortDir] = useState<SortDir>("asc");

  const { data, isLoading, error } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => tasks.list(),
  });

  const handleSort = (key: SortKey) => {
    if (sortKey === key) {
      setSortDir(sortDir === "asc" ? "desc" : "asc");
    } else {
      setSortKey(key);
      setSortDir("asc");
    }
  };

  const filteredTasks = useMemo(() => {
    const filtered = (data?.tasks || []).filter((task) => {
      if (statusFilter !== "all" && task.status !== statusFilter) return false;
      if (priorityFilter !== "all" && task.priority !== priorityFilter) return false;
      if (search) {
        const q = search.toLowerCase();
        const matchesTitle = task.title.toLowerCase().includes(q);
        const matchesDev = task.developers.some((d) =>
          d.name.toLowerCase().includes(q)
        );
        if (!matchesTitle && !matchesDev) return false;
      }
      return true;
    });

    if (!sortKey) return filtered;

    return [...filtered].sort((a, b) => {
      let cmp = 0;
      switch (sortKey) {
        case "status":
          cmp = statusOrder.indexOf(a.status) - statusOrder.indexOf(b.status);
          break;
        case "priority":
          cmp = priorityOrder.indexOf(a.priority) - priorityOrder.indexOf(b.priority);
          break;
        case "due_date": {
          if (!a.due_date && !b.due_date) cmp = 0;
          else if (!a.due_date) cmp = 1;
          else if (!b.due_date) cmp = -1;
          else cmp = new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
          break;
        }
        case "assigned":
          cmp = a.developers.length - b.developers.length;
          break;
      }
      return sortDir === "asc" ? cmp : -cmp;
    });
  }, [data?.tasks, statusFilter, priorityFilter, search, sortKey, sortDir]);

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Tasks</h1>
        <Link
          href="/tasks/new"
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          + New Task
        </Link>
      </div>

      <div className="mb-4 flex flex-wrap gap-3">
        <input
          type="text"
          placeholder="Search tasks or assignees..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="rounded border border-gray-300 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none"
        />
        <select
          value={statusFilter}
          onChange={(e) => setStatusFilter(e.target.value)}
          className="rounded border border-gray-300 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none"
        >
          <option value="all">All Statuses</option>
          {allStatuses.map((s) => (
            <option key={s} value={s}>
              {statusLabels[s]}
            </option>
          ))}
        </select>
        <select
          value={priorityFilter}
          onChange={(e) => setPriorityFilter(e.target.value)}
          className="rounded border border-gray-300 px-3 py-1.5 text-sm focus:border-blue-500 focus:outline-none"
        >
          <option value="all">All Priorities</option>
          {allPriorities.map((p) => (
            <option key={p} value={p}>
              {priorityLabels[p]}
            </option>
          ))}
        </select>
      </div>

      {isLoading && (
        <div className="space-y-3">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="h-12 animate-pulse rounded bg-gray-100" />
          ))}
        </div>
      )}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-600">
            {error instanceof Error ? error.message : "Failed to load tasks"}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-2 text-sm font-medium text-red-700 hover:underline"
          >
            Retry
          </button>
        </div>
      )}

      {data && (
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-4 py-3 font-medium">ID</th>
                <th className="px-4 py-3 font-medium">Title</th>
                <th
                  className="cursor-pointer select-none px-4 py-3 font-medium hover:text-blue-600"
                  onClick={() => handleSort("status")}
                >
                  Status <SortIcon active={sortKey === "status"} dir={sortDir} />
                </th>
                <th
                  className="cursor-pointer select-none px-4 py-3 font-medium hover:text-blue-600"
                  onClick={() => handleSort("priority")}
                >
                  Priority <SortIcon active={sortKey === "priority"} dir={sortDir} />
                </th>
                <th
                  className="cursor-pointer select-none px-4 py-3 font-medium hover:text-blue-600"
                  onClick={() => handleSort("due_date")}
                >
                  Due Date <SortIcon active={sortKey === "due_date"} dir={sortDir} />
                </th>
                <th
                  className="cursor-pointer select-none px-4 py-3 font-medium hover:text-blue-600"
                  onClick={() => handleSort("assigned")}
                >
                  Assigned <SortIcon active={sortKey === "assigned"} dir={sortDir} />
                </th>
              </tr>
            </thead>
            <tbody>
              {filteredTasks.map((task) => (
                <TaskRow key={task.id} task={task} />
              ))}
              {filteredTasks.length === 0 && (
                <tr>
                  <td
                    colSpan={6}
                    className="px-4 py-8 text-center text-gray-500"
                  >
                    {data.tasks.length === 0
                      ? "No tasks yet. Create one to get started."
                      : "No tasks match your filters."}
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
