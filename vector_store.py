from pathlib import Path
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings
from config import CHROMA_PATH, EMBEDDING_MODEL_NAME
from print_format import format_farsi


def get_chroma_collection(collection_name: str = "pdf_documents"):
    """
    ایجاد کلاینت محلی و پایدار ChromaDB به همراه تنظیم مدل Embedding
    """
    # تعریف مدل تبدیل متن به بردار
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name=EMBEDDING_MODEL_NAME
    )

    # ایجاد اتصال محلی (داده‌ها داخل پوشه chroma_db روی سیستم ذخیره می‌شوند)
    client = chromadb.PersistentClient(
    path=str(CHROMA_PATH),
    settings=Settings(anonymized_telemetry=False, is_persistent=True)
    )


    # ساخت یا بازیابی مجموعه
    collection = client.get_or_create_collection(
        name=collection_name,
        embedding_function=embedding_func
    )
    return collection


def add_chunks_to_vector_store(chunks: List[Dict[str, Any]]) -> None:
    """
    دریافت لیست چانک‌ها و ذخیره‌سازی آن‌ها به همراه بردارها در دیتابیس
    """
    if not chunks:
        print("هیچ چانکی برای ذخیره وجود ندارد.")
        return

    collection = get_chroma_collection()

    ids = [chunk["chunk_id"] for chunk in chunks]
    documents = [chunk["text"] for chunk in chunks]
    metadatas = [
    {
        "page_number": chunk["page_number"],
        "source": chunk.get("source", "unknown"),
    }
    for chunk in chunks
]



    # افزودن داده‌ها به دیتابیس (کروما خودش بردارها را می‌سازد و ذخیره می‌کند)
    collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )
    print(f"✅ تعداد {len(chunks)} چانک با موفقیت روی سیستم در پوشه {CHROMA_PATH.name} ذخیره شد.")

def search_documents(query: str, n_results: int = 3) -> Dict[str, Any]:
    """
    جستجوی معنایی در ChromaDB بر اساس متن سوال کاربر
    """
    collection = get_chroma_collection()
    
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )
    return results
