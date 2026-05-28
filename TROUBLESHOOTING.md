# Troubleshooting GitHub Actions Workflow

## Common Issues and Solutions

### ✅ FIXED: Wrong Filter URL

**Problem:** Workflow was using filter 110799 which doesn't exist

**Solution:** ✅ Updated to use your team filter URL directly in the workflow

---

### Issue: Secrets Not Set

**Error message:**
```
No tickets found
```

**Cause:** JIRA_USER_EMAIL or JIRA_API_TOKEN secrets not configured

**Solution:**
1. Go to: https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/settings/secrets/actions
2. Add both secrets:
   - `JIRA_USER_EMAIL` = `uyendava@redhat.com`
   - `JIRA_API_TOKEN` = Your token from `~/.claude/.env`

---

### Issue: Permission Denied on Push

**Error message:**
```
refusing to allow a GitHub App to create or update workflow
```

**Cause:** GitHub Actions doesn't have write permissions

**Solution:**
1. Go to: https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/settings/actions
2. Scroll to "Workflow permissions"
3. Select: **"Read and write permissions"**
4. Check: **"Allow GitHub Actions to create and approve pull requests"**
5. Click **Save**

---

### Issue: Python Dependencies Failed

**Error message:**
```
ModuleNotFoundError: No module named 'requests'
```

**Solution:** ✅ Already in workflow - installs requests automatically

---

### Issue: No Changes to Commit

**Error message:**
```
nothing to commit, working tree clean
```

**Cause:** Dashboard hasn't changed (same data as before)

**Solution:** This is fine! The workflow just exits successfully. Changes only commit when data actually changes.

---

### Issue: API Rate Limit

**Error message:**
```
429 Too Many Requests
```

**Cause:** Too many API calls to Jira in short time

**Solution:** Wait 5-10 minutes and retry

---

## How to Check Workflow Logs

1. Go to: https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions
2. Click on the failed workflow run
3. Click on "update-dashboard" job
4. Expand each step to see detailed logs
5. Look for error messages (usually in red)

---

## Testing Locally Before Pushing

Before relying on GitHub Actions, test locally:

```bash
cd ~/cnv-assigned-jiras-dashboard

# Make sure .env is NOT in repo (it's gitignored)
# Run the script
python3 generate_dashboard.py

# Check if it worked
ls -lh index.html
# Should show 196KB file

# Open to verify
firefox index.html
```

If it works locally but fails in GitHub Actions, it's likely a secrets issue.

---

## Manual Workflow Trigger

To test the workflow:

1. Go to: https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions
2. Click "Update CVE Dashboard" (left sidebar)
3. Click "Run workflow" button (right side)
4. Click "Run workflow" in dropdown
5. Wait 30-60 seconds
6. Refresh page to see status

---

## What the Workflow Does (Step by Step)

```
1. Checkout code
   ✅ Downloads your repo to GitHub's server

2. Set up Python
   ✅ Installs Python 3.11

3. Install dependencies
   ✅ pip install requests

4. Generate dashboard
   ✅ Creates .env with secrets
   ✅ Runs: python3 generate_dashboard.py
   ✅ Generates index.html

5. Commit and push
   ✅ Adds index.html to git
   ✅ Commits if changes exist
   ✅ Pushes to main branch
```

---

## Common Fixes Applied

✅ **Updated filter URL** - Now uses your team filter instead of non-existent filter 110799  
✅ **Removed python-dotenv** - Not needed since we manually create .env  
✅ **Added JIRA_DASHBOARD_FILTER_URL** - Passed to script via environment variable  

---

## Quick Checklist

Before running workflow, verify:

- [ ] **Secrets added** (JIRA_USER_EMAIL + JIRA_API_TOKEN)
- [ ] **Workflow permissions** set to "Read and write"
- [ ] **GitHub Pages enabled** (Settings → Pages)
- [ ] **Latest code pushed** to main branch

---

## Next Steps

1. **Set GitHub Actions permissions:**
   - https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/settings/actions
   - Enable "Read and write permissions"

2. **Verify secrets are set:**
   - https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/settings/secrets/actions
   - Should see 2 secrets listed

3. **Run workflow manually:**
   - https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions
   - Click "Run workflow"

4. **Check logs if it fails:**
   - Click on the run
   - Expand steps to see errors

---

## Still Having Issues?

Share the workflow run URL (like the one you provided) and I can help debug the specific error!

Example: https://github.com/UdayYendva/cnv-assigned-jiras-dashboard/actions/runs/26587961051
