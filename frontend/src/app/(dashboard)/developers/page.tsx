"use client";

import { useEffect } from "react";
import { useQuery } from "@tanstack/react-query";
import { developers, presence } from "@/lib/api";

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
  const { data, isLoading, error } = useQuery({
    queryKey: ["developers"],
    queryFn: () => developers.list(),
  });

  useEffect(() => {
    const interval = setInterval(() => {
      presence.heartbeat().catch(() => {});
    }, 60_000);
    presence.heartbeat().catch(() => {});
    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Developers</h1>

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
                    {dev.local_time || "—"}
                  </td>
                  <td className="px-4 py-3 text-gray-500">
                    {dev.working_hours_start && dev.working_hours_end
                      ? `${dev.working_hours_start} – ${dev.working_hours_end}`
                      : "—"}
                  </td>
                  <td className="px-4 py-3">
                    <WorkingHoursBadge is_within={dev.is_within_working_hours} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
