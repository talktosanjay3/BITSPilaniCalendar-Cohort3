# BITS Pilani Calendar — MSc DS & AI Cohort 3

Learning calendar portal for BITS Pilani MSc Data Science & Artificial Intelligence, Cohort 3 (Trimester 2026).

## Features

- 📅 **14-week calendar** — all live classes, quizzes, assignments, and exams
- 🎨 **Color-coded** by course and event type
- 🔗 **Zoom links** — add and share meeting links per class
- 📧 **Email registration** — register for classes, auto-processed via GitHub Actions
- 🔄 **Weekly & Daily views** — toggle between layouts
- 💾 **GitHub-backed** — all data stored in `data.json` in this repo

## Quick Start

### 1. Deploy to GitHub Pages

```bash
git remote add origin git@github.com:<your-username>/<your-repo>.git
git push -u origin main
```

Then enable GitHub Pages: **Settings → Pages → Source: main branch**

### 2. Create a GitHub Token

Go to **Settings → Developer settings → Fine-grained tokens**:
- Grant **Contents: Read & write** and **Actions: Read & write** for this repo
- Copy the token

### 3. Add Secrets

**Settings → Secrets and variables → Actions → New repository secret**:

| Secret | Value |
|--------|-------|
| `GH_TOKEN` | Your PAT |
| `GH_TOKEN_WORKFLOW` | Your PAT |
| `ZOOM_MEETING_PASSWORD` | Your Zoom password |

### 4. Open the Calendar

Visit `https://<your-username>.github.io/<your-repo>/` and paste your token.

## How It Works

```
Browser → GitHub API → data.json (Zoom links + registrations)
                      ↓
              Workflow dispatch → Playwright → Zoom registration
```

- **Add Zoom link**: Click ✎ on any class card → paste URL → auto-saves to repo
- **Register**: Click Register → enter email → GitHub Action auto-registers on Zoom
- **All data persists** in `data.json` committed to the repo

## File Structure

```
├── index.html          # Calendar portal (CSS + JS embedded)
├── data.json           # Zoom links + email registrations
├── WeekCompo.csv       # Source schedule
└── .github/
    └── workflows/
        └── register-zoom.yml  # Zoom registration automation
```

## Courses

| Course | Color |
|--------|-------|
| Data Visualization & Storytelling | Indigo |
| Data Pre-processing | Purple |
| Statistical Modelling & Inferencing | Pink |
| Feature Engineering | Amber |

## Schedule

- **Fridays & Saturdays**: 18:30, 19:45, 21:00 IST
- **Exams**: Week 14, 09:30 & 12:30 IST
- **Quizzes**: Weeks 3, 6, 9 (3-day windows)
- **Assignments**: Due Week 8

## Docs

Full documentation: [DOCS.md](./DOCS.md)

## License

MIT
