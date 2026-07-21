"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { dashboard, type DashboardOverview } from "@/lib/api";

const statusLabels: Record<string, string> = {
  todo: "To Do",
  in_progress: "In Progress",
  in_review: "In Review",
  done: "Done",
};

const priorityLabels: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
  critical: "Critical",
};

const priorityBarColors: Record<string, string> = {
  low: "bg-gray-400",
  medium: "bg-blue-500",
  high: "bg-orange-500",
  critical: "bg-red-500",
};

const boardStatusColors: Record<string, string> = {
  todo: "bg-gray-100",
  in_progress: "bg-blue-100",
  in_review: "bg-yellow-100",
  done: "bg-green-100",
};

const boardStatusHeaderColors: Record<string, string> = {
  todo: "bg-gray-50 border-gray-200",
  in_progress: "bg-blue-50 border-blue-200",
  in_review: "bg-yellow-50 border-yellow-200",
  done: "bg-green-50 border-green-200",
};

function StatCard({
  label,
  value,
  color,
}: {
  label: string;
  value: number;
  color?: string;
}) {
  return (
    <div
      className={`rounded-lg border p-4 ${color || "bg-white border-gray-200"}`}
    >
      <p className="text-sm text-gray-500">{label}</p>
      <p className="mt-1 text-2xl font-bold text-gray-900">{value}</p>
    </div>
  );
}

