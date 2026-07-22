"use client";

import { useState } from "react";
import { useParams, useRouter } from "next/navigation";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { tasks, type Task } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { statusLabels, priorityLabels } from "@/lib/labels";

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

export default function TaskDetailPage() {
  const params = useParams();
  const router = useRouter();
  const taskId = params.id as string;
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);

  const { data: task, isLoading, error } = useQuery({
    queryKey: ["task", taskId],
    queryFn: () => tasks.get(taskId),
  });

  const deleteMutation = useMutation({
    mutationFn: () => tasks.delete(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tasks"] });
      router.push("/tasks");
    },
  });

  const canEdit = user?.role === "admin" || user?.role === "manager";

  if (isLoading) {
    return (
      <div>
        <div className="mb-6 h-8 w-48 animate-pulse rounded bg-gray-100" />
        <div className="h-64 animate-pulse rounded-lg bg-gray-100" />
      </div>
    );
  }

  if (error) {
    return (
      <div>
        <h1 className="mb-6 text-2xl font-bold">Task</h1>
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-600">
            {error instanceof Error ? error.message : "Failed to load task"}
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

  if (!task) return null;

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <Link
            href="/tasks"
            className="text-sm text-blue-600 hover:underline"
          >
            &larr; Tasks
          </Link>
          <h1 className="mt-2 text-2xl font-bold">{task.title}</h1>
        </div>
        {canEdit && (
          <div className="flex gap-2">
            <Link
              href={`/tasks/${taskId}/edit`}
              className="rounded border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50"
            >
              Edit
            </Link>
            <button
              onClick={() => setShowDeleteConfirm(true)}
              className="rounded border border-red-300 bg-white px-4 py-2 text-sm font-medium text-red-600 hover:bg-red-50"
            >
              Delete
            </button>
          </div>
        )}
      </div>

      {showDeleteConfirm && (
        <div className="mb-6 rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">
            Are you sure you want to delete &ldquo;{task.title}&rdquo;? This action cannot be undone.
          </p>
          <div className="mt-3 flex gap-2">
            <button
              onClick={() => deleteMutation.mutate()}
              disabled={deleteMutation.isPending}
              className="rounded bg-red-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-red-700 disabled:opacity-50"
            >
              {deleteMutation.isPending ? "Deleting..." : "Yes, delete"}
            </button>
            <button
              onClick={() => setShowDeleteConfirm(false)}
              className="rounded border border-gray-300 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-3">
        <div className="md:col-span-2">
          <div className="rounded-lg border border-gray-200 bg-white p-6">
            <h2 className="mb-4 text-sm font-semibold uppercase text-gray-500">
              Details
            </h2>
            {task.description ? (
              <p className="whitespace-pre-wrap text-sm text-gray-700">
                {task.description}
              </p>
            ) : (
              <p className="text-sm text-gray-400">No description provided.</p>
            )}
          </div>
        </div>

        <div className="space-y-4">
          <div className="rounded-lg border border-gray-200 bg-white p-4">
            <h3 className="mb-3 text-sm font-semibold uppercase text-gray-500">
              Properties
            </h3>
            <dl className="space-y-3">
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Status</dt>
                <dd>
                  <span
                    className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${statusColors[task.status] || ""}`}
                  >
                    {statusLabels[task.status] || task.status}
                  </span>
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Priority</dt>
                <dd
                  className={`text-sm font-medium ${priorityColors[task.priority] || ""}`}
                >
                  {priorityLabels[task.priority] || task.priority}
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Due Date</dt>
                <dd className="text-sm text-gray-700">
                  {task.due_date
                    ? new Date(task.due_date).toLocaleDateString()
                    : "\u2014"}
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Created</dt>
                <dd className="text-sm text-gray-700">
                  {new Date(task.created_at).toLocaleDateString()}
                </dd>
              </div>
              <div className="flex justify-between">
                <dt className="text-sm text-gray-500">Updated</dt>
                <dd className="text-sm text-gray-700">
                  {new Date(task.updated_at).toLocaleDateString()}
                </dd>
              </div>
            </dl>
          </div>

          <div className="rounded-lg border border-gray-200 bg-white p-4">
            <h3 className="mb-3 text-sm font-semibold uppercase text-gray-500">
              Assigned Developers
            </h3>
            {task.developers.length === 0 ? (
              <p className="text-sm text-gray-400">No developers assigned.</p>
            ) : (
              <ul className="space-y-2">
                {task.developers.map((dev) => (
                  <li key={dev.id} className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-700">
                      {dev.name}
                    </span>
                    <span className="text-xs text-gray-400">
                      {dev.timezone}
                    </span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
