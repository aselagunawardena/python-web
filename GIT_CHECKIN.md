# GitHub Checkin Commands

## Quick Steps to Push Code to GitHub

### 1. Check the status of your changes
```bash
git status
```

### 2. Stage all changes
```bash
git add .
```

### 3. Commit with a descriptive message
```bash
git commit -m "Add About page with routes examples and fix localhost links for deployment"
```

### 4. Push to GitHub
```bash
git push
```

### Or combine steps 2-4:
```bash
git add . && git commit -m "Add About page with routes examples and fix localhost links for deployment" && git push
```

---

## If pushing for the first time to this branch:
```bash
git push -u origin main
```
(Replace `main` with your branch name if different)

---

## If you need to set up Git first:
```bash
git config user.name "Your Name"
git config user.email "your.email@example.com"
```

---

## Common Commands Reference

| Command | Purpose |
|---------|---------|
| `git status` | See which files have changed |
| `git add .` | Stage all changes |
| `git add <filename>` | Stage specific file |
| `git commit -m "message"` | Commit staged changes |
| `git push` | Push commits to GitHub |
| `git pull` | Get latest changes from GitHub |
| `git log` | View commit history |
