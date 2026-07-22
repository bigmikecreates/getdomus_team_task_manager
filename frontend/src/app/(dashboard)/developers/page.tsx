"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { developers, presence } from "@/lib/api";
import { useAuth } from "@/lib/auth";

function OnlineIndicator({ is_online }: { is_online: boolean }) {
  return (
    <span
      className={`inline-block h-2 w-2 rounded-full ${
        is_online ? "bg-green-500" : "bg-gray-300"
      }`}
      title={is_online ? "Online" : "Offline"}
    />
  );
}

function WorkingHoursBadge({ is_within }: { is_within: boolean }) {
  return (
    <span
      className={`inline-block rounded-full px-2 py-0.5 text-xs font-medium ${
        is_within
          ? "bg-green-100 text-green-700"
          : "bg-gray-100 text-gray-500"
      }`}
    >
      {is_within ? "Within hours" : "Outside hours"}
    </span>
  );
}

export default function DevelopersPage() {
  const { user } = useAuth();
  const queryClient = useQueryClient();
  const [deleteId, setDeleteId] = useState<string | null>(null);

  const { data, isLoading, error } = useQuery({
    queryKey: ["developers"],
    queryFn: () => developers.list(),
  });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => developers.delete(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["developers"] });
      setDeleteId(null);
    },
  });

  useEffect(() => {
    const interval = setInterval(() => {
      presence.heartbeat().catch(() => {});
    }, 60_000);
    presence.heartbeat().catch(() => {});
    return () => clearInterval(interval);
  }, []);

  const isAdmin = user?.role === "admin";

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <h1 className="text-2xl font-bold">Developers</h1>
        {isAdmin && (
          <Link
            href="/developers/new"
            className="rounded bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700"
          >
            + New Developer
          </Link>
        )}
      </div>

      {isLoading && (
        <div className="space-y-3">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className="h-16 animate-pulse rounded-lg bg-gray-100"
            />
          ))}
        </div>
      )}
      {error && (
        <div className="rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-600">
            {error instanceof Error ? error.message : "Failed to load developers"}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="mt-2 text-sm font-medium text-red-700 hover:underline"
          >
            Retry
          </button>
        </div>
      )}

      {data && data.length === 0 && (
        <div className="rounded-lg border border-gray-200 bg-white p-8 text-center">
          <p className="text-sm text-gray-500">No developers yet.</p>
        </div>
      )}

      {deleteId && (
        <div className="mb-4 rounded-lg border border-red-200 bg-red-50 p-4">
          <p className="text-sm text-red-700">
            Are you sure you want to delete this developer? This action cannot be undone.
          </p>
          <div className="mt-3 flex gap-2">
            <button
              onClick={() => deleteMutation.mutate(deleteId)}
              disabled={deleteMutation.isPending}
              className="rounded bg-red-600 px-3 py-1.5 text-xs font-medium text-white hover:bg-red-700 disabled:opacity-50"
            >
              {deleteMutation.isPending ? "Deleting..." : "Yes, delete"}
            </button>
            <button
              onClick={() => setDeleteId(null)}
              className="rounded border border-gray-300 bg-white px-3 py-1.5 text-xs font-medium text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {data && data.length > 0 && (
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Email</th>
                <th className="px-4 py-3 font-medium">Timezone</th>
                <th className="px-4 py-3 font-medium">Local Time</th>
                <th className="px-4 py-3 font-medium">Working Hours</th>
                <th className="px-4 py-3 font-medium">Availability</th>
                {isAdmin && <th className="px-4 py-3 font-medium"></th>}
              </tr>
            </thead>
            <tbody>
              {data.map((dev) => (
                <tr
                  key={dev.id}
                  className="border-b border-gray-100 hover:bg-gray-50"
                >
                  <td className="px-4 py-3">
                    <OnlineIndicator is_online={dev.is_online} />
                  </td>
                  <td className="px-4 py-3 font-medium">{dev.name}</td>
                  <td className="px-4 py-3 text-gray-600">{dev.email}</td>
                  <td className="px-4 py-3 text-gray-600">{dev.timezone}</td>
                  <td className="px-4 py-3 font-mono text-sm text-gray-700">
                    {dev.local_time || "\u2014"}
                  </td>
                  <td className="px-4 py-3 text-gray-500">
                    {dev.working_hours_start && dev.working_hours_end
                      ? `${dev.working_hours_start} \u2013 ${dev.working_hours_end}`
                      : "\u2014"}
                  </td>
                  <td className="px-4 py-3">
                    <WorkingHoursBadge is_within={dev.is_within_working_hours} />
                  </td>
                  {isAdmin && (
                    <td className="px-4 py-3">
                      <button
                        onClick={() => setDeleteId(dev.id)}
                        className="text-xs text-red-500 hover:text-red-700"
                      >
                        Delete
                      </button>
                    </td>
                  )}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
