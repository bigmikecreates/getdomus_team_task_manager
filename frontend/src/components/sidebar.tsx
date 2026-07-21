"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/lib/auth";

const navItems = [
  { href: "/", label: "Dashboard" },
  { href: "/tasks", label: "Tasks" },
  { href: "/board", label: "Board" },
  { href: "/developers", label: "Developers" },
];

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  const isActive = (href: string) =>
    href === "/" ? pathname === "/" : pathname.startsWith(href);

  return (
    <aside className="flex w-60 flex-col border-r border-gray-200 bg-white">
      <div className="border-b border-gray-200 p-4">
        <h1 className="text-lg font-bold text-gray-900">GetDomus</h1>
        <p className="text-xs text-gray-500">Task Manager</p>
      </div>

      <nav className="flex-1 p-3">
        {navItems
          .filter((item) => {
            if (item.href === "/developers" && user?.role === "developer") {
              return false;
            }
            return true;
          })
          .map((item) => (
            <Link
              key={item.href}
              href={item.href}
              className={`mb-1 block rounded px-3 py-2 text-sm font-medium ${
                isActive(item.href)
                  ? "bg-blue-50 text-blue-700"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {item.label}
            </Link>
          ))}
      </nav>

      <div className="border-t border-gray-200 p-3">
        <p className="truncate text-xs text-gray-500">{user?.email}</p>
        <p className="text-xs font-medium capitalize text-gray-700">
          {user?.role}
        </p>
        <button
          onClick={logout}
          className="mt-2 w-full rounded px-3 py-1.5 text-left text-xs text-gray-600 hover:bg-gray-100"
        >
          Sign out
        </button>
      </div>
    </aside>
  );
}
