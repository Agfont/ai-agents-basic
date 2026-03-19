#!/usr/bin/env python3
"""
🔍 Task 4: Semantic Search Implementation
Build a complete semantic search system that understands meaning!
"""

import os
import tempfile
from contextlib import nullcontext
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv
from tee_loger import setup_log

load_dotenv()
setup_log("markers/task4_log.txt")

def build_search_engine():
    print("🔍 Task 4: Semantic Search Implementation")
    print("=" * 55)

    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )

    # TechDocs complete knowledge base
    knowledge_base = [
        "Remote work policy allows employees to work from home up to 3 days per week with manager approval.",
        "Dress code is business casual Monday-Thursday. Jeans are permitted on Fridays only.",
        "Annual performance reviews happen in December with mid-year check-ins in June.",
        "Health insurance covers employee and dependents with company paying 80% of premiums.",
        "401k retirement plan includes company match up to 6% of salary.",
        "Vacation policy provides 15 days PTO first year, increasing to 20 days after 2 years.",
        "Sick leave is separate from vacation with 10 days allocated annually.",
        "Training budget of $2000 per employee for professional development courses.",
        "Office provides free lunch on Tuesdays and Thursdays for all employees.",
        "Parking is free for all employees in the company garage.",
        "Work hours are flexible but core hours 10 AM to 3 PM are required.",
        "Security policy requires password changes every 90 days and two-factor authentication."
    ]

    # Convert to documents
    documents = [Document(page_content=text, metadata={"id": i})
                 for i, text in enumerate(knowledge_base)]

    print(f"📚 Loading {len(documents)} documents into vector store...")

    chroma_host = os.getenv("CHROMA_HOST")
    chroma_port = int(os.getenv("CHROMA_PORT", "8000"))
    context = nullcontext(None)
    create_kwargs = {
        "documents": documents,
        "embedding": embeddings,
    }

    if chroma_host:
        print(f"🌐 Using Chroma server at {chroma_host}:{chroma_port}")
        create_kwargs["client"] = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        create_kwargs["collection_name"] = "techdocs_search"
    else:
        context = tempfile.TemporaryDirectory()

    with context as temp_dir:
        if temp_dir is not None:
            create_kwargs["persist_directory"] = temp_dir

        vectorstore = Chroma.from_documents(**create_kwargs)
        print("✅ Vector store ready!\n")

        # TODO 1: Set search query
        # Replace ___ with: "work from home policy"
        search_query = "work from home policy"

        # TODO 2: Set number of results
        # Replace ___ with: 3
        k = 3

        print(f"🔎 Searching for: '{search_query}'")
        print(f"   Returning top {k} results")
        print("-" * 40)

        # Basic similarity search
        results = vectorstore.similarity_search(search_query, k=k)

        print("\n📊 Search Results:")
        for i, doc in enumerate(results, 1):
            print(f"\n{i}. {doc.page_content}")

        # TODO 3: Similarity search with scores
        # Replace ___ with: 0.5
        score_threshold = 0.5

        print(f"\n🎯 Filtered Search (threshold > {score_threshold}):")
        print("-" * 40)

        results_with_scores = vectorstore.similarity_search_with_score(
            search_query,
            k=5
        )

        relevant_results = [(doc, score) for doc, score in results_with_scores
                           if score >= score_threshold]

        if relevant_results:
            for doc, score in relevant_results[:3]:
                print(f"\n📄 Score: {score:.3f}")
                print(f"   {doc.page_content[:100]}...")
        else:
            print("No results above threshold")

        # Advanced search demonstrations
        print("\n✨ Semantic Magic Examples:")
        print("-" * 40)

        test_searches = [
            ("Can I bring my dog to work?", "dress code"),  # Should find dress code
            ("How many days off do I get?", "vacation"),     # Should find vacation
            ("retirement savings", "401k")                   # Should find 401k
        ]

        for query, expected_topic in test_searches:
            results = vectorstore.similarity_search(query, k=1)
            found_topic = expected_topic.lower() in results[0].page_content.lower()
            status = "✅" if found_topic else "❌"
            print(f"{status} '{query}' → Found: {expected_topic}")

    # Key achievements
    print("\n🏆 What You've Achieved:")
    print("-" * 40)
    print("• Built a semantic search engine")
    print("• Search understands MEANING not keywords")
    print("• 'work from home' finds 'remote work policy'")
    print("• Ready for production deployment!")

    # Create completion marker
    os.makedirs("markers", exist_ok=True)
    with open("markers/task4_search_complete.txt", "w") as f:
        f.write("COMPLETED")

    print("\n✅ Task 4 completed! Semantic search mastered!")
    print("🎉 You've completed the Vector Databases lab!")

if __name__ == "__main__":
    build_search_engine()