# Git Commands Explained - For Beginners

A complete guide to understanding Git commands with visual examples.

---

## What is Git?

**Git** is version control software - it tracks changes to your code over time.

Think of it like:
- **Google Docs version history** - but for code
- **Time machine** - go back to any previous version
- **Backup system** - your code is safe
- **Collaboration tool** - work with others

---

## The Big Picture

```
┌─────────────────────────────────────────────────────────┐
│  YOUR COMPUTER                                           │
│                                                          │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │  Working     │    │  Git         │                  │
│  │  Directory   │───►│  Repository  │                  │
│  │              │    │  (.git)      │                  │
│  │  Your files  │    │  History     │                  │
│  └──────────────┘    └──────┬───────┘                  │
│                              │                           │
└──────────────────────────────┼───────────────────────────┘
                               │
                               │ git push
                               ▼
                    ┌──────────────────┐
                    │     GITHUB       │
                    │  (Cloud backup)  │
                    │                  │
                    │  Your code       │
                    │  online          │
                    └──────────────────┘
```

---

## Command 1: `git init`

### What it does
Creates a new Git repository in your current folder.

### Plain English
"Hey Git, start tracking changes in this folder"

### What happens
```
Before:
/your-project/
  ├── backend/
  ├── frontend/
  └── README.md

After:
/your-project/
  ├── .git/           ← NEW! Hidden folder with Git data
  ├── backend/
  ├── frontend/
  └── README.md
```

### Visual Analogy
Like creating a new Google Doc - now you can save versions.

### When to use
- Starting a new project
- Want to track changes
- **Only run once per project**

### Example
```bash
cd /Users/vggnanas/Documents/kiro-projects/words
git init

# Output:
# Initialized empty Git repository in /Users/vggnanas/Documents/kiro-projects/words/.git/
```

---

## Command 2: `git add .`

### What it does
Stages all changed files for commit (prepares them to be saved).

### Plain English
"Mark these files to be included in the next save"

### The `.` means
"All files in current directory and subdirectories"

### What happens
```
Working Directory          Staging Area
(Your files)              (Ready to commit)

backend/app.py            
frontend/App.tsx          
README.md                 

      ↓ git add .

backend/app.py            backend/app.py ✓
frontend/App.tsx          frontend/App.tsx ✓
README.md                 README.md ✓
```

### Visual Analogy
Like putting items in a shopping cart before checkout.

### Variations
```bash
git add .                    # Add all files
git add backend/            # Add only backend folder
git add README.md           # Add only README.md
git add *.py                # Add all Python files
```

### Example
```bash
git add .

# No output = success
# Files are now staged
```

### Check what's staged
```bash
git status

# Output shows:
# Changes to be committed:
#   new file:   backend/app.py
#   modified:   README.md
```

---

## Command 3: `git commit -m "message"`

### What it does
Saves a snapshot of all staged files with a description.

### Plain English
"Save these changes with this note about what I did"

### The `-m` means
"Message" - the description of your changes

### What happens
```
Staging Area              Git History
(Ready to commit)         (Saved versions)

backend/app.py ✓          
frontend/App.tsx ✓        
README.md ✓               

      ↓ git commit

                          Commit #1: "Initial commit"
                          - backend/app.py
                          - frontend/App.tsx
                          - README.md
                          Date: 2026-02-06
                          Author: You
```

### Visual Analogy
Like taking a photo - captures the current state forever.

### Good commit messages
```bash
git commit -m "Add user authentication"           # ✅ Clear
git commit -m "Fix CSV import bug"                # ✅ Specific
git commit -m "Update README with setup steps"    # ✅ Descriptive

git commit -m "changes"                           # ❌ Too vague
git commit -m "asdf"                              # ❌ Meaningless
git commit -m "Fixed stuff"                       # ❌ Not specific
```

### Example
```bash
git commit -m "Initial commit - Vocabulary app ready for Amplify"

# Output:
# [main 1a2b3c4] Initial commit - Vocabulary app ready for Amplify
#  42 files changed, 3521 insertions(+)
#  create mode 100644 backend/app.py
#  create mode 100644 frontend/App.tsx
```

---

## Command 4: `git remote add origin URL`

### What it does
Connects your local Git repository to a remote repository (GitHub).

### Plain English
"Link my local code to this GitHub repository"

### Breaking it down
- `git remote` = Manage remote repositories
- `add` = Add a new remote
- `origin` = Name for the remote (convention: always "origin")
- `URL` = GitHub repository URL

