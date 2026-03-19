#!/usr/bin/env python3
"""
🗄️ Task 3: Build Vector Store with ChromaDB
Create a production-ready vector database using LangChain and ChromaDB.
"""

import os
import tempfile
from contextlib import nullcontext
from typing import List
from dotenv import load_dotenv
from tee_loger import setup_log
import chromadb

load_dotenv()
setup_log("markers/task3_log.txt")

# TODO 1: Import Chroma vector store
# Replace ___ with: Chroma
from langchain_community.vectorstores import Chroma

# TODO 2: Import HuggingFace embeddings
# Replace ___ with: HuggingFaceEmbeddings
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def main():
    print("🗄️ Task 3: Building Vector Store with ChromaDB")
    print("=" * 55)

    # TODO 3: Initialize embeddings
    # Replace ___ with: "all-MiniLM-L6-v2"
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    print("✅ Embedding model loaded")

    # Sample TechDocs documents
    documents_text = [
        """Remote Work Policy: Employees can work from home up to 3 days per week.
        VPN access required. Core hours 10 AM - 3 PM local time. Manager approval needed.""",

        """Office Benefits: Free lunch on Tuesdays and Thursdays. Gym membership reimbursement
        up to $50/month. Annual learning budget of $2000 for courses and conferences.""",

        """Vacation Policy: 15 days PTO for first year, 20 days after 2 years.
        Sick leave separate - 10 days per year. Holidays follow local calendar.""",

        """Security Guidelines: Two-factor authentication required for all accounts.
        Password changes every 90 days. No sharing of credentials. Report incidents immediately.""",

        """Dress Code: Business casual Monday-Thursday. Casual Fridays allow jeans.
        Client meetings require business formal. Work from home has no dress requirements."""
    ]

    # Convert to Document objects with metadata
    documents = []
    for i, text in enumerate(documents_text):
        doc = Document(
            page_content=text,
            metadata={
                "source": f"handbook_section_{i+1}",
                "type": "policy",
                "id": i
            }
        )
        documents.append(doc)

    print(f"📚 Processing {len(documents)} documents...")

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=50
    )
    splits = text_splitter.split_documents(documents)
    print(f"✂️ Created {len(splits)} chunks")

    # Create vector store
    print("\n🔨 Building ChromaDB vector store...")

    chroma_host = os.getenv("CHROMA_HOST")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    context = nullcontext(None)
    create_kwargs = {
        "documents": splits,
        "embedding": embeddings,
        "collection_name": "techdocs",
    }

    if chroma_host:
        print(f"🌐 Using Chroma server at {chroma_host}:{chroma_port}")
        create_kwargs["client"] = chromadb.HttpClient(host=chroma_host, port=chroma_port)
    else:
        context = tempfile.TemporaryDirectory()

    with context as temp_dir:
        if temp_dir is not None:
            create_kwargs["persist_directory"] = temp_dir

        vectorstore = Chroma.from_documents(**create_kwargs)
        print(f"✅ Vector store created with {vectorstore._collection.count()} vectors")

        print("\n🔍 Testing Vector Store:")
        print("-" * 40)

        test_queries = [
            "Can I work from home?",
            "What's the dress code for Friday?",
            "How many vacation days do I get?"
        ]

        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            results = vectorstore.similarity_search(query, k=1)
            if results:
                print(f"✨ Best match: {results[0].page_content[:100]}...")
                print(f"   Source: {results[0].metadata.get('source', 'unknown')}")

    # Key insights
    print("\n💡 What We Built:")
    print("-" * 40)
    print("• Production-ready vector database")
    print("• Semantic search capability")
    print("• Metadata for filtering")
    print("• Persistent storage support")
    print("• Ready for RAG applications!")

    # Create completion marker
    os.makedirs("markers", exist_ok=True)
    with open("markers/task3_vectorstore_complete.txt", "w") as f:
        f.write("COMPLETED")

    print("\n✅ Task 3 completed! Vector store built successfully.")

if __name__ == "__main__":
    main()