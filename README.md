# 🚀 Auto Contributions

> Automated daily contributions toward GitHub Achievements

## 🎯 Project Goal

این پروژه برای خودکارسازی ثبت روزانه مشارکت‌ها و دستیابی به دستاوردهای GitHub طراحی شده است.

**Target Achievements:**
- ✅ Pull Shark – Create consistent pull requests
- ✅ Open Sourcerer – Maintain a healthy open source project
- ✅ Pair Extraordinaire – Encourage code collaboration
- ✅ Quickdraw – Fast daily contributions
- ✅ Starstruck – Build a valuable repository
- ✅ Galaxy Brain – High-quality code
- ✅ YOLO – Risk-managed automation
- 🎯 Heart On Your Sleeve – Meaningful contributions
- 🎯 Arctic Code Vault Contributor – Long-term maintenance

## 📋 Features

- **Daily Automation**: روزانه یک commit و یک PR معنادار
- **Topic Rotation**: تنوع موضوعات هفتگی برای تنوع در مشارکت
- **Quality Checks**: Pre-commit hooks with `black` و `ruff`
- **Safe Workflow**: بدون force-push، stash، یا اسپم
- **Persian & English**: دوزبانه خروجی‌ها
- **Structured Updates**: هر روز یک فایل `updates/YYYY/MM/DD.md`
- **PR Management**: اسکریپت برای بستن تمام PR ها ([راهنما](./CLOSE_PRS_GUIDE.md))

## 🛠️ Setup

### محیط محلی

```bash
# Clone repository
git clone https://github.com/yourusername/Auto.git
cd Auto

# Install dependencies
pip install -r requirements.txt

# Install pre-commit hooks
pre-commit install

# Run daily contribution manually
python generate_content.py
```

### GitHub Actions Setup

1. مطمئن شوید برنچ `main` اصلی است
2. یک Fine-Grained Personal Access Token ایجاد کنید:
   - Scope: `Contents: Read and Write` برای این repo
   - ذخیره آن در Secrets با نام `GH_TOKEN2`
3. Workflow خودکار هر روز ساعت ۰:۰۰ UTC اجرا می‌شود

## 📂 Project Structure

```
Auto/
├── .github/
│   └── workflows/
│       └── daily-contribution.yml    # Automated workflow
├── config/
│   └── topics.json                   # Configurable topics
├── updates/
│   └── YYYY/MM/DD.md                # Daily updates
├── generate_content.py               # Main content generator
├── requirements.txt                  # Python dependencies
├── .pre-commit-config.yaml          # Code quality hooks
└── README.md                         # This file
```

## 🔄 Workflow

### روزانه اتفاق می‌افتد:

1. GitHub Actions در ساعت ۰:۰۰ UTC trigger می‌شود
2. اسکریپت `generate_content.py` اجرا می‌شود:
   - یک موضوع جدید به `README.md` اضافه می‌شود
   - فایل `updates/YYYY/MM/DD.md` ایجاد می‌شود
3. یک commit ایجاد و push می‌شود
4. یک Pull Request به برنچ `main` باز می‌شود
5. PR متن توضیحی دارد و لینک به فایل روزانه است

### محلی:

```bash
# Generate today's contribution
python generate_content.py

# Check generated files
git status

# Make additional changes if needed
git add .
git commit -m "Manual daily update: $(date +%Y-%m-%d)"
git push
```

## 🎨 Customization

### موضوعات خود را تغییر دهید

در فایل `config/topics.json`:

```json
{
  "topics": [
    "Your Custom Topic 1",
    "Your Custom Topic 2",
    "Your Custom Topic 3"
  ]
}
```

### تغییر زمان Workflow

در `.github/workflows/daily-contribution.yml`:

```yaml
on:
  schedule:
    - cron: '0 0 * * *'  # تغییر این خط (CRON format)
```

## 📊 Statistics

- **Commits/Month**: ~30 (یک روز یکی)
- **PRs/Month**: ~30 (تعامل واقعی)
- **Code Quality**: Enforced via pre-commit
- **Sustainability**: صفر اسپم، صفر force-push

## 🔧 مدیریت Pull Request ها

### ✅ Merge کردن PR ها (پیشنهادی برای دستاوردهای GitHub)

برای بررسی و merge کردن PR های روزانه به منظور دستیابی به دستاوردهای GitHub:

```bash
# Install dependencies (if not already)
pip install -r requirements.txt

# Set your GitHub token
export GITHUB_TOKEN='your_token_here'

# Review PRs (without merging)
python scripts/review_and_merge_prs.py

# Auto-merge ready PRs
python scripts/review_and_merge_prs.py --auto-merge
```

📖 **راهنماهای کامل**:
- [MERGE_PRS_QUICKSTART.md](./MERGE_PRS_QUICKSTART.md) - راهنمای سریع (English)
- [MERGE_PRS_GUIDE.md](./MERGE_PRS_GUIDE.md) - راهنمای کامل (فارسی)

