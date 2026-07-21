"use client";

import { useRef, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { developers, type Developer } from "@/lib/api";

interface DeveloperMultiSelectProps {
  selectedIds: string[];
  onChange: (ids: string[]) => void;
}

export function DeveloperMultiSelect({
  selectedIds,
  onChange,
}: DeveloperMultiSelectProps) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState("");
  const containerRef = useRef<HTMLDivElement>(null);

  const { data: allDevs = [], isLoading } = useQuery({
    queryKey: ["developers"],
    queryFn: () => developers.list(),
  });

  const filtered = allDevs.filter(
    (d) =>
      d.name.toLowerCase().includes(search.toLowerCase()) ||
      d.timezone.toLowerCase().includes(search.toLowerCase()) ||
      (d.working_hours_start && d.working_hours_start.includes(search)) ||
      (d.working_hours_end && d.working_hours_end.includes(search))
  );

  const selected = allDevs.filter((d) => selectedIds.includes(d.id));

  const toggle = (id: string) => {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((i) => i !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  };

  const remove = (id: string) => {
    onChange(selectedIds.filter((i) => i !== id));
  };

  if (isLoading) {
    return <p className="text-xs text-gray-500">Loading developers...</p>;
  }

  if (allDevs.length === 0) {
    return <p className="text-xs text-gray-500">No developers available.</p>;
  }

  return (
    <div ref={containerRef} className="relative">
      {selected.length > 0 && (
        <div className="mb-2 flex flex-wrap gap-1">
          {selected.map((dev) => (
            <span
              key={dev.id}
              className="inline-flex items-center gap-1 rounded bg-blue-100 px-2 py-0.5 text-xs text-blue-800"
            >
              {dev.name}
              <button
                type="button"
                onClick={() => remove(dev.id)}
                className="ml-0.5 rounded hover:bg-blue-200"
                aria-label={`Remove ${dev.name}`}
              >
                &times;
              </button>
            </span>
          ))}
        </div>
      )}

      <button
        type="button"
        onClick={() => setOpen(!open)}
        className="w-full rounded border border-gray-300 bg-white px-3 py-2 text-left text-sm hover:border-gray-400 focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
      >
        {selected.length === 0
          ? "Select developers..."
          : `${selected.length} selected`}
        <span className="float-right text-gray-400">{open ? "\u25B2" : "\u25BC"}</span>
      </button>

      {open && (
        <div className="absolute z-10 mt-1 w-full rounded border border-gray-200 bg-white shadow-lg">
          <div className="border-b border-gray-100 p-2">
            <input
              type="text"
              placeholder="Search developers..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full rounded border border-gray-300 px-2 py-1 text-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
              autoFocus
            />
          </div>
          <ul className="max-h-48 overflow-y-auto">
            {filtered.map((dev) => {
              const isSelected = selectedIds.includes(dev.id);
              return (
                <li key={dev.id}>
                  <button
                    type="button"
                    onClick={() => toggle(dev.id)}
                    className={`flex w-full items-center gap-2 px-3 py-2 text-left text-sm hover:bg-gray-50 ${
                      isSelected ? "bg-blue-50" : ""
                    }`}
                  >
                    <span
                      className={`flex h-4 w-4 items-center justify-center rounded border ${
                        isSelected
                          ? "border-blue-600 bg-blue-600 text-white"
                          : "border-gray-300"
                      }`}
                    >
                      {isSelected && (
                        <svg
                          className="h-3 w-3"
                          fill="none"
                          viewBox="0 0 24 24"
                          stroke="currentColor"
                          strokeWidth={3}
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            d="M5 13l4 4L19 7"
                          />
                        </svg>
                      )}
                    </span>
                    <span className="flex-1">{dev.name}</span>
                    <span className="text-xs text-gray-400">
                      {dev.timezone}
                      {dev.working_hours_start && dev.working_hours_end
                        ? ` · ${dev.working_hours_start.slice(0, 5)}–${dev.working_hours_end.slice(0, 5)}`
                        : ""}
                    </span>
                  </button>
                </li>
              );
            })}
            {filtered.length === 0 && (
              <li className="px-3 py-2 text-sm text-gray-500">
                No matching developers.
              </li>
            )}
          </ul>
        </div>
      )}
    </div>
  );
}
