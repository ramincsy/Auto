# ⚙️ تنظیم Git برای Co-Authored Commits

برای نوشتن صحیح commit‌های Co-Authored، باید Git محلی خود را تنظیم کنید.

---

## **مرحله 1: بررسی تنظیمات فعلی Git**

### **Windows (PowerShell):**
```powershell
git config --list
```

### **Mac/Linux:**
```bash
git config --list
```

**نتیجه مثال:**
```
user.name=Your Name
user.email=your@email.com
core.editor=vim
...
```

---

## **مرحله 2: تنظیم نام و ایمیل شخصی**

اگر هنوز تنظیم نشده:

### **تنظیم نام:**
```bash
git config --global user.name "نام شما"
```

مثال:
```bash
git config --global user.name "علی احمدی"
```

### **تنظیم ایمیل:**
```bash
git config --global user.email "your@email.com"
```

مثال:
```bash
git config --global user.email "ali@example.com"
```

### **بررسی:**
```bash
git config --global user.name
git config --global user.email
```

---

## **مرحله 3: نوشتن Co-Authored Commit**

### **روش 1: Terminal**

```bash
# مرحله اول: تغییرات را اضافه کنید
git add .

# مرحله دوم: commit را بنویسید
git commit -m "feat: improve documentation

Co-authored-by: Friend Name <friend@email.com>"
```

### **روش 2: VS Code**

1. **تغییرات را stage کنید** (Ctrl+K, Ctrl+Space)
2. **دکمه commit را کلیک کنید**
3. **این متن را بنویسید:**
   ```
   feat: improve documentation
   
   Co-authored-by: Friend Name <friend@email.com>
   ```
4. **Enter را بزنید**

### **روش 3: GitHub Desktop**

1. **تغییرات را انتخاب کنید**
2. **Summary را بنویسید:** `feat: improve documentation`
3. **Description را بنویسید:**
   ```
   Co-authored-by: Friend Name <friend@email.com>
   ```
4. **Commit کنید**

---

## **نمونه‌های عملی:**

### **مثال 1: Co-Author واحد**
```bash
git commit -m "docs: update README

Co-authored-by: محمد رضایی <mohammad@example.com>"
```

### **مثال 2: چندین Co-Author**
```bash
git commit -m "feat: add new feature

Co-authored-by: Person 1 <person1@example.com>
Co-authored-by: Person 2 <person2@example.com>"
```

### **مثال 3: فارسی و انگلیسی**
```bash
git commit -m "feat: بهبود کد

Co-authored-by: John Doe <john@example.com>"
```

---

## **مشکلات و حل‌ها:**

### **مشکل 1: نام و ایمیل اشتباه است**

**حل 1:** Commit بعدی را درست کنید
```bash
git commit --amend --author="Correct Name <correct@email.com>"
```

**حل 2:** تمام commits را اصلاح کنید (خطرناک!)
```bash
git rebase --root --exec 'git commit --amend --no-edit --author="Correct Name <correct@email.com>"'
```

### **مشکل 2: Co-Author نام اشتباه است**

**حل:** Commit را اصلاح کنید:
```bash
git commit --amend
# سپس متن را تغییر دهید و ذخیره کنید
```

### **مشکل 3: نمی‌تونم multi-line commit بنویسم**

**حل:** از -m دو بار استفاده کنید:
```bash
git commit -m "feat: improve code" -m "Co-authored-by: Friend <friend@email.com>"
```

---

## **ایمیل‌های مختلف برای مخازن مختلف**

اگر می‌خواهید هر مخزن ایمیل متفاوتی داشته باشد:

### **تنظیم محلی (فقط این مخزن):**
```bash
# درون مخزن
git config --local user.email "local@email.com"
```

### **بررسی:**
```bash
git config user.email  # محلی
git config --global user.email  # عمومی
```

---

## **نکات مهم:**

✅ **صحیح:**
```
Co-authored-by: Full Name <email@example.com>
```

❌ **نادرست:**
```
Co-author: Full Name <email@example.com>  # (نام اشتباه)
Co-authored-by: Full Name (email@example.com)  # (فرمت اشتباه)
Co-authored by: Full Name <email@example.com>  # (فاصله نادرست)
```

---

## **GitHub Recognition:**

تا زمانی که ایمیل درست باشد:
- ✅ GitHub فردی را شناسایی می‌کند
- ✅ به contribution graph آنها اضافه می‌شود
- ✅ Pair Extraordinaire نشان برای هر دو باز می‌شود

---

## **دستورات مفید:**

| دستور | توضیح |
|------|--------|
| `git config --list` | نمایش تمام تنظیمات |
| `git config user.name` | نمایش نام |
| `git config user.email` | نمایش ایمیل |
| `git log --oneline` | نمایش commits |
| `git show [commit-hash]` | نمایش جزئیات commit |
| `git commit --amend` | اصلاح commit آخر |

---

## **چک‌لیست:**

- [ ] نام Git را تنظیم کردم
- [ ] ایمیل Git را تنظیم کردم
- [ ] یک commit تست کردم
- [ ] ایمیل دوستم را پیدا کردم
- [ ] یک Co-Authored commit نوشتم
- [ ] Push کردم

---

## **خلاصه سریع:**

```bash
# تنظیم
git config --global user.name "Your Name"
git config --global user.email "your@email.com"

# نوشتن commit عادی
git add .
git commit -m "your message"

# نوشتن Co-Authored commit
git add .
git commit -m "your message

Co-authored-by: Friend <friend@email.com>"

# push
git push origin branch-name
```

---

**آماده‌اید؟ بیایید شروع کنیم!** 🚀
