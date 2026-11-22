import os
from pathlib import Path
from print_format import format_farsi

# --- مسیرهای پروژه (Project Paths) ---
# پیدا کردن مسیر اصلی پروژه به صورت داینامیک
BASE_DIR = Path(__file__).resolve().parent

# پوشه داده‌ها برای ذخیره PDFها
DATA_DIR = BASE_DIR / "data"

# پوشه پایگاه داده برداری (ChromaDB)
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# مطمئن می‌شویم پوشه‌ها وجود دارند
DATA_DIR.mkdir(exist_ok=True)
CHROMA_DB_DIR.mkdir(exist_ok=True)

PROCESSED_DIR = DATA_DIR / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


# --- تنظیمات پردازش متن (Text Processing Settings) ---
# اندازه هر چانک (بر حسب کاراکتر)
CHUNK_SIZE = 1000

# میزان همپوشانی چانک‌ها برای حفظ پیوستگی معنایی
CHUNK_OVERLAP = 200


# --- تنظیمات مدل هوش مصنوعی (AI Model Settings) ---
# نام مدل امبدینگ که از Sentence-Transformers استفاده می‌کنیم
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# مسیر ذخیره‌سازی محلی دیتابیس کروما
CHROMA_PATH = BASE_DIR / "chroma_db"


# --- تنظیمات فایل‌ها (File Settings) ---
# فعلاً برای تست، نام فایل اصلی رو اینجا می‌ذاریم
SAMPLE_PDF_NAME = "sample.pdf"
SAMPLE_PDF_PATH = DATA_DIR / SAMPLE_PDF_NAME

print(f"✅ تنظیمات با موفقیت از config.py بارگذاری شد.")
