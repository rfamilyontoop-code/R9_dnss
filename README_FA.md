# R9 DNS Generator — راه‌اندازی آنلاین

این پروژه یک وب‌سایت کامل با بک‌اند Python است. فایل HTML را جداگانه باز نکنید؛ API باید روی سرور اجرا شود.

## انتشار در Render با GitHub
1. در github.com حساب بسازید یا وارد شوید.
2. یک مخزن جدید با نام r9-dns-generator بسازید (ترجیحاً Private).
3. فایل‌های **داخل** پوشه R9_DNS_Generator را در ریشه مخزن آپلود و Commit کنید. پوشه static باید به همان شکل باقی بماند.
4. در dashboard.render.com وارد شوید، New > Blueprint را انتخاب کنید و GitHub را متصل کنید.
5. مخزن r9-dns-generator را انتخاب کنید. Render فایل render.yaml را می‌خواند.
6. Apply/Deploy را بزنید. پس از تکمیل استقرار، آدرس https://...onrender.com را باز کنید.
7. کشور، نوع آدرس و Generate را آزمایش کنید. روی طرح رایگان ممکن است اولین بار راه‌اندازی چند ثانیه طول بکشد.

نکته: آدرس‌های برگشتی IP نیم‌سرورهای authoritative هستند؛ لزوماً resolver عمومی قابل استفاده در تنظیمات DNS گوشی نیستند. برخی دامنه‌ها ممکن است رکورد A یا AAAA نیم‌سرور نداشته باشند یا DNS lookup با خطا مواجه شود.

## اجرای محلی
pip install -r requirements.txt
python server.py
سپس http://localhost:8000 را باز کنید.
