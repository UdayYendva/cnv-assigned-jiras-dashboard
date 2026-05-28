# CNV Team CVE Dashboard

Live dashboard tracking 350+ CNV CVE tracker tickets across 4 team members.

## 🔗 View Live Dashboard

**https://udayyendva.github.io/cnv-assigned-jiras-dashboard/**

---

## 📊 Features

✅ **350+ tickets** from 4 team members  
✅ **Real-time filtering** by assignee, status, search  
✅ **Color-coded statuses** (ON_QA, MODIFIED, Verified, etc.)  
✅ **Summary stats** - Total tickets, Overdue count, Per-assignee breakdown  
✅ **Clickable Jira links** - Opens tickets in new tab  
✅ **Auto-updates daily** at 9 AM UTC via GitHub Actions  
✅ **No login required** - Share with anyone  
✅ **Mobile-friendly** - Works on phones/tablets  

---

## 🎯 What It Shows

| Column | Description |
|--------|-------------|
| **Assignee** | Team member name |
| **CVE ID** | CVE identifier (e.g., CVE-2026-12345) |
| **Jira ID** | Clickable link to Jira ticket |
| **PS Component** | Component name (e.g., virt-operator-rhel9) |
| **Version** | CNV version (e.g., 4.21) |
| **Due Date** | Ticket due date |
| **Status** | Current status with color coding |
| **Priority** | Blocker, Critical, Major, Minor |

---

## 🔄 How It Updates

1. **GitHub Actions** runs daily at 9 AM UTC
2. **Fetches latest data** from Jira via API
3. **Regenerates** the HTML dashboard
4. **Auto-commits** and publishes to GitHub Pages

You can also trigger manual updates from the Actions tab.

---

## 🛠️ Local Usage

### Generate Dashboard Locally

```bash
# Install dependencies
pip install requests

# Set credentials in ~/.claude/.env (already configured)
# JIRA_USER_EMAIL=your.email@redhat.com
# JIRA_API_TOKEN=your_token
# JIRA_DASHBOARD_FILTER_URL=<your_filter_url>

# Generate
python3 generate_dashboard.py

# View
firefox index.html
```

---

## 🔧 Customization

### Change Jira Filter

Edit `.github/workflows/update-dashboard.yml` and update the filter URL, or set `JIRA_DASHBOARD_FILTER_URL` secret in GitHub.

### Update Frequency

Edit `.github/workflows/update-dashboard.yml` line 4:

```yaml
- cron: '0 9 * * *'  # Daily at 9 AM UTC
```

Examples:
- Every 6 hours: `'0 */6 * * *'`
- Weekdays only: `'0 9 * * 1-5'`
- Twice daily: `'0 9,17 * * *'`

---

## 📝 Setup

### GitHub Secrets Required

Add these in: Settings → Secrets and variables → Actions

1. **JIRA_USER_EMAIL** - Your Jira email
2. **JIRA_API_TOKEN** - Your Jira API token ([Get one here](https://id.atlassian.com/manage-profile/security/api-tokens))

### GitHub Pages

1. Settings → Pages
2. Source: **Deploy from a branch**
3. Branch: **main**
4. Folder: **/ (root)**
5. Save

---

## 🚀 Manual Update

Go to: [Actions → Update CVE Dashboard → Run workflow](https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions)

---

## 📱 Share With Your Team

Just send them the link:
**https://udayyendva.github.io/cnv-assigned-jiras-dashboard/**

No Jira login needed - perfect for managers, stakeholders, or team overview!

---

## 🔒 Data Privacy

- Dashboard is **publicly accessible** (no authentication required)
- Contains: Ticket IDs, CVE IDs, assignee names, summaries, status
- Does **NOT** contain: Comments, attachments, internal notes
- Refresh your Jira API token regularly for security

---

## 💡 Tips

- **Bookmark** the dashboard for quick daily reference
- **Filter** by your name to see just your tickets
- **Search** for specific CVEs or components
- **Mobile** - Works great on phones for on-the-go checks

---

## 📞 Support

- **Issues with data?** Check the Actions tab for errors
- **Need different filters?** Update `JIRA_DASHBOARD_FILTER_URL`
- **Dashboard not updating?** Verify GitHub secrets are set

---

**Auto-generated via GitHub Actions** | Powered by Jira REST API
