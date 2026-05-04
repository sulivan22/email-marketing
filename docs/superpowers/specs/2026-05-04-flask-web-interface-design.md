---
name: Flask Web Interface for Email Marketing
description: Design for adding a Flask web UI to manage templates, contacts, previews, and view sending statistics/history
type: project
---

# Flask Web Interface for Email Marketing

## Overview

Add a Flask web application that provides a user-friendly interface for the existing email marketing script. The web app allows uploading templates and contact lists, previewing emails before sending, and viewing statistics and history of past sends.

**Stack:** Flask + HTML/CSS/JS (no separate APIs), running on `localhost:5000`  
**Data storage:** Existing `.log` files (no database)  
**Execution model:** Flask calls `enviar_newsletter.py` as a background process

---

## Architecture

### Two-Layer Design

1. **Backend: Flask App (`app.py`)**
   - Serves HTML templates and handles forms
   - Manages file uploads (templates, contact lists)
   - Reads and parses `.log` files for statistics
   - Launches `enviar_newsletter.py` as background subprocess
   - Returns status/progress to frontend

2. **Script: `enviar_newsletter.py` (unchanged)**
   - Core SMTP sending logic remains the same
   - Called by Flask as `subprocess` in background
   - Continues to write `enviados.log` and `errores.log`

### Why This Approach

- **Non-blocking:** Flask UI stays responsive while emails are sending
- **Minimal changes:** Existing script works unchanged
- **Simple:** No database, no complex state management
- **Local-only:** Perfect for single-user, localhost setup

---

## Directory Structure

```
EMAILMARKETING/
├── enviar_newsletter.py              # Original SMTP script (unchanged)
├── app.py                            # Flask application
├── requirements.txt                  # Updated: +Flask
├── .env                              # SMTP config (existing)
│
├── templates/                        # Flask HTML templates
│   ├── base.html                     # Base layout with navbar
│   ├── index.html                    # Dashboard (upload + history)
│   ├── preview.html                  # Email preview page
│   └── history.html                  # Detailed history view
│
├── static/                           # CSS and JavaScript
│   ├── style.css                     # Styling
│   └── script.js                     # Form validation, interactivity
│
├── uploads/                          # Temporary uploaded files
│   ├── templates/                    # User-uploaded HTML templates
│   └── contacts/                     # User-uploaded contact TXT files
│
├── app.html                          # Default template (existing)
├── mails.txt                         # Default contacts (existing)
├── enviados.log                      # Sent emails log (existing)
├── errores.log                       # Errors log (existing)
│
├── docs/                             # Documentation
│   └── superpowers/
│       └── specs/
│           └── 2026-05-04-flask-web-interface-design.md  # This file
│
└── contactos/                        # Legacy contact files (existing)
```

---

## Core Features

### 1. Dashboard (`GET /`)
- **Left panel:** Upload form
  - Template HTML file (optional, defaults to `app.html`)
  - Contact list TXT file (optional, defaults to `mails.txt`)
  - Batch size and batch delay sliders (read from `.env`, editable in form)
- **Right panel:** Quick stats
  - Total sent (this session)
  - Total errors (this session)
  - Last send timestamp

### 2. Preview (`POST /preview`)
- User submits template + contacts
- Flask renders the email preview for the first contact
- Shows: subject, sender, and HTML preview
- Option to "Send Now" or go back

### 3. Send Process (`POST /send`)
- Validates inputs (template exists, contacts non-empty)
- Launches `enviar_newsletter.py` as background process
- Returns immediate success response (email sending happens in background)
- Redirects to status page
- **No blocking:** user can continue browsing or close tab

### 4. Status Page (`GET /status`)
- Polls `enviados.log` and `errores.log` in real-time
- Shows:
  - Emails sent so far (current batch)
  - Emails failed so far
  - Current batch progress
  - "Sending in progress..." message while subprocess runs
  - Refresh button (manual) or auto-refresh via JavaScript

### 5. History (`GET /history`)
- Parses all `.log` files (cumulative)
- Displays table:
  - Date/time of each send
  - Number sent
  - Number failed
  - List of failed emails (if any)
  - Success rate %
- Sortable by date (newest first by default)
- Search/filter by email or date range (optional enhancement)

---

## Data Flow

```
User Access localhost:5000
    ↓
Flask renders dashboard (index.html)
    ↓
User uploads template.html + contacts.txt
    ↓
POST /preview
    ↓
Flask renders email preview (first contact)
    ↓
User clicks "Send Now"
    ↓
POST /send
    ↓
Flask validates inputs → launches subprocess: python enviar_newsletter.py
    ↓
Flask returns "Sending started" → redirects to /status
    ↓
subprocess sends emails in background, writes to enviados.log + errores.log
    ↓
User visits /history anytime
    ↓
Flask reads & parses .log files, displays statistics
```

