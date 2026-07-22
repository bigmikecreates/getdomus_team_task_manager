const API_BASE = process.env.NEXT_PUBLIC_API_URL || "";

export interface User {
  id: string;
  email: string;
  role: "admin" | "manager" | "developer";
  developer_id: string | null;
  created_at: string;
}

export interface Developer {
  id: string;
  name: string;
  email: string;
  timezone: string;
  working_hours_start: string | null;
  working_hours_end: string | null;
  created_at: string;
  updated_at: string;
}

export interface DeveloperWithAvailability extends Developer {
  is_online: boolean;
  is_within_working_hours: boolean;
  local_time: string;
}

export interface Task {
  id: string;
  title: string;
  description: string | null;
  status: "todo" | "in_progress" | "in_review" | "done";
  priority: "low" | "medium" | "high" | "critical";
  due_date: string | null;
  created_by: string | null;
  created_at: string;
  updated_at: string;
  developers: Developer[];
}

export interface TaskListResponse {
  tasks: Task[];
  total: number;
}

export interface StatusCount {
  status: string;
  count: number;
}

export interface PriorityCount {
  priority: string;
  count: number;
}

export interface AssigneeCount {
  developer_id: string;
  developer_name: string;
  task_count: number;
}

export interface DashboardStats {
  total_tasks: number;
  by_status: StatusCount[];
  by_priority: PriorityCount[];
  by_assignee: AssigneeCount[];
}

export interface RecentTask {
  id: string;
  title: string;
  status: string;
  priority: string;
}

export interface UpcomingTask {
  id: string;
  title: string;
  status: string;
  priority: string;
  due_date: string | null;
}

export interface DashboardOverview {
  stats: DashboardStats;
  overdue_tasks: number;
  critical_tasks: number;
  critical_tasks_list: UpcomingTask[];
  upcoming_tasks: UpcomingTask[];
  recent_tasks: RecentTask[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  role?: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export interface TaskCreate {
  title: string;
  description?: string;
  status?: string;
  priority?: string;
  due_date?: string;
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  status?: string;
  priority?: string;
  due_date?: string;
}

function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("token");
}

export async function apiFetch<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...((options.headers as Record<string, string>) || {}),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }

  return res.json();
}

export const auth = {
  login: (data: LoginRequest) =>
    apiFetch<TokenResponse>("/api/auth/login", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  register: (data: RegisterRequest) =>
    apiFetch<User>("/api/auth/register", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  me: () => apiFetch<User>("/api/auth/me"),
};

export const tasks = {
  list: () => apiFetch<TaskListResponse>("/api/tasks"),
  get: (id: string) => apiFetch<Task>(`/api/tasks/${id}`),
  create: (data: TaskCreate) =>
    apiFetch<Task>("/api/tasks", { method: "POST", body: JSON.stringify(data) }),
  update: (id: string, data: TaskUpdate) =>
    apiFetch<Task>(`/api/tasks/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id: string) =>
    apiFetch<{ message: string }>(`/api/tasks/${id}`, { method: "DELETE" }),
  assign: (id: string, developerIds: string[]) =>
    apiFetch<{ message: string }>(`/api/tasks/${id}/assign`, {
      method: "POST",
      body: JSON.stringify({ developer_ids: developerIds }),
    }),
  unassign: (taskId: string, developerId: string) =>
    apiFetch<{ message: string }>(`/api/tasks/${taskId}/assignments/${developerId}`, {
      method: "DELETE",
    }),
};

export interface DeveloperCreate {
  name: string;
  email: string;
  timezone?: string;
  working_hours_start?: string;
  working_hours_end?: string;
}

export const developers = {
  list: () => apiFetch<DeveloperWithAvailability[]>("/api/developers"),
  get: (id: string) => apiFetch<Developer>(`/api/developers/${id}`),
  create: (data: DeveloperCreate) =>
    apiFetch<Developer>("/api/developers", { method: "POST", body: JSON.stringify(data) }),
  delete: (id: string) =>
    apiFetch<{ message: string }>(`/api/developers/${id}`, { method: "DELETE" }),
};

export const presence = {
  heartbeat: () =>
    apiFetch<{ status: string }>("/api/presence/heartbeat", {
      method: "POST",
    }),
};

export const dashboard = {
  stats: () => apiFetch<DashboardStats>("/api/dashboard/stats"),
  overview: () => apiFetch<DashboardOverview>("/api/dashboard/overview"),
};
