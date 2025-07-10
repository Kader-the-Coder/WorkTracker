# WorkTracker – Design Document

This document outlines the architecture, core features, data models, user flows, and implementation plan for WorkTracker — a multi-user time tracking app with real-time UI and session management.

---

## Table of Contents

1. [Core Features](#1-core-features)  
2. [User Authentication & Authorization](#2-user-authentication--authorization)  
3. [API / Route Specifications](#3-api--route-specifications)  
4. [Session Lifecycle & State Transitions](#4-session-lifecycle--state-transitions)  
5. [File Structure](#5-file-structure)  
6. [Error Handling & Validation](#6-error-handling--validation)  
7. [Security Considerations](#7-security-considerations)  
8. [Testing Strategy](#8-testing-strategy)  
9. [Deployment Plan](#9-deployment-plan)  
10. [Performance Considerations](#10-performance-considerations)  
11. [Versioned Checklist](#versioned-checklist)

---

# 1. Core Features

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

## 5. File Structure

```text
WorkTracker/
├── docs/
│   └── DESIGN.md
├── static/
│   ├── style.css
│   └── script.js
├── templates/
│   ├── index.html
│   ├── projects.html
│   ├── project_detail.html
├── tests/
│   └── test_projects.py
├── views/
│   ├── __init__.py
│   ├── projects.py
│   └── sessions.py
├── app.py
├── config.py
├── models.py
├── utils.py
├── requirements.txt
├── .gitignore
├── README.md
└── LICENSE

```
---

## 6. Error Handling & Validation

- Validate all form inputs (e.g., project name required, valid color hex codes)
- Prevent starting timer if another is already active for the project
- Handle database errors gracefully (with user-friendly error pages or flash messages)
- Confirm destructive actions like session deletion
- Return appropriate HTTP status codes and messages for API endpoints

---

## 7. Security Considerations

- Hash passwords securely (bcrypt or similar)
- Protect all POST endpoints with CSRF tokens
- Use Flask-Login to manage user sessions securely
- Validate and sanitize all user inputs to prevent injection
- Limit file upload size if any uploads added in future
- Use HTTPS in deployment to protect data in transit

---

## 8. Testing Strategy

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

## 9. Deployment Plan

- Target deployment on a platform like Heroku, DigitalOcean, or AWS
- Use environment variables to store secrets and config
- Use a production-grade WSGI server (e.g., Gunicorn)
- Automate deployments with CI/CD pipeline
- Set up HTTPS with Let’s Encrypt or platform managed certificates

---

## 10. Performance Considerations

- Cache generated CSS or static assets to reduce load
- Optimize database queries, add indexes on user/project/session IDs
- Limit concurrent active timers per user to prevent abuse
- Consider moving to a more scalable DB if user base grows

---

# Versioned Checklist

### v0.0.0 – Repository Initialized
- [X] Create project folder and initialize Git repository  
- [X] Create `README.md`, `requirements.txt`, and `.gitignore`  
- [X] Create [project structure](#5-file-structure) 
- [ ] Add basic Flask app (`app.py`)  

---

### v0.1.0 – Project and Time Schema + Add Project Form
- [ ] Define database schema: `projects`, `time_entries`, and `users` tables  
- [ ] Create `init_db()` in `models.py`  
- [ ] Create "Add Project" form (name, color, description)  
- [ ] Store new projects in database  
- [ ] Display list of projects  

---

### v0.2.0 – Timer Start/Stop Logic
- [ ] Add start/stop timer endpoint (POST)  
- [ ] Ensure only one active timer per project  
- [ ] Create `time_entries` on start, update `end_time` on stop  
- [ ] Show current total tracked time per project in list  
- [ ] Add `⏱ Active` indicator for running timers  

---

### v0.3.0 – Live Time Updates
- [ ] Create `static/script.js`  
- [ ] Implement real-time DOM update for `<span class="tracked-time">`  
- [ ] Poll active timers every second  
- [ ] Format time as `HHh MMm SSs`  

---

### v0.4.0 – Dynamic Color Styling
- [ ] Generate `/generated/colors.css` dynamically  
- [ ] Apply project colors via CSS classes (e.g. `.project-red`)  
- [ ] Update `<select>` options to reflect color styles  

---

### v0.5.0 – View Sessions Per Project
- [ ] Create a route to view sessions for a given project  
- [ ] Display session name, start time, end time, and duration  
- [ ] Link from project list to session view  

---

### v0.6.0 – Edit/Delete Sessions
- [ ] Add "edit" button per session (name/description only)  
- [ ] Add "delete" button to remove session  
- [ ] Confirm before deleting  

---

### v0.7.0 – Date Filtering
- [ ] Allow filtering sessions by date range  
- [ ] Add UI date picker or manual form input  
- [ ] Calculate filtered total time  

---

### v0.8.0 – Export to CSV
- [ ] Add export button on project/session view  
- [ ] Generate and download CSV of sessions  
- [ ] Include duration, project name, date, notes  

---

### v0.9.0 – Responsive UI
- [ ] Add basic mobile responsiveness  
- [ ] Improve layout spacing and input scaling  
- [ ] Test across viewport sizes  

---

### v1.0.0 – Basic Authentication (Optional)
- [ ] Add user registration and login system  
- [ ] Associate projects and sessions with user ID  
- [ ] Require login to access project data  

