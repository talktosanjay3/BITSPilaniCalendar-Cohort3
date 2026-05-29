# BITS Pilani Calendar — Cohort 3

MSc Data Science & Artificial Intelligence · Trimester 2026

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                        Browser (User)                                │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐          │
│  │ Calendar View │  │ Edit Zoom    │  │ Email Registration│          │
│  │ (read/write)  │  │ Link Panel   │  │ Modal             │          │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘          │
│         │                  │                    │                    │
│         └──────────────────┼────────────────────┘                    │
│                            │ GitHub API (fetch)                      │
└────────────────────────────┼─────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
    ┌───────────────┐  ┌──────────┐  ┌──────────────────┐
    │ data.json     │  │ GH Pages │  │ Workflow Dispatch│
    │ (repo content)│  │ (static) │  │ register-zoom.yml│
    └───────────────┘  └──────────┘  └────────┬─────────┘
                                               │
                                      ┌────────┴─────────┐
                                      │ windows-latest   │
                                      │ runner           │
                                      │                  │
                                      │ 1. Read emails  │
                                      │ 2. Playwright   │
                                      │ 3. Register     │
                                      │ 4. Commit back  │
                                      └──────────────────┘
```

---

## File Structure

```
BITSPilaniCalendar-Cohort3/
├── index.html                    # Single-file calendar portal (CSS + JS embedded)
├── data.json                     # "Database" — Zoom links + email registrations
├── WeekCompo.csv                 # Source schedule (embedded in index.html)
└── .github/
    └── workflows/
        └── register-zoom.yml     # GitHub Action for Zoom registration automation
```

---

## Data Model (data.json)

```json
{
  "zoomLinks": {
    "week-1-2026-05-22-18-30": "https://zoom.us/j/1234567890?pwd=abc123",
    "week-1-2026-05-22-19-45": "https://zoom.us/j/0987654321?pwd=def456",
    ...
  },
  "registrations": [
    {
      "email": "student@bits.ac.in",
      "classKey": "week-1-2026-05-22-18-30",
      "registeredAt": "2026-05-22T10:30:00Z",
      "status": "pending"
    }
  ]
}
```

### Zoom Links Key Format

`week-{weekNumber}-{YYYYMMDD}-{HH-MM}`

Examples:
- `week-1-20260522-18-30` → Week 1, May 22, 6:30 PM
- `week-14-20260822-09-30` → Week 14, Aug 22, 9:30 AM (exam slot)

### Registration Status Values

| Status | Meaning |
|--------|---------|
| `pending` | Submitted, waiting for workflow to process |
| `registered` | Successfully registered on Zoom |
| `failed` | Registration failed (Zoom error, network issue, etc.) |

---

## CSV Data (WeekCompo.csv)

### Source

BITS Pilani Trimester Calendar for MSc DS & AI Cohort 3.

### Columns

| Column | Description |
|--------|-------------|
| Week | Week number (0–14) |
| Component | Type: LIVE CLASS SESSION, GRADED QUIZ, ASSIGNMENT, TRIMESTER EXAMS |
| Start Date | Start date (YYYY-MM-DD) |
| End Date | End date (YYYY-MM-DD) |
| Start Time (IST) | Start time in IST (HH:MM) |
| End Time (IST) | End time in IST (HH:MM) |
| Course | Course name (may be empty for TBA slots) |
| Weightage | Assessment weightage percentage (for quizzes/exams/assignments) |
| Source | Trimester calendar |

### Courses

| Course | Color |
|--------|-------|
| Data Visualization & Storytelling | `#6366f1` (Indigo) |
| Data Pre-processing | `#8b5cf6` (Purple) |
| Statistical Modelling & Inferencing | `#ec4899` (Pink) |
| Feature Engineering | `#f59e0b` (Amber) |

### Event Types

| Type | Color | Badge |
|------|-------|-------|
| Live Class | Accent blue | LIVE |
| Quiz | Slate gray | QUIZ |
| Assignment | Green | ASSIGNMENT |
| Exam | Red | EXAM |
| TBA (empty course) | Gray | TBA |

### Schedule Summary

