# Learning Guide: GitHub Pages & Dashboard Automation

A complete beginner-friendly guide explaining how this CVE dashboard works.

---

## 📚 Table of Contents

1. [What is GitHub Pages?](#what-is-github-pages)
2. [Why Use GitHub Pages for This Dashboard?](#why-use-github-pages)
3. [How Does It All Work Together?](#how-does-it-all-work-together)
4. [Understanding Each Component](#understanding-each-component)
5. [The Automation Flow](#the-automation-flow)
6. [Why We Need GitHub Secrets](#why-we-need-github-secrets)
7. [Step-by-Step: What Happens When You Deploy](#step-by-step-deployment)
8. [Security Explained](#security-explained)
9. [Alternatives & Why We Chose This](#alternatives)
10. [Common Questions](#common-questions)

---

## What is GitHub Pages?

**GitHub Pages** is a free hosting service provided by GitHub that turns your repository files into a live website.

### Simple Analogy:
Think of it like a **digital bulletin board**:
- You pin a poster (HTML file) to the board
- Anyone with the URL can see it
- You can update the poster anytime
- It's always available 24/7
- Completely free!

### Key Features:
- ✅ **Free hosting** - No server costs
- ✅ **Automatic HTTPS** - Secure by default
- ✅ **Custom domains** - Can use your own domain
- ✅ **Fast CDN** - GitHub's servers worldwide
- ✅ **Version control** - Every change is tracked via git

### What GitHub Pages Can Host:
- ✅ Static HTML files (what we're using)
- ✅ CSS, JavaScript
- ✅ Single Page Applications (React, Vue, etc.)
- ❌ Server-side code (PHP, Python backend, databases)

**Our Use Case:** We generate a static HTML file with all ticket data, and GitHub Pages serves it as a website.

---

## Why Use GitHub Pages for This Dashboard?

### Problem We're Solving:
Your manager/team needs to see CVE tracker tickets but:
- ❌ Not everyone has Jira access
- ❌ Jira's interface is cluttered
- ❌ Can't filter/search easily
- ❌ Hard to share a clean view
- ❌ No mobile-friendly summary

### Why GitHub Pages is Perfect:

#### 1. **No Server Setup Required**
```
Traditional Approach:
You → Write Code → Buy Server → Configure Server → Deploy → Maintain Server
Cost: $5-20/month + time

GitHub Pages:
You → Push HTML to GitHub → Done!
Cost: $0
```

#### 2. **Always Available**
- GitHub's infrastructure (99.9% uptime)
- No server crashes to worry about
- Automatically scaled

#### 3. **Shareable Link**
Instead of saying "login to Jira, go to filters, find XYZ"...
Just send: `https://udayyendva.github.io/cnv-assigned-jiras-dashboard/`

#### 4. **Mobile Friendly**
- Works on phones, tablets
- No app installation needed
- Just open the URL

#### 5. **Version Control**
Every update is tracked:
```bash
git log
# Shows history of all dashboard updates
# Can rollback to previous versions anytime
```

---

## How Does It All Work Together?

Let's break down the entire system:

```
┌─────────────────────────────────────────────────────────────┐
│                     THE BIG PICTURE                         │
└─────────────────────────────────────────────────────────────┘

Step 1: DATA SOURCE (Jira)
   ↓
   Your team's CVE tracker tickets live here
   Example: CNV-82920, CNV-82919, etc.
   
Step 2: FETCH DATA (Python Script)
   ↓
   generate_dashboard.py runs
   → Connects to Jira API
   → Fetches all tickets matching filter
   → Extracts: CVE ID, assignee, status, etc.
   
Step 3: GENERATE HTML (Python Script)
   ↓
   Takes ticket data and creates index.html
   → Builds HTML table
   → Adds search/filter JavaScript
   → Includes styling (CSS)
   → Result: Single 196KB HTML file
   
Step 4: PUSH TO GITHUB (Git)
   ↓
   index.html is committed to repository
   → Stored in GitHub's servers
   → Version controlled
   
Step 5: SERVE TO USERS (GitHub Pages)
   ↓
   GitHub Pages reads index.html from main branch
   → Publishes at: udayyendva.github.io/repo-name
   → Anyone can access (no login needed)
   → Works on any device with a browser
   
Step 6: AUTO-UPDATE (GitHub Actions)
   ↓
   Every day at 9 AM UTC:
   → GitHub Actions triggers
   → Runs generate_dashboard.py
   → Fetches latest Jira data
   → Updates index.html
   → Pushes changes
   → GitHub Pages automatically serves new version
```

---

## Understanding Each Component

### 1. **generate_dashboard.py** (The Brain)

**What it does:**
Fetches Jira data and creates HTML

**How it works:**
```python
# 1. Load credentials from .env
JIRA_USER_EMAIL = "uyendava@redhat.com"
JIRA_API_TOKEN = "ATATT3xFf..."

# 2. Build authentication
headers = {'Authorization': 'Basic <base64_encoded_credentials>'}

# 3. Call Jira API
GET https://redhat.atlassian.net/rest/api/3/search/jql
    ?jql=project IN (10270) AND assignee IN (...) AND status != Closed

# 4. Process response (JSON)
{
  "total": 350,
  "issues": [
    {
      "key": "CNV-82920",
      "fields": {
        "summary": "CVE-2026-12345 virt-operator...",
        "status": "Verified",
        "assignee": "Uday Yendava",
        ...
      }
    },
    ...
  ]
}

# 5. Extract relevant data
- CVE ID from summary (regex: CVE-\d{4}-\d+)
- PS Component from summary
- Version from summary ([cnv-4.21])
- Assignee, status, due date, priority

# 6. Generate HTML
- Create table with all tickets
- Add CSS for styling
- Add JavaScript for filtering
- Write to index.html
```

**Why Python?**
- Easy to work with JSON (Jira API responses)
- Good string processing (extracting CVE IDs, versions)
- Popular for automation
- Works on any OS

---

### 2. **index.html** (The Dashboard)

**What it is:**
A single, self-contained HTML file with everything embedded:
- HTML structure (table)
- CSS styling (colors, layout)
- JavaScript logic (search, filters)
- Data (all 350 tickets)

**Why one file?**
- Easy to deploy
- Fast loading (no external dependencies)
- Works offline (once loaded)
- Simple to understand

**Structure:**
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    /* CSS for colors, fonts, layout */
  </style>
</head>
<body>
  <div class="container">
    <!-- Summary stats -->
    <div class="stats">
      Total: 350 | Overdue: 12 | Uday: 87 tickets
    </div>
    
    <!-- Search and filters -->
    <input type="text" id="search" placeholder="Search...">
    <select id="assigneeFilter">...</select>
    
    <!-- Table with all tickets -->
    <table>
      <tr>
        <td>Uday Yendava</td>
        <td>CVE-2026-12345</td>
        <td><a href="...">CNV-82920</a></td>
        ...
      </tr>
      <!-- 349 more rows... -->
    </table>
  </div>
  
  <script>
    // JavaScript for filtering
    function filterTable() { ... }
  </script>
</body>
</html>
```

---

### 3. **.github/workflows/update-dashboard.yml** (The Automation)

**What it is:**
GitHub Actions workflow - a set of instructions for GitHub to run automatically

**When it runs:**
```yaml
on:
  schedule:
    - cron: '0 9 * * *'  # Every day at 9 AM UTC
  workflow_dispatch:      # Manual trigger button
```

**What it does:**
```yaml
jobs:
  update-dashboard:
    runs-on: ubuntu-latest  # GitHub provides a Linux computer
    
    steps:
      # 1. Get the code
      - uses: actions/checkout@v4
      
      # 2. Install Python
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      # 3. Install dependencies
      - run: pip install requests python-dotenv
      
      # 4. Generate dashboard (using secrets)
      - run: |
          echo "JIRA_USER_EMAIL=${{ secrets.JIRA_USER_EMAIL }}" > .env
          echo "JIRA_API_TOKEN=${{ secrets.JIRA_API_TOKEN }}" >> .env
          python3 generate_dashboard.py
      
      # 5. Commit and push changes
      - run: |
          git add index.html
          git commit -m "Update dashboard"
          git push
```

**Think of it like a robot assistant:**
- Wakes up every day at 9 AM
- Downloads your code
- Runs the Python script
- Saves the new HTML
- Goes back to sleep

---

### 4. **GitHub Secrets** (The Vault)

**What they are:**
Encrypted key-value pairs stored in GitHub

**Why we need them:**
The Python script needs to authenticate with Jira:
```python
# Without secrets (INSECURE - anyone can see)
JIRA_API_TOKEN = "ATATT3xFfGF0..."  # Hardcoded in script

# With secrets (SECURE)
JIRA_API_TOKEN = os.getenv('JIRA_API_TOKEN')  # Read from secure vault
```

**How they work:**
```
You add secret:
Name: JIRA_API_TOKEN
Value: ATATT3xFfGF0...

GitHub encrypts it:
Stored as: 🔒 [encrypted blob]

GitHub Actions uses it:
${{ secrets.JIRA_API_TOKEN }} → Decrypts → "ATATT3xFfGF0..."

Logs show:
JIRA_API_TOKEN=***  # Masked, never exposed
```

**Security levels:**
```
❌ Commit to git: Anyone can see
❌ Environment variable: Visible in process list
✅ GitHub Secrets: Encrypted, masked in logs, access-controlled
```

---

## The Automation Flow

### Daily Update Cycle:

```
09:00 UTC - GitHub's cron scheduler triggers
   ↓
09:00:01 - GitHub Actions starts a virtual machine (Ubuntu Linux)
   ↓
09:00:05 - Checks out your code from main branch
   ↓
09:00:10 - Installs Python 3.11
   ↓
09:00:15 - Installs requests and python-dotenv
   ↓
09:00:20 - Creates .env file with secrets
   ↓
09:00:25 - Runs: python3 generate_dashboard.py
   ↓
09:00:26 - Script connects to Jira API
   ↓
09:00:30 - Fetches 350 tickets (paginated)
   ↓
09:00:35 - Processes ticket data
   ↓
09:00:40 - Generates new index.html (196KB)
   ↓
09:00:45 - Commits index.html to git
   ↓
09:00:50 - Pushes to GitHub
   ↓
09:00:55 - GitHub Pages detects change
   ↓
09:01:00 - Rebuilds and deploys site
   ↓
09:02:00 - New dashboard is live!
   ↓
         Users see fresh data when they refresh
```

**Cost:** $0 (GitHub provides 2000 free Action minutes/month)

---

## Why We Need GitHub Secrets

### The Problem:

**Option A: Hardcode credentials (BAD)**
```python
# In generate_dashboard.py
JIRA_API_TOKEN = "ATATT3xFfGF0..."

# Problem:
# - Anyone who views the repo sees your token
# - Token can access your Jira account
# - Security breach!
```

**Option B: Use environment variables locally (BETTER, but not for automation)**
```bash
export JIRA_API_TOKEN="ATATT3xFf..."
python3 generate_dashboard.py

# Problem:
# - Works on your computer
# - GitHub Actions can't access your local variables
# - Can't automate
```

**Option C: GitHub Secrets (BEST)**
```yaml
# In workflow
env:
  JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}

# Benefits:
# ✅ Encrypted at rest
# ✅ Masked in logs
# ✅ Works in automation
# ✅ Can be rotated easily
# ✅ Access-controlled
```

### How Secrets Stay Secure:

1. **Encryption:**
   - Stored encrypted using AES-256
   - Only decrypted when workflow runs
   - Decryption happens in memory (not written to disk)

2. **Access Control:**
   - Only repository owners can add/edit secrets
   - Only workflows in YOUR repo can use them
   - Not accessible to forked repos (security against attacks)

3. **Audit Trail:**
   - Every secret usage is logged
   - Can see when workflows accessed secrets
   - Settings → Security → Audit log

4. **Masking:**
   ```
   Workflow log shows:
   JIRA_API_TOKEN=***
   
   Never shows:
   JIRA_API_TOKEN=ATATT3xFfGF0...
   ```

---

## Step-by-Step: What Happens When You Deploy

### Initial Setup (One-Time):

#### 1. **Add Secrets**
```
You → GitHub Settings → Secrets → Add
↓
GitHub → Encrypts with AES-256
↓
Stored in encrypted database
```

#### 2. **Enable GitHub Pages**
```
You → Settings → Pages → Enable
↓
GitHub → Creates deployment pipeline
↓
Watches main branch for index.html
```

#### 3. **Run Workflow**
```
You → Actions → Run workflow → Click
↓
GitHub → Starts Ubuntu VM
↓
VM → Runs workflow steps
↓
Workflow → Generates index.html
↓
Commits → Pushes to main
↓
GitHub Pages → Detects change → Deploys
↓
2-3 minutes later → Live at udayyendva.github.io/...
```

### How Users Access the Dashboard:

```
User types URL in browser:
https://udayyendva.github.io/cnv-assigned-jiras-dashboard/

↓ DNS Lookup
Browser finds GitHub's servers

↓ HTTPS Request
GET /cnv-assigned-jiras-dashboard/index.html

↓ GitHub Pages
Serves index.html from main branch

↓ Browser
Downloads 196KB HTML file

↓ Browser Renders
- Parses HTML
- Applies CSS styles
- Runs JavaScript (filters, search)

↓ User Sees
Beautiful dashboard with 350 tickets!

↓ User Interacts
- Types in search box → JavaScript filters table
- Clicks assignee dropdown → Shows only that person's tickets
- Clicks Jira link → Opens in new tab
```

**No database needed!** Everything is in the HTML file.

---

## Security Explained

### What's Public vs Private:

| Item | Visibility | Why |
|------|-----------|-----|
| **Repository code** | 🌍 Public | Anyone can see generate_dashboard.py |
| **Workflow YAML** | 🌍 Public | Anyone can see the automation steps |
| **index.html** | 🌍 Public | This is the dashboard - meant to be shared! |
| **README.md** | 🌍 Public | Documentation |
| **JIRA_API_TOKEN** | 🔒 Private | Encrypted secret, never visible |
| **JIRA_USER_EMAIL** | 🔒 Private | Encrypted secret, never visible |
| **Workflow logs** | 🌍 Public (but secrets masked) | Shows `***` instead of actual values |

### What's in the Dashboard (index.html):

✅ **Included (safe to share):**
- Ticket IDs (CNV-82920, CNV-82919, ...)
- CVE IDs (CVE-2026-12345, ...)
- Assignee names (Uday Yendava, ...)
- Status (ON_QA, Verified, ...)
- Due dates
- Priority levels
- PS component names
- Ticket summaries/titles

❌ **NOT included:**
- Your API token
- Your email address
- Jira comments
- Internal notes
- Attachments
- Any credentials

### Trust Model:

```
Your Local Machine:
~/.claude/.env contains raw token
↓ (secure)
GitHub Secrets:
Encrypted storage
↓ (secure)
GitHub Actions VM:
Temporary, runs in isolated container
Decrypts secret → Uses → Deletes
↓ (secure)
Generated HTML:
No credentials, just ticket data
↓ (public)
GitHub Pages:
Serves HTML to anyone
```

---

## Alternatives & Why We Chose This

### Alternative 1: Manual Updates

**How:**
```bash
# Every time you want to update:
python3 generate_dashboard.py
git add index.html
git commit -m "Update"
git push
```

**Pros:**
- ✅ No secrets in GitHub
- ✅ Full control

**Cons:**
- ❌ Have to remember to update
- ❌ Dashboard goes stale
- ❌ Manual work daily

**Verdict:** Works, but tedious

---

### Alternative 2: Hosted Server (e.g., AWS, Heroku)

**How:**
- Rent a server ($5-20/month)
- Install Python
- Run dashboard script
- Serve via web server (nginx)

**Pros:**
- ✅ Can run server-side code
- ✅ More flexibility

**Cons:**
- ❌ Costs money
- ❌ Server maintenance
- ❌ More complex setup
- ❌ Can crash/need monitoring

**Verdict:** Overkill for static dashboard

---

### Alternative 3: Jira Dashboards (Built-in)

**How:**
- Use Jira's dashboard feature

**Pros:**
- ✅ Already in Jira

**Cons:**
- ❌ Requires Jira login
- ❌ Complex interface
- ❌ Not shareable outside org
- ❌ Limited customization
- ❌ Not mobile-friendly

**Verdict:** Not suitable for external sharing

---

### Alternative 4: Google Sheets + Apps Script

**How:**
- Jira → Apps Script → Google Sheets
- Share sheet publicly

**Pros:**
- ✅ Familiar interface
- ✅ Easy sharing

**Cons:**
- ❌ Slow with 350+ rows
- ❌ Limited styling
- ❌ Apps Script quota limits
- ❌ No search/filter UI

**Verdict:** Works for small datasets

---

### Why GitHub Pages Won:

| Criteria | GitHub Pages | Hosted Server | Jira Dashboard | Google Sheets |
|----------|--------------|---------------|----------------|---------------|
| **Cost** | Free | $5-20/mo | Included | Free |
| **Setup Time** | 10 min | 2-3 hours | 30 min | 1 hour |
| **Maintenance** | None | Weekly | None | Minimal |
| **Customization** | Full | Full | Limited | Medium |
| **Sharing** | Public URL | Public URL | Login required | Public URL |
| **Mobile** | ✅ | ✅ | ❌ | Meh |
| **Search/Filter** | ✅ | ✅ | ✅ | ❌ |
| **Auto-update** | ✅ | ✅ | N/A | ✅ |
| **Speed** | Fast | Fast | Slow | Slow (350 rows) |

**Winner:** GitHub Pages ✅

---

## Common Questions

### Q1: "Why not just use Jira filters?"

**A:** Jira filters require login and are not shareable with people outside your org (like managers without Jira access). GitHub Pages creates a public, accessible view.

---

### Q2: "Is it safe to make my dashboard public?"

**A:** If the ticket information (CVE IDs, assignees, statuses) is okay to share with your team/manager, then yes. We're NOT exposing:
- Your login credentials
- Private Jira comments
- Attachments
- Internal notes

Only the ticket metadata you want to share.

---

### Q3: "What if my API token expires?"

**A:** Simply generate a new one and update the GitHub Secret:
1. Go to https://id.atlassian.com/manage-profile/security/api-tokens
2. Create new token
3. Update `JIRA_API_TOKEN` secret in GitHub
4. Done!

---

### Q4: "Can I make the dashboard private?"

**A:** Yes! Two options:

**Option A: Private repo (requires GitHub Pro)**
- Make repo private
- Dashboard still works via GitHub Pages
- Only invited collaborators can see code

**Option B: Password-protect HTML**
- Add JavaScript password prompt
- Simple but not very secure

---

### Q5: "How much does this cost?"

**A:** $0

- GitHub Pages: Free
- GitHub Actions: 2000 minutes/month free (we use ~5 minutes/month)
- Storage: Unlimited for public repos

---

### Q6: "What if I have 10,000 tickets?"

**A:** The HTML file would be larger (~5-10MB), but still works fine. Browsers can handle it. For very large datasets (100k+ tickets), consider:
- Pagination
- Server-side filtering
- Database backend

But for 350-5000 tickets, static HTML is perfect.

---

### Q7: "Can I customize the look?"

**A:** Yes! Edit the `<style>` section in `generate_dashboard.py`:
```python
# Change colors
.stat-card { background: blue; }  # Change to your brand color

# Change fonts
body { font-family: 'Comic Sans'; }  # (please don't)

# Add your logo
<img src="your-logo.png">
```

---

### Q8: "Why 9 AM UTC for auto-updates?"

**A:** Arbitrary choice. Change it:
```yaml
cron: '0 14 * * *'  # 2 PM UTC = 7:30 PM IST
cron: '0 */6 * * *'  # Every 6 hours
```

---

### Q9: "What if GitHub goes down?"

**A:** Highly unlikely (99.9% uptime SLA), but if it happens:
- Your local copy still works (`file:///path/to/index.html`)
- Can host on any other static host (Netlify, Vercel, etc.)
- Data is backed up in git history

---

### Q10: "Can I add more features?"

**A:** Absolutely! Ideas:
- Charts (using Chart.js)
- Export to CSV button
- Dark mode toggle
- Email notifications for overdue tickets
- Integration with Slack

Just edit `generate_dashboard.py` and add HTML/JavaScript.

---

## Summary: The Whole Picture

```
┌─────────────────────────────────────────────────────────┐
│                    YOU CREATED                          │
│                                                         │
│  A self-updating, shareable CVE dashboard              │
│  that costs $0 and requires zero maintenance           │
│                                                         │
│  Components:                                            │
│  ✅ Python script (generates HTML from Jira)           │
│  ✅ GitHub repository (stores code + HTML)             │
│  ✅ GitHub Actions (automates daily updates)           │
│  ✅ GitHub Pages (hosts HTML publicly)                 │
│  ✅ GitHub Secrets (secures credentials)               │
│                                                         │
│  Result:                                                │
│  📊 Live dashboard at udayyendva.github.io/...         │
│  🔄 Updates automatically every day                    │
│  🔒 Secure (no credentials exposed)                    │
│  📱 Works on any device                                │
│  🆓 Completely free                                    │
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Next Steps

1. ✅ Read this guide
2. ✅ Follow `GITHUB_PAGES_SETUP.md` to deploy
3. ✅ Share dashboard URL with your team
4. ✅ Enjoy automated updates!

**Questions?** Feel free to ask!

---

**Created:** 2026-05-28  
**Author:** Uday Yendava  
**For:** Learning about GitHub Pages and dashboard automation