### What happens
```
Your Computer                     GitHub
┌──────────────┐                 ┌──────────────┐
│  Local Repo  │                 │  Remote Repo │
│              │                 │              │
│  .git/       │                 │  (empty)     │
└──────────────┘                 └──────────────┘

      ↓ git remote add origin URL

┌──────────────┐                 ┌──────────────┐
│  Local Repo  │────────────────►│  Remote Repo │
│              │   "origin"      │              │
│  .git/       │   points to     │  (empty)     │
└──────────────┘                 └──────────────┘
```

### Visual Analogy
Like adding a contact to your phone - now you can call them.

### Example
```bash
git remote add origin https://github.com/yourusername/vocabulary-app.git

# No output = success
```

### Check remotes
```bash
git remote -v

# Output:
# origin  https://github.com/yourusername/vocabulary-app.git (fetch)
# origin  https://github.com/yourusername/vocabulary-app.git (push)
```

### Common mistake
```bash
# If you already added a remote:
git remote add origin URL
# Error: remote origin already exists

# Fix: Remove and re-add
git remote remove origin
git remote add origin NEW_URL
```

---

## Command 5: `git branch -M main`

### What it does
Renames the current branch to "main".

### Plain English
"Call this branch 'main' instead of 'master'"

### Breaking it down
- `git branch` = Manage branches
- `-M` = Move/rename (force)
- `main` = New name

### What happens
```
Before:
Branch: master ──► Your commits

After:
Branch: main ──► Your commits
```

### Why?
GitHub now uses "main" as the default branch name (used to be "master").

### Visual Analogy
Like renaming a file - same content, different name.

### Example
```bash
git branch -M main

# No output = success
# Your branch is now called "main"
```

### Check current branch
```bash
git branch

# Output:
# * main    ← The * shows current branch
```

---

## Command 6: `git push -u origin main`

### What it does
Uploads your commits to GitHub.

### Plain English
"Send my code to GitHub and remember this connection"

### Breaking it down
- `git push` = Upload commits
- `-u` = Set upstream (remember this connection)
- `origin` = Remote name (GitHub)
- `main` = Branch name

### What happens
```
Your Computer                     GitHub
┌──────────────┐                 ┌──────────────┐
│  Local Repo  │                 │  Remote Repo │
│              │                 │              │
│  Commit #1   │                 │  (empty)     │
│  Commit #2   │                 │              │
│  Commit #3   │                 │              │
└──────────────┘                 └──────────────┘

      ↓ git push -u origin main

┌──────────────┐                 ┌──────────────┐
│  Local Repo  │                 │  Remote Repo │
│              │                 │              │
│  Commit #1   │────────────────►│  Commit #1   │
│  Commit #2   │                 │  Commit #2   │
│  Commit #3   │                 │  Commit #3   │
└──────────────┘                 └──────────────┘
```

### Visual Analogy
Like uploading files to Dropbox - now they're backed up in the cloud.

### The `-u` flag
Sets up tracking so next time you can just type `git push` (no need for `origin main`).

### Example
```bash
git push -u origin main

# Output:
# Enumerating objects: 42, done.
# Counting objects: 100% (42/42), done.
# Writing objects: 100% (42/42), 3.5 MiB | 1.2 MiB/s, done.
# To https://github.com/yourusername/vocabulary-app.git
#  * [new branch]      main -> main
# Branch 'main' set up to track remote branch 'main' from 'origin'.
```

### First time push
You'll be asked for GitHub credentials:
```
Username: yourusername
Password: your_personal_access_token
```

**Note**: GitHub no longer accepts passwords - you need a Personal Access Token:
1. Go to GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token
3. Copy and use as password

### After first push
```bash
# Make changes
git add .
git commit -m "Update feature"
git push    # ← No need for -u origin main anymore!
```

---

## Complete Workflow Example

Let's walk through a complete example:

### Scenario
You want to upload your vocabulary app to GitHub.

### Step-by-Step

```bash
# 1. Navigate to your project
cd /Users/vggnanas/Documents/kiro-projects/words

# 2. Initialize Git (creates .git folder)
git init
# → "Start tracking changes in this folder"

# 3. Stage all files (prepare for commit)
git add .
# → "Mark all files to be saved"

# 4. Commit (save snapshot)
git commit -m "Initial commit - Vocabulary app ready for deployment"
# → "Save these files with this description"

# 5. Connect to GitHub (link to remote)
git remote add origin https://github.com/yourusername/vocabulary-app.git
# → "Connect my local code to this GitHub repo"

# 6. Rename branch to main
git branch -M main
# → "Call this branch 'main'"

# 7. Push to GitHub (upload)
git push -u origin main
# → "Send my code to GitHub and remember this connection"
```