function HorizontalBar({
  label,
  value,
  max,
  color,
}: {
  label: string;
  value: number;
  max: number;
  color: string;
}) {
  const pct = max > 0 ? (value / max) * 100 : 0;
  return (
    <div className="flex items-center gap-3">
      <span className="w-20 shrink-0 text-right text-sm text-gray-600">
        {label}
      </span>
      <div className="h-4 flex-1 overflow-hidden rounded bg-gray-100">
        <div
          className={`h-full rounded ${color}`}
          style={{ width: `${pct}%` }}
        />
      </div>
      <span className="w-8 text-right text-sm font-medium text-gray-700">
        {value}
      </span>
    </div>
  );
}

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard-overview"],
    queryFn: () => dashboard.overview(),
  });

  const { data: taskData } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => import("@/lib/api").then((m) => m.tasks.list()),
  });

  if (isLoading) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold">Dashboard</h1>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-20 animate-pulse rounded-lg bg-gray-100" />
          ))}
        </div>
        <div className="mt-8 h-48 animate-pulse rounded-lg bg-gray-100" />
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold">Dashboard</h1>
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-600">
            {error instanceof Error ? error.message : "Failed to load dashboard"}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-2 text-sm font-medium text-red-700 hover:underline"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  const {
    stats,
    overdue_tasks,
    critical_tasks,
    upcoming_tasks,
    recent_tasks,
  } = data;

  const allTasks = taskData?.tasks || [];

  const statusCounts = new Map(stats.by_status.map((s) => [s.status, s.count]));
  const maxPriority = Math.max(...stats.by_priority.map((p) => p.count), 1);
  const maxAssignee = Math.max(...stats.by_assignee.map((a) => a.task_count), 1);

  const boardColumns = ["todo", "in_progress", "in_review", "done"] as const;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Dashboard</h1>
        <Link
          href="/tasks/new"
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          + New Task
        </Link>
      </div>

      {/* PROJECT HEALTH */}
      <section className="mb-8">
        <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
          Project Health
        </h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <StatCard label="Total Tasks" value={stats.total_tasks} />
          <StatCard
            label="Overdue"
            value={overdue_tasks}
            color="bg-red-50 border-red-200"
          />
          <StatCard
            label="In Progress"
            value={statusCounts.get("in_progress") || 0}
            color="bg-blue-50 border-blue-200"
          />
          <StatCard
            label="Completed"
            value={statusCounts.get("done") || 0}
            color="bg-green-50 border-green-200"
          />
        </div>
      </section>

      {/* ATTENTION REQUIRED */}
      {(critical_tasks > 0 || overdue_tasks > 0) && (
        <section className="mb-8">
          <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
            Attention Required
          </h2>
          <div className="flex flex-wrap gap-6 rounded-lg border border-amber-200 bg-amber-50 px-6 py-4">
            {critical_tasks > 0 && (
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-red-500" />
                <span className="text-sm font-medium text-gray-700">
                  {critical_tasks} critical task{critical_tasks !== 1 ? "s" : ""}
                </span>
              </div>
            )}
            {overdue_tasks > 0 && (
              <div className="flex items-center gap-2">
                <span className="h-2 w-2 rounded-full bg-orange-500" />
                <span className="text-sm font-medium text-gray-700">
                  {overdue_tasks} overdue task{overdue_tasks !== 1 ? "s" : ""}
                </span>
              </div>
            )}
          </div>
        </section>
      )}

      {/* TASK BOARD */}
      <section className="mb-8">
        <div className="mb-3 flex items-center justify-between">
          <h2 className="text-sm font-semibold uppercase text-gray-500">
            Task Board
          </h2>
          <Link
            href="/tasks"
            className="text-sm font-medium text-blue-600 hover:underline"
          >
            View Tasks &rarr;
          </Link>
        </div>
        <div className="flex gap-4 overflow-x-auto pb-4">
          {boardColumns.map((status) => {
            const colTasks = allTasks.filter((t) => t.status === status);
            return (
              <div
                key={status}
                className="flex min-w-[220px] flex-1 flex-col"
              >
                <div
                  className={`mb-2 rounded-lg border px-3 py-2 ${boardStatusHeaderColors[status]}`}
                >
                  <h3 className="text-xs font-semibold text-gray-700">
                    {statusLabels[status]}{" "}
                    <span className="font-normal text-gray-500">
                      ({colTasks.length})
                    </span>
                  </h3>
                </div>
                <div className="flex flex-1 flex-col gap-1.5">
                  {colTasks.slice(0, 5).map((task) => (
                    <Link
                      key={task.id}
                      href={`/tasks/${task.id}/edit`}
                      className="rounded border border-gray-200 bg-white p-2 text-xs hover:shadow-sm"
                    >
                      <span className="font-medium text-gray-900">
                        {task.title}
                      </span>
                    </Link>
                  ))}
                  {colTasks.length === 0 && (
                    <p className="py-4 text-center text-[10px] text-gray-400">
                      No tasks
                    </p>
                  )}
                  {colTasks.length > 5 && (
                    <p className="text-center text-[10px] text-gray-400">
                      +{colTasks.length - 5} more
                    </p>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </section>

      <div className="mb-8 grid gap-8 md:grid-cols-2">
        {/* PRIORITY DISTRIBUTION */}
        {stats.by_priority.length > 0 && (
          <section>
            <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
              Priority Distribution
            </h2>
            <div className="rounded-lg border border-gray-200 bg-white p-4">
              <div className="flex flex-col gap-3">
                {stats.by_priority
                  .sort((a, b) => {
                    const order = ["critical", "high", "medium", "low"];
                    return order.indexOf(a.priority) - order.indexOf(b.priority);
                  })
                  .map((p) => (
                    <HorizontalBar
                      key={p.priority}
                      label={priorityLabels[p.priority] || p.priority}
                      value={p.count}
                      max={maxPriority}
                      color={priorityBarColors[p.priority] || "bg-gray-400"}
                    />
                  ))}
              </div>
            </div>
          </section>
        )}

        {/* TEAM WORKLOAD */}
        {stats.by_assignee.length > 0 && (
          <section>
            <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
              Team Workload
            </h2>
            <div className="rounded-lg border border-gray-200 bg-white p-4">
              <div className="flex flex-col gap-3">
                {stats.by_assignee
                  .sort((a, b) => b.task_count - a.task_count)
                  .map((a) => (
                    <HorizontalBar
                      key={a.developer_id}
                      label={a.developer_name}
                      value={a.task_count}
                      max={maxAssignee}
                      color="bg-blue-500"
                    />
                  ))}
              </div>
            </div>
          </section>
        )}
      </div>

      <div className="grid gap-8 md:grid-cols-2">
        {/* UPCOMING DEADLINES */}
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
            Upcoming Deadlines
          </h2>
          <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
            {upcoming_tasks.length === 0 ? (
              <p className="px-4 py-6 text-center text-sm text-gray-400">
                No upcoming deadlines
              </p>
            ) : (
              <table className="w-full text-left text-sm">
                <tbody>
                  {upcoming_tasks.map((task) => (
                    <tr
                      key={task.id}
                      className="border-b border-gray-100 last:border-0"
                    >
                      <td className="px-4 py-3">
                        <Link
                          href={`/tasks/${task.id}/edit`}
                          className="font-medium text-blue-600 hover:underline"
                        >
                          {task.title}
                        </Link>
                      </td>
                      <td className="px-4 py-3 text-right text-xs text-gray-500">
                        {task.due_date
                          ? new Date(task.due_date).toLocaleDateString()
                          : "\u2014"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>

        {/* RECENT ACTIVITY */}
        <section>
          <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
            Recent Activity
          </h2>
          <div className="overflow-hidden rounded-lg border border-gray-200 bg-white">
            {recent_tasks.length === 0 ? (
              <p className="px-4 py-6 text-center text-sm text-gray-400">
                No recent activity
              </p>
            ) : (
              <table className="w-full text-left text-sm">
                <tbody>
                  {recent_tasks.map((task) => (
                    <tr
                      key={task.id}
                      className="border-b border-gray-100 last:border-0"
                    >
                      <td className="px-4 py-3">
                        <Link
                          href={`/tasks/${task.id}/edit`}
                          className="font-medium text-blue-600 hover:underline"
                        >
                          {task.title}
                        </Link>
                      </td>
                      <td className="px-4 py-3 text-right">
                        <span className="text-xs text-gray-500">
                          {statusLabels[task.status] || task.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </section>
      </div>
    </div>
  );
}