- **14 weeks** (Week 1–14)
- **Regular sessions**: Fridays & Saturdays, 18:30–19:30, 19:45–20:45, 21:00–22:00 IST
- **Exam slots**: Week 14, 09:30–11:30 and 12:30–14:30
- **Quizzes**: Graded quizzes in Weeks 3, 6, 9 (spanning 3 days)
- **Assignments**: Due Week 8 (extended deadline Aug 8)
- **Empty course slots**: 21:00 slots and some Saturday 18:30 slots show as "TBA"

---

## Application Features

### Calendar Views

#### Weekly View (Default)
- Two-column grid: Friday | Saturday
- Each day shows time-slotted class cards
- Quizzes, assignments, and exams appear in a separate section below
- Current day highlighted with accent border

#### Daily View
- Day-by-day breakdown
- All events for the day listed chronologically
- Useful for detailed planning

### Per-Class Features

| Feature | Description |
|---------|-------------|
| **Join Button** | Clickable Zoom link (appears when link is added) |
| **Register Button** | Opens email registration modal |
| **Edit Button (✎)** | Prompt to add/edit Zoom link |
| **Color dot** | Course identifier |
| **Today highlight** | Accent border on current day's classes |

### Registration Flow

1. User clicks "Register" on a class card
2. Modal opens with class info (course, date, time)
3. User enters email address
4. On submit:
   - Email added to `data.json` with status `pending`
   - `workflow_dispatch` API called with classKey + email
   - GitHub Action triggers on `windows-latest` runner
   - Playwright opens Zoom, fills email, submits
   - Status updated to `registered` or `failed`
   - `data.json` committed back to repo

### Data Persistence

- **Read**: `GET /repos/{owner}/{repo}/contents/data.json` → base64 decode → JSON
- **Write**: `PUT /repos/{owner}/{repo}/contents/data.json` → base64 encode → commit
- SHA token required for writes (optimistic concurrency)
- All changes are versioned in Git history

---

## GitHub Actions Workflow (register-zoom.yml)

### Triggers

| Trigger | When |
|---------|------|
| `workflow_dispatch` | Manually triggered by anyone via UI or API |

### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `classKey` | Yes | — | Class key (e.g., `week-1-2026-05-22-18-30`) |
| `email` | No | — | Email to register (empty = process all pending for class) |

### Runner

`windows-latest` (Windows Server 2022)

### Steps

1. **Checkout repo** — Uses `GH_TOKEN_WORKFLOW` secret
2. **Setup Python 3.12** — Via `actions/setup-python@v5`
3. **Install Playwright** — `pip install playwright` + `playwright install chromium`
4. **Run registration** — Embedded Python script:
   - Reads `data.json`
   - Filters pending registrations for the classKey
   - For each pending email:
     - Opens Chromium via Playwright (headless)
     - Navigates to Zoom URL from `data.json`
     - Fills email input field
     - Fills password if `ZOOM_MEETING_PASSWORD` secret is set
     - Clicks submit
     - Captures result (success/fail)
   - Updates `data.json` with registration status
5. **Commit and push** — Pushes updated `data.json` back to repo

### Secrets Required

| Secret | Purpose |
|--------|---------|
| `GH_TOKEN_WORKFLOW` | Git push access for workflow |
| `ZOOM_MEETING_PASSWORD` | Zoom meeting password (optional, per-class) |

---

## Setup Instructions

### Step 1: Create GitHub Repository

```bash
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

### Step 2: Enable GitHub Pages

1. Go to repository **Settings**
2. Navigate to **Pages**
3. Set **Source** to `main` branch
4. Save — URL will be `https://<your-username>.github.io/<your-repo>/`

### Step 3: Create Fine-Grained PAT

1. Go to **GitHub → Settings → Developer settings → Fine-grained tokens**
2. Click **Generate new token**
3. Configure:
   - **Token name**: `BITS-Calendar-Token`
   - **Expiration**: Choose your preference
   - **Repository access**: Select this repository only
   - **Permissions**:
     - **Contents**: Read & write
     - **Actions**: Read & write
     - **Metadata**: Read-only
4. Generate and copy the token

### Step 4: Add Repository Secrets

Go to **Settings → Secrets and variables → Actions → New repository secret**:

