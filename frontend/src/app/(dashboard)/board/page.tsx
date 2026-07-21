"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { tasks, type Task } from "@/lib/api";

const columns = [
  { status: "todo", label: "To Do", color: "bg-gray-100" },
  { status: "in_progress", label: "In Progress", color: "bg-blue-100" },
  { status: "in_review", label: "In Review", color: "bg-yellow-100" },
  { status: "done", label: "Done", color: "bg-green-100" },
] as const;

const priorityDot: Record<string, string> = {
  low: "bg-gray-400",
  medium: "bg-blue-500",
  high: "bg-orange-500",
  critical: "bg-red-500",
};

function TaskCard({ task }: { task: Task }) {
  return (
    <Link
      href={`/tasks/${task.id}/edit`}
      className="block rounded-lg border border-gray-200 bg-white p-3 shadow-sm hover:shadow-md"
    >
      <div className="mb-2 flex items-start justify-between gap-2">
        <h3 className="text-sm font-medium text-gray-900">{task.title}</h3>
        <span className={`mt-1 h-2 w-2 shrink-0 rounded-full ${priorityDot[task.priority] || "bg-gray-400"}`} />
      </div>
      {task.due_date && (
        <p className="mb-2 text-xs text-gray-400">
          Due {new Date(task.due_date).toLocaleDateString()}
        </p>
      )}
      {task.developers.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {task.developers.map((dev) => (
            <span
              key={dev.id}
              className="inline-block rounded bg-gray-100 px-1.5 py-0.5 text-[10px] text-gray-600"
            >
              {dev.name}
            </span>
          ))}
        </div>
      )}
    </Link>
  );
}

function BoardColumn({
  label,
  color,
  tasks: columnTasks,
}: {
  label: string;
  color: string;
  tasks: Task[];
}) {
  return (
    <div className="flex min-w-[250px] flex-1 flex-col">
      <div className={`mb-3 rounded-lg px-3 py-2 ${color}`}>
        <h2 className="text-sm font-semibold text-gray-700">
          {label}{" "}
          <span className="ml-1 text-xs font-normal text-gray-500">
            ({columnTasks.length})
          </span>
        </h2>
      </div>
      <div className="flex flex-1 flex-col gap-2">
        {columnTasks.map((task) => (
          <TaskCard key={task.id} task={task} />
        ))}
        {columnTasks.length === 0 && (
          <p className="py-8 text-center text-xs text-gray-400">
            No tasks
          </p>
        )}
      </div>
    </div>
  );
}

export default function BoardPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["tasks"],
    queryFn: () => tasks.list(),
  });

  if (isLoading) {
    return <p className="text-sm text-gray-500">Loading board...</p>;
  }

  if (error) {
    return (
      <p className="text-sm text-red-600">
        {error instanceof Error ? error.message : "Failed to load board"}
      </p>
    );
  }

  const allTasks = data?.tasks || [];

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Board</h1>
        <Link
          href="/tasks/new"
          className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
        >
          + New Task
        </Link>
      </div>

      <div className="flex gap-4 overflow-x-auto pb-4">
        {columns.map((col) => (
          <BoardColumn
            key={col.status}
            label={col.label}
            color={col.color}
            tasks={allTasks.filter((t) => t.status === col.status)}
          />
        ))}
      </div>
    </div>
  );
}
