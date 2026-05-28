# GitHub Actions - Complete Explanation

A detailed walkthrough of everything we did with GitHub Actions and why.

---

## 📚 Table of Contents

1. [What is GitHub Actions?](#what-is-github-actions)
2. [Why Did We Use It?](#why-did-we-use-it)
3. [Everything We Did - Step by Step](#everything-we-did---step-by-step)
4. [The Workflow File Explained](#the-workflow-file-explained)
5. [GitHub Secrets - Why & How](#github-secrets---why--how)
6. [Permissions - Why We Needed Them](#permissions---why-we-needed-them)
7. [What Happens When It Runs](#what-happens-when-it-runs)
8. [Troubleshooting & Fixes](#troubleshooting--fixes)
9. [How It All Connects Together](#how-it-all-connects-together)

---

## What is GitHub Actions?

### Simple Definition:
**GitHub Actions is a robot that runs code for you automatically on GitHub's computers.**

### Detailed Explanation:

Think of GitHub Actions like having a personal assistant who:
- Wakes up at specific times (like 9 AM every day)
- Follows your exact instructions
- Has access to GitHub's powerful computers
- Works 24/7 without getting tired
- Costs you nothing (free tier)

### Real-World Analogy:

```
WITHOUT GitHub Actions (Manual):
─────────────────────────────────
You wake up at 9 AM
↓
Turn on your computer
↓
Open terminal
↓
Run: python3 generate_dashboard.py
↓
Wait for it to finish
↓
Run: git add, git commit, git push
↓
Every. Single. Day. 😫

WITH GitHub Actions (Automated):
─────────────────────────────────
You sleep peacefully 😴
↓
GitHub's robot wakes up at 9 AM
↓
Runs all commands automatically
↓
Updates dashboard
↓
Pushes changes
↓
You wake up to fresh data! 🎉
```

---

## Why Did We Use It?

### Problem We Solved:

**Manual Update Process:**
```
Every time Jira tickets change, you would need to:
1. Remember to update the dashboard
2. Run the Python script manually
3. Commit the changes
4. Push to GitHub
5. Repeat daily... forever
```

**With GitHub Actions:**
```
✅ Runs automatically at 9 AM UTC daily
✅ Never forget to update
✅ Always fresh data
✅ Zero manual work
✅ Works even when your computer is off
```

### Benefits:

| Feature | Manual Process | GitHub Actions |
|---------|---------------|----------------|
| **Reliability** | Depends on you remembering | Runs every day guaranteed |
| **Time Required** | 5 min daily = 30 hours/year | 0 minutes (automated) |
| **Computer Needed** | Your laptop must be on | GitHub's servers (always on) |
| **Cost** | Free but time-consuming | Free and automatic |
| **Consistency** | May forget or miss days | Never misses a day |
| **Works When You're...** | Sleeping/vacation? ❌ | Sleeping/vacation? ✅ |

---

## Everything We Did - Step by Step

### Step 1: Created the Workflow File

**What:** Created `.github/workflows/update-dashboard.yml`

**Why:** This file tells GitHub Actions WHAT to do and WHEN to do it

**Location:**
```
your-repo/
└── .github/
    └── workflows/
        └── update-dashboard.yml  ← This file!
```

**Command we used:**
```bash
mkdir -p .github/workflows
# Then created the YAML file
```

**Purpose:** GitHub automatically detects files in `.github/workflows/` and runs them as automated tasks

---

### Step 2: Wrote the Workflow Instructions (YAML)

**What:** The YAML file contains all the instructions for the robot

**Structure:**
```yaml
name: Update CVE Dashboard          # Give it a name (shows in GitHub UI)

on:                                 # WHEN to run
  schedule:
    - cron: '0 9 * * *'            # Daily at 9 AM UTC
  workflow_dispatch:                # Manual trigger button

jobs:                               # WHAT to run
  update-dashboard:                 # Job name
    runs-on: ubuntu-latest          # Which computer to use
    
    steps:                          # List of actions to perform
      - Checkout code
      - Install Python
      - Install dependencies
      - Run Python script
      - Push changes
```

**Why YAML?** 
- Industry standard for configuration
- Easy to read (indentation = structure)
- GitHub Actions understands it

---

### Step 3: Set Up the Schedule (Cron)

**What we wrote:**
```yaml
on:
  schedule:
    - cron: '0 9 * * *'
```

**Why:** Tell GitHub "run this every day at 9 AM UTC"

**Cron Syntax Explained:**
```
 ┌───────────── minute (0 - 59)
 │ ┌───────────── hour (0 - 23)
 │ │ ┌───────────── day of month (1 - 31)
 │ │ │ ┌───────────── month (1 - 12)
 │ │ │ │ ┌───────────── day of week (0 - 6, Sunday = 0)
 │ │ │ │ │
 * * * * *

Examples:
'0 9 * * *'     = 9 AM UTC daily
'0 */6 * * *'   = Every 6 hours
'0 9 * * 1-5'   = 9 AM weekdays only
'30 14 * * *'   = 2:30 PM UTC daily
```

**Why 9 AM UTC?**
- UTC = Universal Time (no timezone confusion)
- 9 AM UTC = 2:30 PM IST (India)
- You can change this anytime!

**workflow_dispatch:**
```yaml
workflow_dispatch:  # Adds a "Run workflow" button in GitHub
```
- Lets you trigger manually anytime
- Great for testing
- Shows up in Actions tab

---

### Step 4: Configured the Job Steps

#### Step 4a: Checkout Code
```yaml
- name: Checkout repository
  uses: actions/checkout@v4
```

**What it does:** Downloads your repo code to GitHub's computer

**Why needed:** The robot needs your code (generate_dashboard.py) to run

**Without this:** Error! Script file not found

**Technical detail:** 
- `uses: actions/checkout@v4` = Use GitHub's pre-built action
- `@v4` = Version 4 (latest stable)

---

#### Step 4b: Install Python
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

**What it does:** Installs Python 3.11 on the virtual machine

**Why needed:** Our script is written in Python

**Why version 3.11?** 
- Modern and stable
- Fast performance
- Compatible with all libraries we use

**Without this:** Error! python3: command not found

---

#### Step 4c: Install Dependencies
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install requests
```

**What it does:** Installs the `requests` library

**Why needed:** Our script uses `requests` to call Jira API

**Line by line:**
```bash
python -m pip install --upgrade pip  # Update pip to latest version
pip install requests                  # Install requests library
```

**Why not python-dotenv?** 
- Initially included
- Later removed (we create .env manually in workflow)
- Don't need it since we're writing .env ourselves

---

#### Step 4d: Generate Dashboard (The Main Step!)
```yaml
- name: Generate dashboard
  env:
    JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
    JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
    JIRA_BASE_URL: https://redhat.atlassian.net
    JIRA_DASHBOARD_FILTER_URL: https://redhat.atlassian.net/issues?jql=...
  run: |
    echo "JIRA_USER_EMAIL=$JIRA_USER_EMAIL" > .env
    echo "JIRA_API_TOKEN=$JIRA_API_TOKEN" >> .env
    echo "JIRA_BASE_URL=$JIRA_BASE_URL" >> .env
    echo "JIRA_DASHBOARD_FILTER_URL=$JIRA_DASHBOARD_FILTER_URL" >> .env
    python3 generate_dashboard.py
```

**What it does:** Creates .env file with credentials, then runs the Python script

**Breaking it down:**

**Part 1: env: section**
```yaml
env:
  JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
```
- Sets environment variables for this step
- `${{ secrets.JIRA_USER_EMAIL }}` = Read from encrypted GitHub Secrets
- These variables exist ONLY during this step's execution

**Part 2: Create .env file**
```bash
echo "JIRA_USER_EMAIL=$JIRA_USER_EMAIL" > .env
```
- `>` = Create new file (or overwrite)
- `>>` = Append to file
- Creates same .env format as your local ~/.claude/.env

**Why create .env?**
- Our Python script reads credentials from .env
- Keeps the script unchanged
- Works same way locally and in GitHub Actions

**Part 3: Run the script**
```bash
python3 generate_dashboard.py
```
- Runs our dashboard generator
- Fetches 350 tickets from Jira
- Generates index.html with all data

---

#### Step 4e: Commit and Push Changes
```yaml
- name: Commit and push changes
  run: |
    git config user.name "GitHub Actions Bot"
    git config user.email "actions@github.com"
    git add index.html
    git diff --quiet && git diff --staged --quiet || (git commit -m "🤖 Auto-update dashboard - $(date +'%Y-%m-%d %H:%M')" && git push)
```

**What it does:** Saves the new dashboard to GitHub

**Line by line:**

**Configure git user:**
```bash
git config user.name "GitHub Actions Bot"
git config user.email "actions@github.com"
```
- Every git commit needs author info
- Sets bot as the committer
- Shows up in commit history as "GitHub Actions Bot"

**Stage the file:**
```bash
git add index.html
```
- Prepares index.html for commit
- Only adds the dashboard (not .env with secrets!)

**Smart commit logic:**
```bash
git diff --quiet && git diff --staged --quiet || (git commit ... && git push)
```

Let's break this down:

```bash
# Check if there are changes
git diff --quiet              # No unstaged changes?
&&                            # AND
git diff --staged --quiet     # No staged changes?

# If both are true (no changes):
  # Do nothing (exit successfully)

||  # OR (if there ARE changes):

# Commit and push
(git commit -m "🤖 Auto-update..." && git push)
```

**Why this logic?**
- If data didn't change → No useless commits
- If data changed → Commit and push
- Keeps git history clean

**Commit message:**
```bash
"🤖 Auto-update dashboard - $(date +'%Y-%m-%d %H:%M')"
```
- `$(date ...)` = Current timestamp
- Example: "🤖 Auto-update dashboard - 2026-05-28 09:00"
- Emoji makes it easy to spot automated commits

---

### Step 5: Added GitHub Secrets

**What:** Encrypted storage for sensitive data

**Where:** Settings → Secrets and variables → Actions

**What we added:**
1. `JIRA_USER_EMAIL` = uyendava@redhat.com
2. `JIRA_API_TOKEN` = ATATT3xFfGF0...

**Why needed:** The script needs these to authenticate with Jira API

**How they work:**
```
You type in GitHub UI:
┌─────────────────────────────┐
│ Name: JIRA_API_TOKEN       │
│ Value: ATATT3xFfGF0...     │
│ [Add secret]               │
└─────────────────────────────┘
        ↓
GitHub encrypts with AES-256
        ↓
Stored in encrypted database
        ↓
Workflow accesses via: ${{ secrets.JIRA_API_TOKEN }}
        ↓
Decrypted ONLY when workflow runs
        ↓
Used in script, then discarded
        ↓
Logs show: JIRA_API_TOKEN=***
```

**Security features:**
- ✅ Encrypted at rest (AES-256)
- ✅ Masked in logs (shows as ***)
- ✅ Only accessible to workflows in YOUR repo
- ✅ Can be updated anytime
- ✅ Can be deleted anytime
- ✅ Audit log tracks usage

**Why not hardcode in workflow?**
```yaml
# BAD - Never do this!
env:
  JIRA_API_TOKEN: ATATT3xFfGF0...  # ❌ Visible to everyone!

# GOOD - Use secrets
env:
  JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}  # ✅ Encrypted
```

---

### Step 6: Set Workflow Permissions

**What:** Gave GitHub Actions permission to push changes

**Where:** Settings → Actions → General → Workflow permissions

**What we selected:**
- ✅ Read and write permissions
- ✅ Allow GitHub Actions to create and approve pull requests

**Why needed:**

**Default permissions:** Read-only
- Can checkout code ✅
- Can run scripts ✅
- Can push changes ❌ (ERROR!)

**With write permissions:**
- Can checkout code ✅
- Can run scripts ✅
- Can push changes ✅ (SUCCESS!)

**What happens without this:**
```
Error: refusing to allow a GitHub App to create or update workflow
```

**Technical reason:**
- Git push = Write operation
- Needs write permission to the repository
- GitHub protects repos by default (security)

---

### Step 7: Enabled GitHub Pages

**What:** Turned on static site hosting

**Where:** Settings → Pages → Source

**Configuration:**
- Source: Deploy from a branch
- Branch: main
- Folder: / (root)

**Why needed:** To make index.html accessible as a website

**How it works:**
```
index.html in repo
        ↓
GitHub Pages reads it
        ↓
Hosts at: username.github.io/repo-name
        ↓
Anyone can access it
```

**Without GitHub Pages:**
- index.html exists in repo ✅
- But only accessible by downloading ❌
- Not a live website ❌

**With GitHub Pages:**
- index.html exists in repo ✅
- Accessible as live website ✅
- Updates automatically when file changes ✅

---

## The Workflow File Explained

### Complete Annotated Version:

```yaml
# WORKFLOW NAME
# Appears in GitHub Actions UI
name: Update CVE Dashboard

# TRIGGERS - When to run
on:
  # Scheduled trigger - runs automatically
  schedule:
    - cron: '0 9 * * *'  # Every day at 9 AM UTC
  
  # Manual trigger - "Run workflow" button in UI
  workflow_dispatch:

# JOBS - What to run
jobs:
  # Job name (can have multiple jobs)
  update-dashboard:
    
    # ENVIRONMENT
    # GitHub provides a virtual Ubuntu machine
    runs-on: ubuntu-latest
    
    # STEPS - Sequential actions
    steps:
      # STEP 1: Get the code
      - name: Checkout repository
        uses: actions/checkout@v4
        # Downloads repo to: /home/runner/work/repo-name/repo-name
      
      # STEP 2: Install Python
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
        # Installs Python 3.11
        # Makes 'python3' and 'pip' available
      
      # STEP 3: Install Python packages
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests
        # Updates pip to latest
        # Installs requests library
      
      # STEP 4: Run the main script
      - name: Generate dashboard
        # Environment variables for this step only
        env:
          # Read from encrypted secrets
          JIRA_USER_EMAIL: ${{ secrets.JIRA_USER_EMAIL }}
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          # Hardcoded (not sensitive)
          JIRA_BASE_URL: https://redhat.atlassian.net
          # The team filter URL (could also be a secret)
          JIRA_DASHBOARD_FILTER_URL: https://redhat.atlassian.net/issues?jql=...
        run: |
          # Create .env file
          echo "JIRA_USER_EMAIL=$JIRA_USER_EMAIL" > .env
          echo "JIRA_API_TOKEN=$JIRA_API_TOKEN" >> .env
          echo "JIRA_BASE_URL=$JIRA_BASE_URL" >> .env
          echo "JIRA_DASHBOARD_FILTER_URL=$JIRA_DASHBOARD_FILTER_URL" >> .env
          
          # Run the Python script
          python3 generate_dashboard.py
          # Script reads .env, fetches Jira data, generates index.html
      
      # STEP 5: Save and publish changes
      - name: Commit and push changes
        run: |
          # Configure git identity
          git config user.name "GitHub Actions Bot"
          git config user.email "actions@github.com"
          
          # Stage the updated file
          git add index.html
          
          # Commit and push ONLY if there are changes
          git diff --quiet && git diff --staged --quiet || \
            (git commit -m "🤖 Auto-update dashboard - $(date +'%Y-%m-%d %H:%M')" && git push)
```

---

## GitHub Secrets - Why & How

### Why Secrets Are Necessary

**The Problem:**
```python
# In generate_dashboard.py, we need:
JIRA_API_TOKEN = "ATATT3xFfGF0..."  # How do we provide this?
```

**Option 1: Hardcode (TERRIBLE)**
```python
# In the script
JIRA_API_TOKEN = "ATATT3xFfGF0..."
```
❌ Visible to everyone  
❌ Committed to git history  
❌ Security breach!  

**Option 2: Environment variable (BETTER)**
```python
# In the script
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')
```
✅ Not in code  
❌ But where does the value come from in GitHub Actions?  

**Option 3: GitHub Secrets (BEST)**
```yaml
# In workflow
env:
  JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
```
✅ Encrypted storage  
✅ Masked in logs  
✅ Easy to update  
✅ Industry standard  

### How Secrets Work

**Adding a Secret:**
```
1. You navigate to GitHub repo
2. Settings → Secrets → Actions
3. Click "New repository secret"
4. Enter name: JIRA_API_TOKEN
5. Enter value: ATATT3xFfGF0...
6. Click "Add secret"
```

**Behind the scenes:**
```
GitHub UI receives your input
        ↓
Encrypts using AES-256-GCM
        ↓
Stores in GitHub's secret database
        ↓
Associated with your repository
        ↓
Only your workflows can access it
```

**Using in Workflow:**
```yaml
env:
  MY_SECRET: ${{ secrets.MY_SECRET }}
```

**At runtime:**
```
Workflow starts
        ↓
GitHub reads: ${{ secrets.MY_SECRET }}
        ↓
Decrypts the secret
        ↓
Injects into environment as: MY_SECRET=actual_value
        ↓
Script accesses via: os.getenv('MY_SECRET')
        ↓
Workflow ends
        ↓
Value is discarded (not saved anywhere)
```

**In Logs:**
```
# What you see in workflow logs:
JIRA_API_TOKEN=***

# What actually ran:
JIRA_API_TOKEN=ATATT3xFfGF0b_7tr28T5SM9V9bywnbGNhpNhPdMdMclBoUQEpq6dlMPtEJblyipxiycfi_EBnn8QhFOWrWJ_kf_8qr2OWpoCwy7aJI_QsSufNIO1MzDuKWg8EcQH4ZnCtsmUB7a36CcDCDLoJJIncL3bzKy3QcXRHlpFO4WJHhFp9E9naDtjSM
```

---

## Permissions - Why We Needed Them

### Default Behavior

**GitHub's default (security first):**
- Workflows can READ your repo ✅
- Workflows CANNOT WRITE to your repo ❌

**Why?**
- Prevents malicious code from modifying your repo
- Requires explicit permission grant
- You must consciously enable it

### What Happens Without Write Permission

**Workflow runs:**
```bash
git push
```

**GitHub responds:**
```
Error: refusing to allow a GitHub App to create or update workflow
Permission denied (publickey).
fatal: Could not read from remote repository.
```

**Why?**
- The workflow is trying to WRITE (push) to the repo
- Default permissions = READ-ONLY
- Git push fails

### Enabling Write Permission

**Steps:**
1. Settings → Actions → General
2. Scroll to "Workflow permissions"
3. Select "Read and write permissions"
4. Optional: Check "Allow GitHub Actions to create and approve pull requests"
5. Save

**What this enables:**
```yaml
# Now this works:
- run: |
    git add index.html
    git commit -m "Update"
    git push  # ✅ SUCCESS!
```

**Security consideration:**
- Only enable for trusted workflows
- Review what your workflow does before enabling
- Our workflow only pushes index.html (safe)

---

## What Happens When It Runs

### Complete Flow - Minute by Minute

```
09:00:00 UTC - GitHub's cron scheduler triggers
        ↓
09:00:01 - GitHub allocates a virtual machine (Ubuntu)
        ↓
09:00:05 - VM boots up
        ↓
09:00:10 - Workflow starts: "Update CVE Dashboard"
        ↓
        
STEP 1: Checkout repository (10 seconds)
09:00:10 - Download your repo
09:00:15 - Files available at: /home/runner/work/repo/repo
09:00:20 - ✅ Checkout complete
        ↓
        
STEP 2: Set up Python (15 seconds)
09:00:20 - Download Python 3.11
09:00:25 - Install Python
09:00:30 - Verify: python3 --version → 3.11.x
09:00:35 - ✅ Python ready
        ↓
        
STEP 3: Install dependencies (20 seconds)
09:00:35 - pip install --upgrade pip
09:00:40 - pip install requests
09:00:50 - Verify: pip list | grep requests
09:00:55 - ✅ Dependencies installed
        ↓
        
STEP 4: Generate dashboard (30 seconds)
09:00:55 - Create .env with secrets
09:00:56 - Run: python3 generate_dashboard.py
09:00:57 - Script: Load .env
09:00:58 - Script: Connect to Jira API
09:01:00 - Script: Fetch page 1/4 (100 tickets)
09:01:05 - Script: Fetch page 2/4 (100 tickets)
09:01:10 - Script: Fetch page 3/4 (100 tickets)
09:01:15 - Script: Fetch page 4/4 (50 tickets)
09:01:20 - Script: Process 350 tickets
09:01:22 - Script: Generate HTML
09:01:25 - Script: Write index.html (196KB)
09:01:25 - ✅ Dashboard generated
        ↓
        
STEP 5: Commit and push (10 seconds)
09:01:25 - git config user.name "GitHub Actions Bot"
09:01:26 - git add index.html
09:01:27 - Check for changes: git diff
09:01:28 - Changes detected ✅
09:01:29 - git commit -m "🤖 Auto-update dashboard - 2026-05-28 09:01"
09:01:30 - git push
09:01:32 - Push successful ✅
09:01:35 - ✅ Commit and push complete
        ↓
        
09:01:35 - Workflow complete! ✅
09:01:40 - VM shuts down
09:01:45 - Resources released
        ↓
        
09:02:00 - GitHub Pages detects change
09:02:30 - Rebuilds site
09:03:00 - New dashboard is LIVE! 🎉
```

**Total time:** ~3 minutes from trigger to live site

---

## Troubleshooting & Fixes

### Issue 1: Empty Dashboard (0 Tickets)

**Problem:**
```
Dashboard showed:
Total Tickets: 0
Overdue: 0
Empty table
```

**Cause:**
- Workflow ran successfully
- But secrets were empty/not set
- Script connected to Jira with invalid credentials
- Jira returned 0 tickets

**How we detected:**
```bash
wc -l index.html     # 105 lines (should be 3600+)
grep "<tr>" index.html | wc -l  # 1 row (just header)
```

**Fix:**
1. Added secrets in GitHub (JIRA_USER_EMAIL, JIRA_API_TOKEN)
2. Regenerated locally: `python3 generate_dashboard.py`
3. Verified: 350 tickets fetched ✅
4. Pushed manually: `git push`

**Prevention:**
- Always verify secrets are set before first run
- Test workflow manually after setting secrets

---

### Issue 2: Permission Denied on Push

**Problem:**
```
Error: refusing to allow a GitHub App to create or update workflow
```

**Cause:**
- Workflow tried to: `git push`
- Default permissions: Read-only
- Push operation requires write permission

**Fix:**
1. Settings → Actions → Workflow permissions
2. Selected: "Read and write permissions"
3. Saved
4. Re-ran workflow → Success! ✅

---

### Issue 3: Wrong Filter URL

**Problem:**
- Initially used filter 110799 (doesn't exist)
- Workflow fetched 0 tickets

**Fix:**
```yaml
# Before:
python3 generate_dashboard.py "https://redhat.atlassian.net/issues/?filter=110799"

# After:
JIRA_DASHBOARD_FILTER_URL: https://redhat.atlassian.net/issues?jql=...
python3 generate_dashboard.py
```

**Why this works:**
- Script checks for JIRA_DASHBOARD_FILTER_URL in environment
- Reads filter URL from env variable
- Uses correct team filter

---

### Issue 4: python-dotenv Not Needed

**Problem:**
- Initially installed `python-dotenv`
- Not actually needed

**Why:**
```yaml
# We manually create .env:
echo "JIRA_USER_EMAIL=$JIRA_USER_EMAIL" > .env

# Script reads it manually:
with open('.env') as f:
    # Parse .env
```

**Fix:**
```yaml
# Before:
pip install requests python-dotenv

# After:
pip install requests  # Only requests needed
```

**Result:** Faster workflow (less to install)

---

## How It All Connects Together

### The Complete Picture

```
┌─────────────────────────────────────────────────────────────┐
│                     YOUR SETUP                              │
└─────────────────────────────────────────────────────────────┘

LOCAL MACHINE (Your Computer)
├── ~/.claude/.env               ← Your credentials (local only)
├── ~/cnv-assigned-jiras-dashboard/
│   ├── generate_dashboard.py    ← The Python script
│   ├── index.html               ← Generated dashboard
│   └── .github/workflows/
│       └── update-dashboard.yml ← Automation instructions

        ↓ git push

GITHUB REPOSITORY
├── generate_dashboard.py        ← Committed
├── index.html                   ← Committed
└── .github/workflows/
    └── update-dashboard.yml     ← Tells GitHub Actions what to do

        +

GITHUB SECRETS (Encrypted Storage)
├── JIRA_USER_EMAIL             ← Your email (encrypted)
└── JIRA_API_TOKEN              ← Your token (encrypted)

        +

GITHUB ACTIONS (Automation Engine)
Every day at 9 AM UTC:
1. Starts Ubuntu VM
2. Checks out your code
3. Installs Python
4. Installs requests
5. Creates .env from secrets
6. Runs generate_dashboard.py
7. Commits updated index.html
8. Pushes to GitHub

        ↓

GITHUB PAGES (Web Hosting)
Detects new index.html
Rebuilds site
Serves at: username.github.io/repo-name

        ↓

USERS (Anyone with the URL)
Visit: https://udayyendva.github.io/cnv-assigned-jiras-dashboard/
See: Fresh data (updated daily)
```

### Data Flow

```
JIRA (Source of Truth)
        ↓
API Request (GitHub Actions runs Python script)
        ↓
JSON Response (350 tickets)
        ↓
Python Processing (extract CVE IDs, assignees, etc.)
        ↓
HTML Generation (build table with all tickets)
        ↓
index.html (196KB file)
        ↓
Git Commit (save to repository)
        ↓
GitHub Pages (serve as website)
        ↓
Browser (user sees dashboard)
```

### Automation Flow

```
⏰ 9:00 AM UTC - Cron triggers
        ↓
🤖 GitHub Actions starts
        ↓
📥 Checkout code
        ↓
🐍 Install Python + packages
        ↓
🔐 Load secrets into .env
        ↓
🔄 Run generate_dashboard.py
        ├─→ Connect to Jira
        ├─→ Fetch 350 tickets
        ├─→ Process data
        └─→ Generate HTML
        ↓
💾 Commit index.html
        ↓
📤 Push to GitHub
        ↓
🌐 GitHub Pages deploys
        ↓
✅ Dashboard is live!
```

---

## Key Takeaways

### What You Learned

1. **GitHub Actions** = Automated tasks on GitHub's computers
2. **Workflows** = Instructions in YAML files
3. **Secrets** = Encrypted credential storage
4. **Permissions** = Control what workflows can do
5. **Cron** = Schedule tasks to run automatically
6. **CI/CD** = Continuous Integration / Continuous Deployment

### What We Built

✅ Automated daily dashboard updates  
✅ Secure credential management  
✅ Zero-maintenance system  
✅ Free hosting and automation  
✅ Professional DevOps setup  

### Skills Acquired

- ✅ Writing GitHub Actions workflows
- ✅ Using GitHub Secrets
- ✅ Understanding YAML syntax
- ✅ Configuring permissions
- ✅ Debugging workflow failures
- ✅ Setting up CI/CD pipelines
- ✅ Automating repetitive tasks

---

## Summary

**What we did:**
1. Created `.github/workflows/update-dashboard.yml`
2. Configured it to run daily at 9 AM UTC
3. Added steps: checkout, install, generate, push
4. Stored credentials in GitHub Secrets
5. Enabled write permissions for the workflow
6. Enabled GitHub Pages to serve the dashboard

**Why we did it:**
- Automate daily dashboard updates
- No manual work required
- Always fresh data
- Professional DevOps practice

**Result:**
🎉 A fully automated, self-updating dashboard that costs $0 and requires zero maintenance!

---

**Created:** 2026-05-28  
**For:** Understanding GitHub Actions automation  
**Dashboard:** https://udayyendva.github.io/cnv-assigned-jiras-dashboard/
