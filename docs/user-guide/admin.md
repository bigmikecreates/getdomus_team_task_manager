# Admin Workflow

As an admin, you have full access to all features including user and developer management.

<!-- SCREENSHOT: admin-dashboard
     What to capture: Dashboard view after logging in as admin (full nav visible)
     Suggested size: 1280x800
-->

## All Manager Features

Admins can do everything a manager can:

- [Create and manage tasks](manager.md#creating-a-task)
- [Assign developers](manager.md#assigning-developers)
- [Track progress](manager.md#tracking-progress)

In addition, admins can manage the team.

## Adding a Developer

<!-- SCREENSHOT: create-developer-form
     What to capture: Developer creation form with name, email, timezone, working hours
     Suggested size: 1280x800
-->

1. Navigate to **Developers** from the sidebar
2. Click **+ New Developer**
3. Fill in the details:
   - **Name** (required)
   - **Email** (required)
   - **Timezone** — IANA timezone (e.g., `America/New_York`)
   - **Working Hours** — Optional start/end times for availability tracking
4. Click **Create Developer**

## Deleting a Developer

1. Navigate to **Developers** from the sidebar
2. Click the **Delete** button (X) on the developer's row
3. Confirm the deletion in the dialog

!!! warning
    Deleting a developer will remove them from all task assignments.

## Managing Users

User accounts are created through the registration process. Admins can manage access by:

- Creating new accounts with specific roles
- Using the test accounts provided in the seed data

### Default Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full access: manage users, developers, tasks |
| **Manager** | Create/edit tasks, assign developers |
| **Developer** | View tasks, update status on assigned tasks |
