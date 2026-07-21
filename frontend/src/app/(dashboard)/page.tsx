"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { tasks, type Task } from "@/lib/api";

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

function TaskRow({ task }: { task: Task }) {
  return (
    <tr className="border-b border-gray-100 hover:bg-gray-50">
      <td className="px-4 py-3">
        <Link
          href={`/tasks/${task.id}/edit`}
          className="font-medium text-blue-600 hover:underline"
        >
          {task.title}
        </Link>
      </td>
      <td className="px-4 py-3">
        <span
          className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[task.status] || ""}`}
        >
          {task.status.replace("_", " ")}
        </span>
      </td>
      <td
        className={`px-4 py-3 text-sm font-medium ${priorityColors[task.priority] || ""}`}
      >
        {task.priority}
      </td>
      <td className="px-4 py-3 text-sm text-gray-500">
        {task.due_date
          ? new Date(task.due_date).toLocaleDateString()
          : "—"}
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
  const { data, isLoading, error } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => tasks.list(),
  });

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

      {isLoading && <p className="text-sm text-gray-500">Loading tasks...</p>}
      {error && (
        <p className="text-sm text-red-600">
          {error instanceof Error ? error.message : "Failed to load tasks"}
        </p>
      )}

      {data && (
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-4 py-3 font-medium">Title</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Priority</th>
                <th className="px-4 py-3 font-medium">Due Date</th>
                <th className="px-4 py-3 font-medium">Assigned</th>
              </tr>
            </thead>
            <tbody>
              {data.tasks.map((task) => (
                <TaskRow key={task.id} task={task} />
              ))}
              {data.tasks.length === 0 && (
                <tr>
                  <td
                    colSpan={5}
                    className="px-4 py-8 text-center text-gray-500"
                  >
                    No tasks yet. Create one to get started.
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
