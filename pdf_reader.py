import json
from pathlib import Path
from pypdf import PdfReader
from config import PROCESSED_DIR # وارد کردن مسیر از کانفیگ

def extract_pages_from_pdf(pdf_path: str, save_json: bool = True):
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"فایلی در مسیر '{pdf_path}' پیدا نشد!")

    reader = PdfReader(str(path))
    total_pages = len(reader.pages)
    print(f"📄 فایل با موفقیت باز شد. تعداد کل صفحات: {total_pages}")

    extracted_documents = []
    full_text = ""

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = text.strip()

        if text:
            extracted_documents.append({
                "page_number": page_number,
                "text": text,
                "char_count": len(text),
            })
            full_text += text + "\n\n"
        else:
            print(f"⚠️ صفحه {page_number} خالی یا شامل تصویر بدون متن بود.")

    # ذخیره‌سازی استاندارد در پوشه مشخص‌شده در config.py
    if save_json:
        # نام فایل json بر اساس نام PDF ساخته می‌شود
        json_filename = f"{path.stem}.json"
        json_path = PROCESSED_DIR / json_filename
        
        data_to_save = {
            "metadata": {
                "source": str(path),
                "total_pages": total_pages,
                "file_name": path.name
            },
            "full_text": full_text,
            "pages": extracted_documents
        }
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)
        print(f"💾 نسخه متنی مقاله در '{json_path}' ذخیره شد.")

    return extracted_documents
