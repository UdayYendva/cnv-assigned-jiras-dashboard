#!/bin/bash
# Script to push dashboard to GitHub
# Run this manually to push your changes

echo "============================================"
echo " Push CVE Dashboard to GitHub"
echo "============================================"
echo ""
echo "Your files are committed and ready to push!"
echo "Total: 350 tickets in dashboard"
echo ""
echo "To push to GitHub, you have 2 options:"
echo ""
echo "Option 1: Use GitHub CLI (if installed)"
echo "  gh auth login"
echo "  git push origin main"
echo ""
echo "Option 2: Use SSH (recommended)"
echo "  # Set remote to use SSH instead of HTTPS"
echo "  git remote set-url origin git@github.com:UdayYendva/cnv-assigned-jiras-dashboard.git"
echo "  git push origin main"
echo ""
echo "Option 3: Push manually from GitHub web UI"
echo "  1. Go to https://github.com/new/import"
echo "  2. Your old repository's clone URL: ~/cnv-assigned-jiras-dashboard"
echo "  3. Or upload files directly via GitHub web interface"
echo ""
echo "Option 4: Use personal access token"
echo "  git remote set-url origin https://YOUR_GITHUB_TOKEN@github.com/UdayYendva/cnv-assigned-jiras-dashboard.git"
echo "  git push origin main"
echo ""
echo "============================================"
echo "Current status:"
cd ~/cnv-assigned-jiras-dashboard
git status
echo ""
echo "Files ready to push:"
git log --oneline
echo "============================================"
