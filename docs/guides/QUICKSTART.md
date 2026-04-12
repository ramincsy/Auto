# ⚡ Quick Start Guide

سریع‌ترین راه برای شروع استفاده از این ریپو.

## 🚀 تنظیم ۵ دقیقه‌ای (محلی)

### Windows
```powershell
# Clone و setup
git clone https://github.com/yourusername/Auto.git
cd Auto
setup.bat
```

### macOS / Linux
```bash
# Clone و setup
git clone https://github.com/yourusername/Auto.git
cd Auto
chmod +x setup.sh
./setup.sh
```

## 📝 استفاده روزانه

### Automated (GitHub Actions)
✅ **هر روز ساعت ۰:۰۰ UTC** - خودکار اجرا می‌شود

### Manual
```bash
# تولید یک contribution جدید
python generate_content.py

# یک یادداشت اضافه کنید
python scripts/log_daily.py --note "دستاوردم امروز: ..."

# توپیک‌های موجود را ببینید
python scripts/log_daily.py --list

# تغییرات را ببینید
git status
git diff README.md
```

## 🔗 GitHub Setup

### ۱. Fine-Grained PAT ایجاد کنید
1. رفتن به: https://github.com/settings/tokens?type=beta
2. "Generate new token" کلیک کنید
3. نام: `gh_token_auto_contributions`
4. Expiration: ۹۰ روز (یا بیشتر)
5. Resource owner: `ramincsy` (اکانت شما)
6. Permissions:
   - `Contents: Read and Write`
7. Generate کنید و copy کنید

### ۲. Token را در Secrets ذخیره کنید
1. رفتن به: https://github.com/ramincsy/Auto/settings/secrets/actions
2. "New repository secret"
3. Name: `GH_TOKEN2`
4. Value: PAT‌ای که copy کردید
5. Add secret

### ۳. بررسی Workflow
1. رفتن به: https://github.com/ramincsy/Auto/actions
2. "Daily Contributions (Safe)" را کلیک کنید
3. "Run workflow" → "Run workflow"
4. منتظر ۲-۳ دقیقه بمانید

## 📊 دستاوردها را بگیرید

### ۱️⃣ **Pull Shark** (۴ روز)
```bash
# هر روز اتومات یک PR ایجاد می‌شود
# شما آن را merge کنید:
git checkout main
git pull origin daily-contribution-YYYY-MM-DD
git merge --no-ff daily-contribution-YYYY-MM-DD
git push origin main
```
> ۴ بار تکرار کنید

### ۲️⃣ **Quickdraw** (فوری)
- PR را بلافاصله merge کنید (< ۳۰ دقیقه)
- بیشتر، بهتر

### ۳️⃣ **Galaxy Brain** (۱ هفته)
```bash
# دوست را invite کنید برای review
# آنها باید "Approve" کنند
# حداقل ۴ approval لازم است
```

### ۴️⃣ **Pair Extraordinaire** (هر روز)
```bash
# Co-authored commit:
git commit -m "feat: improvement

Co-authored-by: Friend <friend@email.com>"
```

### ۵️⃣ **Starstruck** (۲+ هفته)
- کیفیت کد بالا نگاهداری کنید
- دوستان را invite کنید
- مستندسازی بهتر تنظیم کنید

### ۶️⃣ **Open Sourcerer** (۶۰ روز)
- اتومات ✅
- فقط منتظر بمانید

---

## 🔧 Customization

### توپیک‌های خود را تنظیم کنید
ویرایش `config/topics.json`:
```json
{
  "topics": [
    "Your Topic 1",
    "Your Topic 2",
    "Your Topic 3"
  ]
}
```

### زمان Workflow را تغییر دهید
ویرایش `.github/workflows/daily-contribution.yml`:
```yaml
schedule:
  - cron: '0 2 * * *'  # ۲ صبح UTC
```

---

## 🆘 Troubleshooting

### Workflow ناموفق؟
1. رفتن به Actions tab
2. آخرین run را کلیک کنید
3. Logs را بررسی کنید
4. معمول‌اً عدم‌وجود Token است

### README تغییر نمی‌کند؟
```bash
# محلی آزمایش کنید:
python generate_content.py
git status  # باید README تغییر کند
```

### یک روز PR ایجاد نشد؟
```bash
# بررسی git config:
git config --global user.email
git config --global user.name
```

---

## 📞 Commands Reference

```bash
# Generate contribution
python generate_content.py

# Log a note
python scripts/log_daily.py --note "Your note"

# View available topics
python scripts/log_daily.py --list

# View workflow runs
gh run list --repo ramincsy/Auto

# Manual merge PR
git merge --no-ff origin/daily-contribution-YYYY-MM-DD

# Create feature PR
git checkout -b feature/your-feature
# Make changes
git commit -m "feat: description"
git push origin feature/your-feature
```

---

## 🎯 Expected Timeline

| Day | What Happens |
|-----|-------------|
| Day 1 | First PR created, Quickdraw possible |
| Day 4 | 4 merged PRs = Pull Shark ✅ |
| Day 7 | With 4 approvals = Galaxy Brain ✅ |
| Day 7 | With co-authored = Pair Extraordinaire ✅ |
| Week 2 | With 25 stars = Starstruck ✅ |
| Day 60 | Open Sourcerer ✅ |

---

## 🎉 Next Steps

1. ✅ Fork یا Clone کنید
2. ✅ Setup کنید
3. ✅ Token را add کنید
4. ✅ Workflow را run کنید
5. ✅ دوستان را invite کنید
6. ✅ دستاوردها جمع کنید! 🏆

---

**Happy Contributing!** 🚀
