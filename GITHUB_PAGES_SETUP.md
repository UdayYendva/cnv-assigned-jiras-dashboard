# Enable GitHub Pages - Final Steps

Your dashboard code is now on GitHub! ✅

## Step 1: Add GitHub Secrets

1. Go to: **https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/settings/secrets/actions**
2. Click **"New repository secret"**
3. Add these TWO secrets:

### Secret 1:
- Name: `JIRA_USER_EMAIL`
- Value: `uyendava@redhat.com`

### Secret 2:
- Name: `JIRA_API_TOKEN`  
- Value: (Copy from your `~/.claude/.env` file - the ATATT3xFfGF0... token)

```bash
# To see your token:
grep JIRA_API_TOKEN ~/.claude/.env
```

## Step 2: Enable GitHub Pages

1. Go to: **https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/settings/pages**
2. Under **"Source"**:
   - Select: **Deploy from a branch**
   - Branch: **main**
   - Folder: **/ (root)**
3. Click **"Save"**

## Step 3: Run the Workflow

1. Go to: **https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions**
2. Click on **"Update CVE Dashboard"** workflow (left sidebar)
3. Click **"Run workflow"** button (top right)
4. Click **"Run workflow"** in the dropdown
5. Wait ~30 seconds for it to complete

## Step 4: View Your Live Dashboard!

After ~2-3 minutes, your dashboard will be live at:

**https://udayyendva.github.io/cnv-assigned-jiras-dashboard/**

---

## 🎉 What You Get

✅ **350 tickets** from your team  
✅ **Auto-updates daily** at 9 AM UTC  
✅ **Searchable & filterable** by assignee, status  
✅ **Shareable** - No Jira login needed  
✅ **Mobile-friendly**  

---

## 📱 Share With Your Team

Just send them:
**https://udayyendva.github.io/cnv-assigned-jiras-dashboard/**

---

## 🔄 Manual Updates

Anytime you want to refresh the dashboard:

1. Go to: https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions
2. Click "Update CVE Dashboard"
3. Click "Run workflow"

Or run locally:
```bash
cd ~/cnv-assigned-jiras-dashboard
python3 generate_dashboard.py
git add index.html
git commit -m "Update dashboard"
git push
```

---

## ❓ Troubleshooting

**GitHub Actions failing?**
- Check that both secrets (JIRA_USER_EMAIL and JIRA_API_TOKEN) are set correctly
- Make sure your Jira API token is still valid

**Dashboard showing old data?**
- Run the workflow manually
- Check the Actions tab for errors

**Pages not deploying?**
- Wait 2-3 minutes after enabling Pages
- Check Settings → Pages shows "Your site is live at..."
- Hard refresh your browser (Ctrl+Shift+R)

---

## 🎯 Next Steps

1. ✅ Set the secrets (Step 1)
2. ✅ Enable Pages (Step 2)
3. ✅ Run workflow (Step 3)
4. ✅ Share the URL with your manager!

---

**Generated:** 2026-05-28  
**Tickets:** 350  
**Team Members:** 4  
**Auto-updates:** Daily at 9 AM UTC
