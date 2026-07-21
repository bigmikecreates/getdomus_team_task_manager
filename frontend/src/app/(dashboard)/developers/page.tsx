"use client";

import { useQuery } from "@tanstack/react-query";
import { developers } from "@/lib/api";

export default function DevelopersPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ["developers"],
    queryFn: () => developers.list(),
  });

  return (
    <div>
      <h1 className="mb-6 text-2xl font-bold">Developers</h1>

      {isLoading && (
        <p className="text-sm text-gray-500">Loading developers...</p>
      )}
      {error && (
        <p className="text-sm text-red-600">
          {error instanceof Error ? error.message : "Failed to load developers"}
        </p>
      )}

      {data && (
        <div className="overflow-hidden rounded-lg bg-white shadow">
          <table className="w-full text-left text-sm">
            <thead className="border-b border-gray-200 bg-gray-50">
              <tr>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Email</th>
                <th className="px-4 py-3 font-medium">Timezone</th>
                <th className="px-4 py-3 font-medium">Working Hours</th>
              </tr>
            </thead>
            <tbody>
              {data.map((dev) => (
                <tr
                  key={dev.id}
                  className="border-b border-gray-100 hover:bg-gray-50"
                >
                  <td className="px-4 py-3 font-medium">{dev.name}</td>
                  <td className="px-4 py-3 text-gray-600">{dev.email}</td>
                  <td className="px-4 py-3 text-gray-600">{dev.timezone}</td>
                  <td className="px-4 py-3 text-gray-500">
                    {dev.working_hours_start && dev.working_hours_end
                      ? `${dev.working_hours_start} – ${dev.working_hours_end}`
                      : "—"}
                  </td>
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td
                    colSpan={4}
                    className="px-4 py-8 text-center text-gray-500"
                  >
                    No developers found.
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