| Secret Name | Value | Used By |
|-------------|-------|---------|
| `GH_TOKEN` | Your fine-grained PAT | Browser (read/write data.json) |
| `GH_TOKEN_WORKFLOW` | Same PAT | GitHub Action (commit back) |
| `ZOOM_MEETING_PASSWORD` | Your Zoom password | Playwright (auto-fill) |

### Step 5: Open the Calendar

Navigate to `https://<your-username>.github.io/<your-repo>/`

1. Paste your PAT in the token field
2. Click **Save & Load**
3. Calendar loads from `data.json` in the repo

---

## User Guide

### Viewing the Calendar

- **Weekly view**: Default grid showing Friday and Saturday columns
- **Daily view**: Toggle to see all days chronologically
- **Today button**: Scrolls to and highlights the current day
- **Legend**: Color-coded course indicators at the top

### Adding a Zoom Link

1. Find the class card
2. Click the ✎ (edit) button
3. Paste the Zoom meeting link in the prompt
4. Link is saved to `data.json` and visible to all users

### Registering for a Class

1. Click **Register** on a live class card
2. Enter your email address
3. Click **Register**
4. Status shows as "✓ Registered"
5. Workflow processes the registration (check workflow runs for status)

### Checking Registration Status

- After clicking Register, the button updates to "✓ Registered"
- To verify actual Zoom registration, check the GitHub Action run logs
- Go to **Actions → Register Zoom** → click the latest run → review logs

---

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Auth model | No password, anyone can edit | Per requirement; token stored in browser localStorage |
| Data storage | `data.json` in repo | Simple, versioned, viewable, no external DB needed |
| Zoom automation | Playwright on `windows-latest` | Per requirement; Windows required for Playwright |
| Zoom URL storage | Per-class in `data.json` | Each class has unique Zoom link |
| Email dedup | Prevents duplicate registrations | Checks existing entries before adding |
| Zoom response | Best-effort detection | No API key; uses DOM inspection |
| View toggle | Weekly (default) + Daily | Per requirement |
| Weeks shown | All 14 weeks | Per requirement |
| Empty courses | Displayed as "TBA" | Per requirement |
| Timezone | IST (hardcoded) | All classes are in IST |

---

## Limitations & Considerations

### Browser Token Security

- The GitHub PAT is stored in `localStorage` (visible in browser DevTools)
- Anyone with the token can read/write `data.json`
- For production use, consider:
  - A dedicated bot account with minimal permissions
  - IP restrictions on the PAT
  - Regular token rotation

### Zoom Registration

- Playwright automation is **best-effort** — Zoom may change their DOM
- No Zoom API key used; relies on UI interaction
- Registration success depends on:
  - Zoom meeting URL being correct
  - Meeting being open for registration
  - No CAPTCHA or additional verification from Zoom
- Always verify in the Zoom dashboard

### GitHub API Rate Limits

- Unauthenticated: 60 requests/hour
- Authenticated: 5,000 requests/hour
- Write operations count toward the limit
- For high-traffic use, consider caching

### Data.json Concurrency

- If multiple users edit simultaneously, last-write-wins
- The SHA check prevents some conflicts but not all
- For multi-user editing, consider GitHub's merge API

---

## Troubleshooting

### "No data in repo yet"
- `data.json` hasn't been committed to the repo yet
- Push the initial `data.json` to the repo

### "Save failed"
- Check your PAT has **Contents: Read & write** permission
- Check the repo name is correctly detected in the URL

### Zoom registration not working
- Check the GitHub Action run logs for errors
- Verify the Zoom URL in `data.json` is correct
- Ensure the meeting allows registration
- Check if `ZOOM_MEETING_PASSWORD` is set if required

### Calendar not loading
- Verify GitHub Pages is enabled
- Check the PAT is saved correctly
- Open DevTools console for error messages

---

## Future Enhancements

- [ ] Zoom API integration (replace Playwright with Zoom API)
- [ ] Email notifications for upcoming classes
- [ ] Browser push notifications
- [ ] Dark/Light theme toggle
- [ ] Export calendar to iCal/Google Calendar
- [ ] Multi-trimester support
- [ ] Attendance tracking
- [ ] Per-user saved preferences
- [ ] Admin role for Zoom link management
