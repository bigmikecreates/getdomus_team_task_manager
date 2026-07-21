import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, it, expect, vi } from "vitest";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn() }),
}));

vi.mock("@/lib/auth", () => ({
  useAuth: () => ({
    register: vi.fn().mockResolvedValue(undefined),
    user: null,
    loading: false,
    login: vi.fn(),
    logout: vi.fn(),
  }),
}));

import RegisterPage from "@/app/(auth)/register/page";

describe("Register page", () => {
  it("renders email and password fields", () => {
    render(<RegisterPage />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
  });

  it("renders create account button", () => {
    render(<RegisterPage />);
    expect(
      screen.getByRole("button", { name: /create account/i })
    ).toBeInTheDocument();
  });

  it("renders link to login page", () => {
    render(<RegisterPage />);
    expect(screen.getByText(/sign in/i)).toHaveAttribute("href", "/login");
  });

  it("allows user to type email and password", async () => {
    const user = userEvent.setup();
    render(<RegisterPage />);

    await user.type(screen.getByLabelText(/email/i), "new@example.com");
    await user.type(screen.getByLabelText(/password/i), "secure123");

    expect(screen.getByLabelText(/email/i)).toHaveValue("new@example.com");
    expect(screen.getByLabelText(/password/i)).toHaveValue("secure123");
  });
});
