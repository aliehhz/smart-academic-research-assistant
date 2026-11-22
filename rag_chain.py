from typing import List, Dict, Any
# وارد کردن تابع جستجو از فایلی که قبلا نوشتی
from vector_store import search_documents 
from llm_service import get_gemini_response
from pathlib import Path


def retrieve_chunks(query: str, top_k: int = 10) -> List[Dict[str, Any]]:
    """این تابع خروجی خام کروما را به لیست تمیز تبدیل می‌کند"""
    results = search_documents(query, n_results=top_k)

    if not results.get("documents") or not results["documents"][0]:
        return []

    # استخراج داده‌ها از لیست‌های تو در توی کروما
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]
    ids = results["ids"][0]

    chunks = []
    for c_id, text, meta, dist in zip(ids, documents, metadatas, distances):
        chunks.append({
            "chunk_id": c_id,
            "text": text,
            "page": meta.get("page_number") if meta else "؟",
            "source": meta.get("source") if meta else "نامشخص",
            "distance": dist
        })
    return chunks

def generate_rag_response(query: str, top_k: int = 3, distance_threshold: float = 1.8) -> str:
    print(f"🔍 جستجو برای: '{query}'")
    chunks = retrieve_chunks(query, top_k=top_k)

    if not chunks:
        return "❌ هیچ داده‌ای در دیتابیس یافت نشد. آیا فایلی را قبلاً آپلود کرده‌ای؟"

    # --- بخش دیباگ برای دیدن فاصله‌ها ---
    print("📋 وضعیت چانک‌های پیدا شده:")
    for c in chunks:
        print(f"   📍 Distance: {c['distance']:.4f} | Text: {c['text'][:50]}...")

    # فیلتر کردن بر اساس آستانه دقت
    valid_chunks = [c for c in chunks if c["distance"] <= distance_threshold]

    if not valid_chunks:
        min_dist = min([c['distance'] for c in chunks])
        return f"❌ نتیجه دقیقی یافت نشد. (بهترین فاصله: {min_dist:.4f} ولی حد ما {distance_threshold} است)"

    # ساخت کانتکست برای جمنای
    context = "\n\n".join([f"منبع: {c['source']} ص {c['page']}:\n{c['text']}" for c in valid_chunks])
    
    prompt = f"فقط بر اساس متن زیر پاسخ بده:\n{context}\n\nسوال: {query}"
    
    print("🤖 ارسال به جمنای...")
    return get_gemini_response(prompt)

if __name__ == "__main__":
    # اجرای تست
    print(generate_rag_response("What is APD?"))