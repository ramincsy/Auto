# 🔒 Security Policy

## Reporting Security Issues

اگر یک آسیب‌پذیری امنیتی کشف کردید، **لطفاً آن را به صورت عمومی منتشر نکنید**.

به‌جایش، لطفاً ایمیل بزنید به:
- ramincsy2@gmail.com

لطفاً موارد زیر را شامل کنید:
- توضیح آسیب‌پذیری
- مراحل بازتولید
- تاثیر احتمالی
- پیشنهادات اصلاح (اگر دارید)

## Supported Versions

| Version | مدت پشتیبانی |
|---------|------------|
| 1.x     | فعال      |

## Security Best Practices

هنگام استفاده از این پروژه:

1. **Tokens**: هرگز Personal Access Tokens را در کد commit نکنید
2. **Secrets**: تمام sensitive data را در GitHub Secrets ذخیره کنید
3. **Permissions**: از Fine-Grained PAT‌ها برای حداقل permissions استفاده کنید
4. **Logs**: هیچ sensitive info را در logs یا commit messages نگذارید

## Security Checks

این پروژه از استفاده می‌کند:
- Pre-commit hooks برای کیفیت کد
- GitHub Secrets برای token management
- Read-only source checkout
- Safe git operations (بدون force-push)

## Compliance

- ✅ بدون اسپم یا automation abuse
- ✅ بدون scraping یا unauthorized access
- ✅ تمام actions GitHub ToS را دنبال می‌کند

---

**شکر برای کمک به حفاظت این پروژه** 🛡️