🎯 **دستاوردها**: با merge کردن PR ها، دستاوردهای Pull Shark 🦈، Quickdraw ⚡ و YOLO 🎉 را بدست می‌آورید!

### ❌ بستن تمام PR های باز

اگر نیاز دارید تمام PR های باز را ببندید (بدون merge):

```bash
# Set your GitHub token
export GITHUB_TOKEN='your_token_here'

# Close all PRs
python scripts/close_all_prs.py
```

📖 **راهنمای کامل**: [CLOSE_PRS_GUIDE.md](./CLOSE_PRS_GUIDE.md)

⚠️  **نکته**: برای دستیابی به دستاوردهای GitHub، بهتر است PR ها را merge کنید، نه close!

## 👥 دعوت دوستان برای کمک

**می‌خواهید دوستانتان برای رسیدن به نشان‌های GitHub کمک کنند؟**

👉 **راهنمای کامل:** [HOW_TO_INVITE_FRIENDS.md](./HOW_TO_INVITE_FRIENDS.md)

### سه راه برای کمک:

1. **Code Review** (🧠 Galaxy Brain)
   - [راهنمای فارسی](./FRIENDS_GUIDE.md)
   - [English Guide](./FRIENDS_GUIDE_EN.md)

2. **Pull Request Merge** (🐋 Pull Shark)
   - راهنما در فایل‌های بالا

3. **Co-Authored Commits** (👥 Pair Extraordinaire)
   - [Git Setup Guide](./GIT_SETUP_FOR_COAUTHOR.md)
   - [نقش‌های مختلف](./FRIEND_ROLES.md)

### پیام‌های آماده:
- [دعوت‌نامه‌های آماده](./FRIEND_INVITATION_MESSAGES.md)
- فقط کپی و پیست کنید! 📋

## 🤝 Contributing

اگر می‌خواهید به بهبود این پروژه کمک کنید:

1. یک Fork ایجاد کنید
2. یک Feature Branch بسازید (`git checkout -b feature/xyz`)
3. تغییرات خود را commit کنید
4. یک Pull Request باز کنید

یا:
- 👉 [نقش‌های مختلف برای کمک](./FRIEND_ROLES.md)

## 📝 License

This project is open source and available under the MIT License.

## 💡 Tips for Achievements

- **Pull Shark**: PRها باید معنادار باشند (تنها تغییر محتوا کافی است)
- **Open Sourcerer**: ریپو بیش از ۲ ماه فعال باشد + خوب پروژه‌ای باشد
- **Quickdraw**: PR باید خیلی سریع merge شود (خودکار پذیرش ریسک‌دار است؛ بهتر دستی merge کنید)
- **Starstruck**: ریپو جذاب و مفید باشد تا ستاره دریافت کند
- **Galaxy Brain**: کد باید high-quality باشد (pre-commit و تست‌ها کمک می‌کند)
- **Pair Extraordinaire**: با دیگران در PR collaborate کنید
- **YOLO**: از automation احتیاط کنید و قوانین GitHub را دنبال کنید

---

**Last Updated**: {{DATE}}
**Maintained by**: ramincsy


## 📅 2025-12-13
- 📚 Studied: Cloud Computing & DevOps
- 📚 Studied: Cloud Computing & DevOps
- 📚 Studied: Cloud Computing & DevOps

## 📅 2025-12-14
- 📚 Studied: Cloud Computing & DevOps
- 📚 Studied: Cloud Computing & DevOps
- 📚 Studied: Cloud Computing & DevOps

## 📅 2025-12-17
- 📚 Studied: Data Science & Analytics
- 📚 Studied: Data Science & Analytics
- 📚 Studied: Data Science & Analytics

## 📅 2025-12-18
- 📚 Studied: Data Science & Analytics
- 📚 Studied: Data Science & Analytics
- 📚 Studied: Data Science & Analytics

## 📅 2025-12-23
- 📚 Studied: Open Source Contribution
- 📚 Studied: Open Source Contribution
- 📚 Studied: Open Source Contribution

## 📅 2026-01-02
- 📚 Studied: Web Development (Frontend/Backend)
- 📚 Studied: Web Development (Frontend/Backend)
- 📚 Studied: Web Development (Frontend/Backend)

## 📅 2026-01-29
- 📚 Studied: Security & Best Practices
- 📚 Studied: Security & Best Practices
- 📚 Studied: Security & Best Practices

## 📅 2026-02-08
- 📚 Studied: System Design
- 📚 Studied: System Design
- 📚 Studied: System Design

## 📅 2026-02-24
- 📚 Studied: Web Development (Frontend/Backend)
- 📚 Studied: Web Development (Frontend/Backend)
- 📚 Studied: Web Development (Frontend/Backend)
