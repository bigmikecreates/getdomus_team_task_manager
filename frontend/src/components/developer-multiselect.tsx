"use client";

import { useQuery } from "@tanstack/react-query";
import { developers } from "@/lib/api";

interface DeveloperMultiSelectProps {
  selectedIds: string[];
  onChange: (ids: string[]) => void;
}

export function DeveloperMultiSelect({
  selectedIds,
  onChange,
}: DeveloperMultiSelectProps) {
  const { data, isLoading } = useQuery({
    queryKey: ["developers"],
    queryFn: () => developers.list(),
  });

  const toggle = (id: string) => {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((i) => i !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  };

  if (isLoading) {
    return <p className="text-xs text-gray-500">Loading developers...</p>;
  }

  if (!data || data.length === 0) {
    return <p className="text-xs text-gray-500">No developers available.</p>;
  }

  return (
    <div className="space-y-1">
      {data.map((dev) => (
        <label
          key={dev.id}
          className="flex cursor-pointer items-center gap-2 rounded px-2 py-1 hover:bg-gray-50"
        >
          <input
            type="checkbox"
            checked={selectedIds.includes(dev.id)}
            onChange={() => toggle(dev.id)}
            className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
          />
          <span className="text-sm">{dev.name}</span>
          <span className="text-xs text-gray-400">{dev.timezone}</span>
        </label>
      ))}
    </div>
  );
}
