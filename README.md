# FrappeTrack

FrappeTrack is a desktop-based time tracking application built using **Frappe**, **ERPNext**, and **Electron**.

The app allows users to track time spent on tasks directly from their desktop with simple **Start, Pause, and Stop** controls. While tracking is active, the application captures screenshots at random intervals to provide work context and transparency.

Once tracking is stopped, the recorded time, selected task details, and captured screenshots are automatically synced to **ERPNext Timesheets**, ensuring accurate and centralized time records.

FrappeTrack is designed for teams and organizations that use ERPNext and need a seamless, secure, and efficient way to monitor task-based work time, with future support for activity tracking and productivity insights.

--- 

## High-Level Architecture
![FrappeTrack HLD](Frappe%20Tracker/high-level-arch.png)
---

## Backend API
- Authentication validation APIs
- Task & Timesheet fetch APIs
- Timesheet creation/update API
- Screenshot upload & attachment handling
  
---

## Frontend (User Interface)
1. Login Screen

![FrappeTrack Login](Frappe%20Tracker/loginui.png)

2. Main Screen

![FrappeTrack Login](Frappe%20Tracker/Timetracker.png)

3. More ui Image (Coming Soon)

---

## 🚀 API Development Progress

1. Authentication & User
    - [X] POST /auth/login – Login API
    - [X] POST /auth/logout - Logout API 
    - [X] GET /user/profile – Get Profile API

2. Project Management
    - [X] GET/POST /projects – Project API
    - [X] GET /projects/{id}/tasks – Get Task by project ID

3. Task & Productivity
    - [X] GET/POST /tasks – Task API
    - [X] GET /activity - Activity API  
    - [X] POST /timetracker – Timetracker API
