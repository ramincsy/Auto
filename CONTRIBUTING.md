# Contributing Guidelines

درخواست شما برای کمک گرفتن به اینجا است.

## 🎯 نحوه کمک

### 1. محلی تست کنید

```bash
# Clone کنید
git clone https://github.com/yourusername/Auto.git
cd Auto

# محیط راه‌اندازی کنید
python -m venv venv
source venv/bin/activate  # یا `venv\Scripts\activate` در Windows

# وابستگی‌ها نصب کنید
pip install -r requirements.txt
pip install pre-commit

# Pre-commit hooks را راه‌اندازی کنید
pre-commit install
```

### 2. تغییرات خود را انجام دهید

```bash
# یک feature branch بسازید
git checkout -b feature/your-feature

# تغییرات خود را انجام دهید
# تست‌ها را اجرا کنید
python generate_content.py

# Pre-commit را اجرا کنید
pre-commit run --all-files
```

### 3. Commit و Push کنید

```bash
git add .
git commit -m "feat: توضیح تغییر شما"
git push origin feature/your-feature
```

### 4. Pull Request ایجاد کنید

- شناسنامه واضح بنویسید
- مسائل مرتبط را ذکر کنید
- نمونه کد یا اسکرین‌شات اضافه کنید اگر مربوطه باشد

## 📋 Commit Message Format

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat`: ویژگی جدید
- `fix`: رفع باگ
- `docs`: تغییر مستندسازی
- `style`: فرمت‌بندی (بدون تغییر کد)
- `refactor`: بازسازی کد بدون تغییر رفتار
- `perf`: بهبود عملکرد
- `test`: اضافه کردن/تغییر تست‌ها
- `chore`: تغییرات ساختاری

**مثال:**
```
feat(generate_content): add topic rotation logic

Implement weekly topic rotation to avoid repetition
and improve variety in daily contributions.

Closes #5
```

## 🔍 Code Quality

- **Format**: `black` - خودکار توسط pre-commit
- **Lint**: `ruff` - خودکار توسط pre-commit
- **Style**: PEP 8

## 📝 مستندسازی

- Docstring‌ها اضافه کنید برای توابع عمومی
- توضیحات واضح برای منطق پیچیده
- اگر رفتار تغییر می‌کند، README را به‌روزرسانی کنید

## 🧪 تست

```bash
# تست روزانه تولید محتوا
python generate_content.py

# بررسی فایل‌های ایجاد شده
ls -la updates/YYYY/MM/
cat README.md | grep "Contributions for"
```

## ❌ چه کاری را دوری کنید

- Force-push (`git push --force`)
- Hard resets روی main
- بدون توضیح تغییرات بزرگ
- PR‌های بدون شناسنامه مناسب

## ✅ Merge Policy

- حداقل یک تصویب مورد نیاز است
- CI checks باید pass کنند
- Squash merge برای feature branches
- PR باید از main شاخه‌ای باشد

## 💬 سؤالات؟

- Issues را باز کنید برای بگ‌ها یا پیشنهادات
- Discussions برای اکتشاف ایده‌های بزرگ
- Email: ramincsy2@gmail.com

---

**مشکور بابت کمک‌کردن!** 🙏