### What you see on GitHub

After pushing, go to `https://github.com/yourusername/vocabulary-app`:

```
vocabulary-app
├── backend/
├── frontend/
├── README.md
├── amplify.yml
└── ... (all your files)

Latest commit: "Initial commit - Vocabulary app ready for deployment"
```

---

## Making Updates

After initial setup, the workflow is simpler:

```bash
# 1. Make changes to your code
# ... edit files ...

# 2. Stage changes
git add .

# 3. Commit changes
git commit -m "Add search feature"

# 4. Push to GitHub
git push
# ← Much simpler! No need for -u origin main
```

---

## Common Git Commands

### Check status
```bash
git status
# Shows:
# - Which files changed
# - Which files are staged
# - Which branch you're on
```

### View history
```bash
git log
# Shows all commits with:
# - Commit ID
# - Author
# - Date
# - Message
```

### View changes
```bash
git diff
# Shows exactly what changed in files
```

### Undo changes
```bash
# Undo changes to a file (before staging)
git checkout -- filename

# Unstage a file (after git add)
git reset filename

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1
```

---

## Visual Summary

```
┌─────────────────────────────────────────────────────────┐
│                    Git Workflow                          │
└─────────────────────────────────────────────────────────┘

1. git init
   └─► Creates .git folder (start tracking)

2. git add .
   └─► Stages files (prepare to save)

3. git commit -m "message"
   └─► Saves snapshot (create version)

4. git remote add origin URL
   └─► Links to GitHub (connect)

5. git branch -M main
   └─► Renames branch (standardize)

6. git push -u origin main
   └─► Uploads to GitHub (backup)

┌─────────────────────────────────────────────────────────┐
│              After Initial Setup                         │
└─────────────────────────────────────────────────────────┘

1. Make changes
2. git add .
3. git commit -m "message"
4. git push
```

---

## Analogy: Git as a Photo Album

Think of Git like a photo album:

| Git Command | Photo Album Equivalent |
|-------------|------------------------|
| `git init` | Buy a new photo album |
| `git add .` | Select photos to add |
| `git commit` | Glue photos into album with date/caption |
| `git remote add` | Connect album to cloud storage |
| `git push` | Upload album to cloud |
| `git log` | Flip through album pages |
| `git diff` | Compare two photos |

---

## Troubleshooting

### "fatal: not a git repository"
**Problem**: You're not in a Git-initialized folder

**Fix**:
```bash
git init
```

### "fatal: remote origin already exists"
**Problem**: You already added a remote

**Fix**:
```bash
git remote remove origin
git remote add origin NEW_URL
```

### "Permission denied (publickey)"
**Problem**: GitHub authentication failed

**Fix**:
1. Use HTTPS URL (not SSH)
2. Use Personal Access Token (not password)
3. Or set up SSH keys

### "Your branch is ahead of 'origin/main'"
**Problem**: You have local commits not pushed

**Fix**:
```bash
git push
```

### "Your branch is behind 'origin/main'"
**Problem**: GitHub has commits you don't have locally

**Fix**:
```bash
git pull
```

---

## Quick Reference Card

```bash
# Setup (once)
git init                                    # Start tracking
git remote add origin URL                   # Connect to GitHub
git branch -M main                          # Rename branch

# Daily workflow
git status                                  # Check what changed
git add .                                   # Stage all changes
git commit -m "message"                     # Save snapshot
git push                                    # Upload to GitHub

# Viewing
git log                                     # View history
git diff                                    # View changes

# Undoing
git checkout -- file                        # Discard changes
git reset HEAD file                         # Unstage file
```

---

## Summary

**Git** = Version control (tracks changes)
**GitHub** = Cloud storage for Git repositories

**Basic workflow**:
1. `git init` - Start tracking
2. `git add .` - Stage changes
3. `git commit -m "msg"` - Save snapshot
4. `git push` - Upload to GitHub

**That's it!** These 4 commands cover 90% of daily Git usage.

---

## Next Steps

1. ✅ Understand Git commands
2. 🔄 Push your vocabulary app to GitHub
3. 🔄 Deploy with AWS Amplify
4. 🔄 Make changes and push updates

Ready to push your code to GitHub? Just follow the commands in order!
