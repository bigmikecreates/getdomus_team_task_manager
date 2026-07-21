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

const statusCardColors: Record<string, string> = {
  todo: "bg-gray-50 border-gray-200",
  in_progress: "bg-blue-50 border-blue-200",
  in_review: "bg-yellow-50 border-yellow-200",
  done: "bg-green-50 border-green-200",
};

const priorityLabels: Record<string, string> = {
  low: "Low",
  medium: "Medium",
  high: "High",
  critical: "Critical",
};

const priorityCardColors: Record<string, string> = {
  low: "bg-gray-50 border-gray-200",
  medium: "bg-blue-50 border-blue-200",
  high: "bg-orange-50 border-orange-200",
  critical: "bg-red-50 border-red-200",
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

export default function DashboardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["dashboard-overview"],
    queryFn: () => dashboard.overview(),
  });

  if (isLoading) {
    return <p className="text-sm text-gray-500">Loading dashboard...</p>;
  }

  if (error) {
    return (
      <p className="text-sm text-red-600">
        {error instanceof Error ? error.message : "Failed to load dashboard"}
      </p>
    );
  }

  if (!data) return null;

  const { stats, recent_tasks, overdue_tasks } = data;

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Dashboard</h1>

      <div className="mb-8">
        <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
          Overview
        </h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <StatCard label="Total Tasks" value={stats.total_tasks} />
          <StatCard label="Overdue" value={overdue_tasks} color="bg-red-50 border-red-200" />
          {stats.by_status.map((s) => (
            <StatCard
              key={s.status}
              label={statusLabels[s.status] || s.status}
              value={s.count}
              color={statusCardColors[s.status]}
            />
          ))}
        </div>
      </div>

      {stats.by_priority.length > 0 && (
        <div className="mb-8">
          <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
            By Priority
          </h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
            {stats.by_priority.map((p) => (
              <StatCard
                key={p.priority}
                label={priorityLabels[p.priority] || p.priority}
                value={p.count}
                color={priorityCardColors[p.priority]}
              />
            ))}
          </div>
        </div>
      )}

      {stats.by_assignee.length > 0 && (
        <div className="mb-8">
          <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
            By Assignee
          </h2>
          <div className="grid grid-cols-2 gap-4 md:grid-cols-3">
            {stats.by_assignee.map((a) => (
              <StatCard
                key={a.developer_id}
                label={a.developer_name}
                value={a.task_count}
              />
            ))}
          </div>
        </div>
      )}

      {recent_tasks.length > 0 && (
        <div>
          <h2 className="mb-3 text-sm font-semibold uppercase text-gray-500">
            Recent Tasks
          </h2>
          <div className="overflow-hidden rounded-lg bg-white shadow">
            <table className="w-full text-left text-sm">
              <thead className="border-b border-gray-200 bg-gray-50">
                <tr>
                  <th className="px-4 py-3 font-medium">Title</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium">Priority</th>
                </tr>
              </thead>
              <tbody>
                {recent_tasks.map((task) => (
                  <tr key={task.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="px-4 py-3">
                      <Link
                        href={`/tasks/${task.id}/edit`}
                        className="font-medium text-blue-600 hover:underline"
                      >
                        {task.title}
                      </Link>
                    </td>
                    <td className="px-4 py-3">
                      <span className="text-xs text-gray-500">
                        {statusLabels[task.status] || task.status}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-500">
                      {priorityLabels[task.priority] || task.priority}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