---

## Log Parsing Logic

### `enviados.log` Format (existing)
```
--- Envío 20260504_120000 ---
user1@example.com
user2@example.com
user3@example.com
```

### `errores.log` Format (existing)
```
--- Errores 20260504_120030 ---
invalid@.com
user4@example.com
```

### Parser Responsibilities
- Extract timestamp from "--- Envío YYYYMMDD_HHMMSS ---" lines
- Count emails sent in each batch
- Count emails failed in each batch
- Aggregate: total sent, total errors, success rate
- Display in readable table format

---

## Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Dashboard (upload forms + quick stats) |
| `/preview` | POST | Preview email before sending |
| `/send` | POST | Launch send subprocess |
| `/status` | GET | Real-time progress page |
| `/history` | GET | View all past sends (from logs) |
| `/static/<file>` | GET | CSS, JS files |

---

## Templates & Components

### `base.html`
- Header with app title
- Navigation menu (Dashboard, History, Status)
- `{% block content %}` for page-specific content
- Footer with version/info

### `index.html`
- Form: template upload, contact upload, batch settings
- Button: "Preview" (validates → shows preview.html)
- Quick stats box (sent/failed this session)

### `preview.html`
- Displays preview of email (template + first contact name)
- Shows: subject, from, to, HTML body
- Buttons: "Send Now" or "Back"

### `history.html`
- Table of all past sends (parsed from logs)
- Columns: date, sent, failed, success %, details
- Sortable, searchable (optional)

---

## Error Handling

- **Missing template:** show error, suggest using default
- **Invalid email list:** show count of valid/invalid, ask to proceed with valid only
- **SMTP error during send:** captured by `enviar_newsletter.py` (unchanged), logged to `errores.log`, visible in `/status` and `/history`
- **File upload errors:** show friendly message, suggest checking file format

---

## Environment & Configuration

**From `.env` (read by Flask + script):**
- `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`
- `EMAIL_FROM_NAME`, `EMAIL_FROM_ADDRESS`, `EMAIL_SUBJECT`
- `BATCH_SIZE`, `BATCH_DELAY_SECONDS`
- `MAIL_LIST_FILE` (default: `mails.txt`)
- `HTML_TEMPLATE_FILE` (default: `app.html`)

**Flask-specific:**
- Secret key for session management (auto-generated or from `.env`)
- Upload folder: `uploads/`
- Max upload file size: 10MB (reasonable for templates/contacts)

---

## Technology Decisions

| Decision | Reason |
|----------|--------|
| Flask over Django | Simple, no overkill, fast to develop |
| No separate API | User wants traditional server-rendered HTML |
| Subprocess for sending | Non-blocking, better UX |
| `.log` files, no DB | Keeps setup simple, uses existing logs |
| HTML/CSS/JS (no frameworks) | Minimal dependencies, lightweight |
| `localhost:5000` only | Single-user, local development |

---

## Success Criteria

✅ User can upload template and contacts via web UI  
✅ User can preview email before sending  
✅ Email sends in background without blocking UI  
✅ User can view sending progress in real-time  
✅ User can see complete history of all sends with stats  
✅ App runs on `localhost:5000` with Flask  
✅ Uses existing `.env` for SMTP config  
✅ Existing `enviar_newsletter.py` works unchanged  
✅ All logs read from `enviados.log` and `errores.log`  

---

## Implementation Phases

**Phase 1: Core MVP**
- `app.py` basic structure with Flask
- Dashboard (index.html) with upload forms
- Preview route and template
- "Send" route that launches subprocess
- Basic status page

**Phase 2: History & Stats**
- Log parser utility
- History page with table
- Statistics aggregation

**Phase 3: Polish (Optional)**
- Auto-refresh on status page
- Search/filter in history
- CSS styling refinements
- Mobile-responsive design

---

## Files to Create

- `app.py` — Flask application
- `templates/base.html`, `index.html`, `preview.html`, `history.html`
- `static/style.css`, `static/script.js`
- `uploads/templates/.gitkeep`, `uploads/contacts/.gitkeep`
- Update `requirements.txt` with Flask

---

## Files to Modify

- `requirements.txt` — add Flask
- `.env` — (no changes, but Flask will read from it)

---

## Files to Keep Unchanged

- `enviar_newsletter.py` — core script, no modifications
- `app.html`, `mails.txt`, `enviados.log`, `errores.log`
- `contactos/` directory

---

## Scope Notes

- **Out of scope:** user authentication, multi-user support, persistent database, scheduled sends (for now)
- **Focus:** simple, clean interface for the core workflow: upload → preview → send → view history

