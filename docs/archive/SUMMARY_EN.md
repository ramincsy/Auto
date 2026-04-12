# 📋 Summary: How to Review and Close Pull Requests for GitHub Achievements

## 🎯 Your Goal
You want to review and close your daily pull requests to earn GitHub achievements.

## ⚠️ Important Note
I cannot directly merge or close PRs because I don't have access to your GitHub credentials. However, I've created comprehensive tools and guides that make this process easy for you.

## ✨ What I Built for You

### 1. Advanced Script: `review_and_merge_prs.py`
A powerful tool that:
- ✅ Analyzes all open PRs
- ✅ Checks PR status (ready to merge, conflicts, etc.)
- ✅ Shows changed files
- ✅ Provides merge recommendations
- ✅ Can auto-merge PRs
- ✅ Tracks your GitHub achievements progress

**File location:** `scripts/review_and_merge_prs.py`

### 2. Comprehensive Guides
- **MERGE_PRS_QUICKSTART.md** - Quick start guide (English)
- **MERGE_PRS_GUIDE.md** - Complete guide (Persian)
- **SUMMARY.md** - Summary in Persian
- **README.md** - Updated with new instructions

## 🚀 How to Use (3 Simple Steps)

### Step 1: Install Dependencies
```bash
cd Auto
pip install -r requirements.txt
```

### Step 2: Set GitHub Token
1. Go to [GitHub Settings > Personal Access Tokens](https://github.com/settings/tokens)
2. Click **Generate new token (classic)**
3. Name: "Merge PRs Script"
4. Select scope: **repo** (full control)
5. Click **Generate token**
6. Copy the token

Then set the token:
```bash
export GITHUB_TOKEN='your_token_here'
```

### Step 3: Run the Script

#### Option A: Review Only (no merging)
```bash
python scripts/review_and_merge_prs.py
```
This analyzes all PRs and tells you which are ready to merge.

#### Option B: Auto-Merge Ready PRs
```bash
python scripts/review_and_merge_prs.py --auto-merge
```
This identifies ready PRs, asks for confirmation, and merges them.

## 📊 Expected Output

When you run the script, you'll see something like:

```
🔍 Fetching GitHub token...
📋 Fetching open pull requests for ramincsy/Auto...

🔍 Analyzing 30 pull request(s)...
  Analyzing PR #3423... ✅
  Analyzing PR #3422... ✅
  ...

================================================================================
📊 PULL REQUEST ANALYSIS
================================================================================

✅ Ready to Merge: 28
⚠️  Has Conflicts: 0
🔄 Still Checking: 0
👀 Review Manually: 2

✅ READY TO MERGE:
--------------------------------------------------------------------------------
  #3423: Daily Update daily-contribution-2026-01-22
    Files: updates/2026/01/22.md, README.md
    Created: 2026-01-22
  ...

💡 To automatically merge ready PRs, run:
   python scripts/review_and_merge_prs.py --auto-merge
```

## 🎯 GitHub Achievements You'll Earn

By using this script and merging PRs:

### ✅ Immediate (Today)
1. **🦈 Pull Shark** - By merging 4+ PRs
2. **🎉 YOLO** - By merging PRs without review
3. **⚡ Quickdraw** - By quickly merging new PRs (within 30 minutes)

### ⏳ Coming Soon
4. **🧠 Galaxy Brain** - By getting 4+ approved reviews from friends
5. **👯 Pair Extraordinaire** - By adding co-authors to commits
6. **⭐ Starstruck** - By getting 25+ stars on repo
7. **🎓 Open Sourcerer** - By maintaining repo for 2+ months (until mid-February)

## 💡 Recommended Strategy

### Today:
```bash
python scripts/review_and_merge_prs.py --auto-merge
```
**Result:** 🦈 Pull Shark + 🎉 YOLO unlocked!

### Daily:
When a new PR is created, within 5-10 minutes:
```bash
python scripts/review_and_merge_prs.py --auto-merge
```
**Result:** ⚡ Quickdraw unlocked!

### Next Week:
- Ask 4 friends to review and approve different PRs
- **Result:** 🧠 Galaxy Brain unlocked!

### Following Weeks:
- Create co-authored commits with friends
- **Result:** 👯 Pair Extraordinaire unlocked!

## 🆚 Script Comparison

You have two scripts:

| Feature | close_all_prs.py | review_and_merge_prs.py |
|---------|------------------|-------------------------|
| Purpose | Close PRs (without merging) | Merge PRs |
| For achievements | ❌ | ✅ |
| Analyze PRs | ❌ | ✅ |
| Check conflicts | ❌ | ✅ |
| Show files | ❌ | ✅ |
| Track achievements | ❌ | ✅ |

**Recommendation:** Use `review_and_merge_prs.py` for GitHub achievements.

## 📚 Full Documentation

For more information:
- **Quick Guide (English):** [MERGE_PRS_QUICKSTART.md](./MERGE_PRS_QUICKSTART.md)
- **Complete Guide (Persian):** [MERGE_PRS_GUIDE.md](./MERGE_PRS_GUIDE.md)
- **Achievements Guide:** [ACHIEVEMENTS.md](./ACHIEVEMENTS.md)
- **Invite Friends:** [HOW_TO_INVITE_FRIENDS.md](./HOW_TO_INVITE_FRIENDS.md)

## 🔐 Security Tips

- ⚠️ **Never** commit your GitHub token
- ✅ Only set token in environment variable
- ✅ After use, revoke token if not needed

## ❓ FAQ

### Q: Can I merge PRs manually?
**A:** Yes! Use GitHub UI:
```
https://github.com/ramincsy/Auto/pulls
```

### Q: What if a PR has conflicts?
**A:** Resolve manually:
```bash
git checkout main
git pull origin daily-contribution-YYYY-MM-DD
# Resolve conflicts
git add .
git commit
git push
```

### Q: Do I need to merge all PRs?
**A:** For Pull Shark you need at least 4 PRs, but merging all is better.

### Q: How long until I see achievements?
**A:** Usually a few hours to one day after merging PRs.

## 🎉 Summary

You now have everything you need:
1. ✅ A powerful script for review & merge
2. ✅ Complete guides in two languages
3. ✅ Clear strategy for achievements
4. ✅ Updated documentation

**Your Next Steps:**
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set token
export GITHUB_TOKEN='your_token_here'

# 3. Merge PRs!
python scripts/review_and_merge_prs.py --auto-merge
```

**Good luck! 🚀**

---

**Note:** If you have questions or need more help, read the complete guides or ask for assistance.
