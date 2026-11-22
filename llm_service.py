import os
import time
from dotenv import load_dotenv
from google import genai
from print_format import format_farsi

# بارگذاری تنظیمات از فایل .env
load_dotenv()

# لیست مدل‌های کاندیدا به ترتیب اولویت (از سبک به سنگین برای پایداری بیشتر)
CANDIDATE_MODELS = [
    "gemini-flash-lite-latest",   # نسخه آخر لایت
    "gemini-flash-latest"         # نسخه آخر فلش
    "gemini-2.5-flash-lite",      # اولویت اول: بسیار پایدار و سریع
    "gemini-2.5-flash",           # اولویت دوم: مدل استاندارد
    "gemini-3.8-flash",           # اولویت سوم: جدیدترین مدل
    
]

def get_gemini_response(prompt: str) -> str:
    """
    ارسال درخواست به جمنای با قابلیت سوییچ خودکار بین مدل‌ها در صورت شلوغی سرور.
    """
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        return "❌ خطا: GOOGLE_API_KEY در فایل .env پیدا نشد."

    # ایجاد کلاینت بدون تنظیمات پروکسی (استفاده از تنظیمات پیش‌فرض سیستم)
    client = genai.Client(api_key=api_key)

    for model_name in CANDIDATE_MODELS:
        try:
            print(f"🔄 در حال تلاش با مدل: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            # اگر پاسخ موفقیت‌آمیز بود، متن رو برگردون
            if response.text:
                print(f"✅ موفقیت با مدل {model_name}!\n")
                return response.text
            
        except Exception as e:
            error_msg = str(e).upper()
            # تشخیص خطاهای موقت (شلوغی سرور یا عدم دسترسی به مدل خاص)
            if "503" in error_msg or "UNAVAILABLE" in error_msg:
                print(f"⚠️ مدل {model_name} شلوغ است (503). سوییچ به مدل بعدی...")
            elif "404" in error_msg or "NOT_FOUND" in error_msg:
                print(f"⚠️ مدل {model_name} در دسترس نیست (404). سوییچ به مدل بعدی...")
            else:
                # برای خطاهای دیگر (مثل قطع بودن اینترنت)، پیام خطا رو نشون بده و ادامه بده
                print(f"❌ خطا در مدل {model_name}: {e}")
            
            # یک ثانیه صبر قبل از تست مدل بعدی
            time.sleep(1)

    return "❌ متأسفانه در حال حاضر هیچ‌کدام از مدل‌های جمنای پاسخگو نیستند. لطفاً وضعیت اینترنت یا فیلترشکن خود را بررسی کنید."

if __name__ == "__main__":
    print("🚀 شروع تست هوشمند اتصال به جمنای (بدون پروکسی)...\n")
    test_prompt = "سلام! اگه صدام رو می‌شنوی بگو 'سیستم آماده است'."
    answer = get_gemini_response(test_prompt)
    
    print("-" * 30)
    print("پاسخ نهایی:")
    print(answer)
    print("-" * 30)
