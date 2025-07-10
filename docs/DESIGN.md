# WorkTracker – Design Document

This document outlines the architecture, core features, data models, user flows, and implementation plan for WorkTracker — a multi-user time tracking app with real-time UI and session management.

---

## 1. Core Features

### 1.1 Project Management
- Add new projects with:
  - Name
  - Color
  - Description
- Total time spent on each project displayed next to it
- Display projects in a list
- Assign each project a distinct text color
- Selecting a project navigates to a submenu where sessions can be created

### 1.2 Sessions
- Start a new session by clicking “Start” on a project or session submenu
- Sessions are named numerically, defined by a prefix (e.g. Task X, or Session X)
- Timer controls per session:
  - Start / Stop session timer
  - Pause session timer to start break timer
  - Resume session timer after break ends
- Modify session start/end times manually

### 1.3 Time Tracking
- One active session per project at a time
- Show tracked time as `HHh MMm SSs`
- Timer updates live in the browser (without page reload)
- All session data stored in a SQLite database

### 1.4 Real-Time UI
- Timer updates every second for active sessions
- Active projects display a badge: `⏱ Active`
- Dynamic project colors via CSS classes and a generated stylesheet

---

## 2. User Authentication & Authorization

- User registration and login system
- Passwords stored securely with hashing (e.g., bcrypt)
- Projects and sessions are scoped to the logged-in user only
- Access control enforced: users see and modify only their data
- Use Flask-Login (or similar) for session management and protection
- CSRF protection on forms (e.g., with Flask-WTF)

---

## 3. API / Route Specifications

| Route                    | Method  | Description                          | Inputs                   | Outputs                         |
|--------------------------|---------|--------------------------------------|--------------------------|---------------------------------|
| `/`                      | GET     | Home page                            | None                     | Renders `index.html`            |
| `/projects`              | GET     | List all projects for logged-in user | None                     | Render list of projects         |
| `/projects`              | POST    | Add a new project                    | name, color, description | Redirect to projects list       |
| `/projects/<id>/start`   | POST    | Start timer for project `<id>`       | None                     | Redirect to projects list       |
| `/projects/<id>/stop`    | POST    | Stop timer for project `<id>`        | None                     | Redirect to projects list       |
| `/projects/<id>/sessions`| GET     | List all sessions for project `<id>` | None                     | Render sessions view            |
| `/sessions/<id>/edit`    | GET/POST| Edit session details                 | name, description, times | Redirect to sessions list       |
| `/sessions/<id>/delete`  | POST    | Delete session                       | None                     | Redirect to sessions list       |
| `/generated/colors.css`  | GET     | Serve dynamically generated CSS      | None                     | CSS stylesheet                  |

---

## 4. Session Lifecycle & State Transitions

| Action         | Result                                                          | Notes                                           |
|----------------|-----------------------------------------------------------------|-------------------------------------------------|
| Start session  | Creates a new session row with `start_time` and `end_time` null | Stops any other active session for that project |
| Pause session  | Sets a break timer; session timer pauses                        | Break timer runs independently                  |
| Resume session | Ends break timer; session timer continues                       | Only one break per session at a time            |
| Stop session   | Sets `end_time` for active session                              | Session is no longer active                     |

- Timers run independently client-side for display, but authoritative time stored in DB
- Conflicts prevented by server checks on start/stop actions

---

## 5. Error Handling & Validation

- Validate all form inputs (e.g., project name required, valid color hex codes)
- Prevent starting timer if another is already active for the project
- Handle database errors gracefully (with user-friendly error pages or flash messages)
- Confirm destructive actions like session deletion
- Return appropriate HTTP status codes and messages for API endpoints

---

## 6. Security Considerations

- Hash passwords securely (bcrypt or similar)
- Protect all POST endpoints with CSRF tokens
- Use Flask-Login to manage user sessions securely
- Validate and sanitize all user inputs to prevent injection
- Limit file upload size if any uploads added in future
- Use HTTPS in deployment to protect data in transit

---

## 7. Testing Strategy

- Unit tests for:
  - Database models and `init_db()` correctness
  - Timer logic (start, pause, resume, stop)
  - Form validation
- Integration tests for:
  - Full request-response cycles (e.g., project creation, timer start/stop)
  - Authentication and authorization flows
- Use pytest + Flask test client
- Mock time functions where possible to test timer accuracy

---

## 8. Deployment Plan

- Target deployment on a platform like Heroku, DigitalOcean, or AWS
- Use environment variables to store secrets and config
- Use a production-grade WSGI server (e.g., Gunicorn)
- Automate deployments with CI/CD pipeline
- Set up HTTPS with Let’s Encrypt or platform managed certificates

---

## 9. Performance Considerations

- Cache generated CSS or static assets to reduce load
- Optimize database queries, add indexes on user/project/session IDs
- Limit concurrent active timers per user to prevent abuse
- Consider moving to a more scalable DB if user base grows

---
