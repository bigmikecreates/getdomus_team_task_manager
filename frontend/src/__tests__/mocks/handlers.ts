import { http, HttpResponse } from "msw";

const mockUser = {
  id: "user-1",
  email: "admin@example.com",
  role: "admin",
  developer_id: null,
  created_at: "2026-01-01T00:00:00Z",
};

const mockToken = {
  access_token: "mock-jwt-token",
  token_type: "bearer",
};

export const handlers = [
  http.post("*/api/auth/login", () => {
    return HttpResponse.json(mockToken);
  }),

  http.post("*/api/auth/register", () => {
    return HttpResponse.json(mockUser, { status: 201 });
  }),

  http.get("*/api/auth/me", ({ request }) => {
    const auth = request.headers.get("Authorization");
    if (!auth || !auth.startsWith("Bearer ")) {
      return HttpResponse.json(
        { detail: "Could not validate credentials" },
        { status: 401 }
      );
    }
    return HttpResponse.json(mockUser);
  }),

  http.get("*/api/tasks", () => {
    return HttpResponse.json({ tasks: [], total: 0 });
  }),

  http.get("*/api/developers", () => {
    return HttpResponse.json({ developers: [], total: 0 });
  }),
];
