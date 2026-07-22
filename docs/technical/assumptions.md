# Assumptions

This document outlines the assumptions made during development and their rationale.

## 1. Single-Workspace Architecture

**Assumption:** The application operates as a single shared workspace with no organization or team scoping beyond role-based access control.

**Rationale:** The specification describes a task management tool for distributed teams with three roles (admin, manager, developer). There is no mention of multi-tenancy, organizations, or workspace isolation. Adding tenant scoping would over-engineer the solution for the stated requirements and introduce unnecessary complexity in the data model, API layer, and authorization logic.

## 2. Three Pre-Seeded Accounts

**Assumption:** The three seeded accounts (`admin@example.com`, `manager@example.com`, `dev@example.com`) are sufficient to demonstrate all role-based functionality.

**Rationale:** Each account represents one of the three RBAC roles defined in the specification. This provides immediate access to all permission levels without requiring the reviewer to register new accounts. New accounts can be created via the registration endpoint, which defaults to the developer role.

## 3. Informational Timezone Display

**Assumption:** Timezone-aware working hours are for informational display only, not for scheduling enforcement or automatic task routing.

**Rationale:** The specification requires timezone awareness and working hours display. It does not require the system to prevent task assignment outside working hours or to automatically route tasks based on timezone overlap. The implementation shows each developer's local time and whether they are within working hours, which satisfies the stated requirement.

## 4. Heartbeat-Based Presence

**Assumption:** A heartbeat-based presence system (frontend pings the backend periodically) is sufficient for indicating online/offline status.

**Rationale:** The specification mentions "online/offline status" as a feature. A full real-time presence system (WebSockets, SSE) would be disproportionate for the scope. Heartbeat tracking provides a reasonable approximation: developers appear online when their browser is active and sending periodic requests, and offline when inactive.

## 5. Seed Data for Demo

**Assumption:** The seed script provides a realistic demo environment with developers across multiple timezones, tasks in various states, and multi-developer assignments.

**Rationale:** A blank application is not useful for demonstrating features. The seed data includes 4 developers across 4 timezones (New York, London, Tokyo, Los Angeles), 8 tasks in different statuses and priorities, and 11 assignments showing multi-developer allocation. This allows the reviewer to immediately see the application in action.

## 6. PostgreSQL as Target Database

**Assumption:** PostgreSQL is the target database for both development and production environments.

**Rationale:** The specification lists PostgreSQL. SQLite is used only for automated tests to keep CI fast and dependency-free. Development uses Docker PostgreSQL for production parity. Production uses Neon (serverless PostgreSQL).

## 7. GitHub as Source of Truth

**Assumption:** The GitHub repository is the source of truth for code review, with CI running on pull requests.

**Rationale:** The specification asks for a Git repository link. GitHub Actions CI ensures all code on `main` has passed backend tests, frontend tests, and frontend build. Branch protection enforces this via required status checks.

## 8. Single-Developer Submission

**Assumption:** This is a single-developer submission. All code, documentation, and deployment was authored by one person.

**Rationale:** The submission is an individual technical assessment. There is no team coordination or code review workflow required beyond the PR-based CI enforcement.
