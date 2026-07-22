# GetDomus Team Task Manager

Task management app for distributed engineering teams. Supports multi-developer assignment, timezone awareness, and role-based access control.


<!-- SCREENSHOT: dashboard-overview
     What to capture: Full dashboard showing stats cards, task list, sidebar navigation
     Suggested size: 1280x800
-->

## Documentation

### [User Guide →](user-guide/index.md)

Walkthroughs for using the app, organized by role:

- [Manager Workflow](user-guide/manager.md) — Create tasks, assign developers, track progress
- [Developer Workflow](user-guide/developer.md) — View assigned tasks, update status
- [Admin Workflow](user-guide/admin.md) — Manage team members, configure settings
- [Dashboard](user-guide/dashboard.md) — Understanding the overview

### [Technical Guide →](technical/index.md)

Setup, architecture, and development reference:

- [Local Setup](technical/setup.md) — Get the app running locally
- [Testing](technical/testing.md) — Run and write tests
- [Contributing](technical/contributing.md) — Code conventions and workflow
- [Deployment](technical/deployment.md) — Production setup
- [Architecture](technical/architecture.md) — System design + diagrams
- [Decisions](technical/decisions.md) — Key technical choices
- [API Reference](technical/api/reference.md) — Auto-generated endpoint documentation

!!! note
    The **API Reference** is included within the
    [Technical Guide](technical/api/reference.md).
    Interactive Swagger docs are also available at `<backend-url>/docs` when the server is running.

## Quick Start

```bash
# Clone and setup
git clone https://github.com/bigmikecreates/getdomus_team_task_manager.git
cd getdomus_team_task_manager

# Start database
docker compose up -d

# Setup backend
pip install -e ".[dev]"
alembic upgrade head
python -m backend.seed
uvicorn backend.main:app --reload

# Setup frontend (separate terminal)
cd frontend && npm install && npm run dev
```

Open [http://localhost:3000](http://localhost:3000)

See the [full setup guide](technical/setup.md) for detailed instructions.

