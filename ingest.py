import os
from config import SAMPLE_PDF_PATH
from pdf_reader import extract_pages_from_pdf
from chunker import create_chunks_from_pages
from print_format import format_farsi

# ۱. بررسی وجود فایل نمونه PDF
if not os.path.exists(SAMPLE_PDF_PATH):
    print(f"❌ خطا: فایل {SAMPLE_PDF_PATH} پیدا نشد!")
else:
    print("⏳ در حال خواندن فایل PDF...")
    pages = extract_pages_from_pdf(str(SAMPLE_PDF_PATH))
    print(f"✅ مرحله اول کامل شد: تعداد کل صفحات: {len(pages)}")

    print("\n⏳ در حال تبدیل صفحات به چانک‌های معنایی...")
    chunks = create_chunks_from_pages(pages)
    print(f"✅ مرحله دوم کامل شد: تعداد کل چانک‌ها: {len(chunks)}")
    print("-" * 50)

    # نمایش اطلاعات چند چانک اول به عنوان نمونه
    if chunks:
        print("🔍 بررسی نمونه چانک شماره ۱:")
        print(f"📌 شناسه چانک: {chunks[0]['chunk_id']}")
        print(f"📄 شماره صفحه اصلی: {chunks[0]['page_number']}")
        print(f"📏 طول کاراکتری متن چانک: {len(chunks[0]['text'])}")
        print("📝 متن چانک:")
        print(chunks[0]['text'][:300] + " ... [ادامه دارد]")
        print("=" * 50)


from vector_store import add_chunks_to_vector_store

# ... بعد از بخش تولید چانک‌ها ...
print("\n⏳ در حال تبدیل چانک‌ها به بردار و ذخیره‌سازی در ChromaDB...")
add_chunks_to_vector_store(chunks)
