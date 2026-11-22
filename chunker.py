"""
ماژول خرد کردن متن (Chunking) برای پایپ‌لاین RAG.
این ماژول متن‌های استخراج‌شده از PDF را به تکه‌های کوچک‌تر با هم‌پوشانی مشخص تبدیل می‌کند.
"""

from typing import List, Dict, Any
from config import CHUNK_SIZE, CHUNK_OVERLAP
from print_format import format_farsi


def create_chunks_from_pages(pages_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    دریافت لیست صفحات استخراج‌شده و تبدیل آن‌ها به چانک‌های کوچک‌تر همراه با متادیتا (شماره صفحه).

    :param pages_data: لیستی از دیکشنری‌ها که شامل شماره صفحه و متن آن صفحه است.
    :return: لیستی از دیکشنری‌های چانک شده شامل متن چانک، شماره صفحه و شناسه چانک.
    """
    all_chunks = []
    chunk_counter = 0

    for page in pages_data:
        page_number = page.get("page_number")
        text = page.get("text", "").strip()

        if not text:
            continue

        start = 0
        text_length = len(text)

        # برش دادن متن صفحه به گام‌های CHUNK_SIZE با هم‌پوشانی CHUNK_OVERLAP
        while start < text_length:
            end = start + CHUNK_SIZE
            chunk_text = text[start:end]

            chunk_counter += 1
            all_chunks.append({
                "chunk_id": f"chunk_{chunk_counter}",
                "page_number": page_number,
                "text": chunk_text
            })

            # حرکت پنجره به جلو (منهای میزان هم‌پوشانی)
            start += (CHUNK_SIZE - CHUNK_OVERLAP)

    return all_chunks


if __name__ == "__main__":
    # تست سریع داخلی ماژول
    sample_pages = [
        {"page_number": 1, "text": "این یک متن تست برای بررسی نحوه کارکرد چانکر است. " * 30}
    ]
    chunks = create_chunks_from_pages(sample_pages)
    print(f"✅ تست چانکر موفقیت‌آمیز بود! تعداد چانک‌های ساخته‌شده: {len(chunks)}")
    if chunks:
        print(f"نمونه چانک اول (صفحه {chunks[0]['page_number']}):\n{chunks[0]['text'][:100]}...")
