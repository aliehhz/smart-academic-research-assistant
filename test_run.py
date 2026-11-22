from vector_store import search_documents
from print_format import format_farsi

def main():
    # یک سوال آزمایشی به زبان انگلیسی (متناسب با مقاله شما)
    query = "What is APD?"
    
    print(f"🔍 در حال جستجوی مفهوم: '{query}' ...\n")
    
    # ۳ تا از شبیه‌ترین بخش‌ها را واکشی می‌کنیم
    results = search_documents(query=query, n_results=3)
    
    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0] if "distances" in results else []
    
    print("=" * 50)
    print("🎯 نتایج پیدا شده از میان چانک‌ها:")
    print("=" * 50)
    
    ids = results.get("ids", [[]])[0]

    for i, (doc, meta, chunk_id) in enumerate(zip(documents, metadatas, ids), start=1):
        page = meta.get("page_number", "نامشخص")
        print(f"\n[{i}] نتیجه از صفحه: {page} (شناسه چانک: {chunk_id})")
        print("-" * 40)
        print(doc)
        print("-" * 40)

if __name__ == "__main__":
    main()
