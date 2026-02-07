# 🚀 RAG Lab: From Search to Answers

## Transform Your Semantic Search into an AI Q&A System

Welcome to the RAG (Retrieval-Augmented Generation) Lab! You've mastered semantic search in the Vector Databases Lab - now it's time to add AI generation to create a complete question-answering system.

## 🎯 Lab Objective

**Your Mission:** Build a production-ready RAG system that doesn't just find relevant documents, but generates accurate, context-aware answers from them.

**The Challenge:** Your CEO wants the system to answer "Yes, you can work 3 days from home" instead of just showing the remote work policy document.

## 📚 Prerequisites

Before starting this lab, you should have completed:
- ✅ **Vector Databases Lab** - Understanding embeddings, ChromaDB, and semantic search
- ✅ Familiarity with Python and basic NLP concepts
- ✅ Understanding of vector similarity and document chunking

## 🏗️ What You'll Build

A complete RAG pipeline that:
1. **Retrieves** relevant document chunks using semantic search (95% accuracy)
2. **Augments** prompts with retrieved context
3. **Generates** accurate answers using LLM (gpt-4.1-nano)
4. **Cites** sources for transparency

## 📋 Lab Structure

### Task 1: Vector Store Setup 🔧
**File:** `task_1_setup_vectorstore.py`
- Initialize ChromaDB client with persistent storage
- Create collection for TechCorp documents
- Set up embedding model (all-MiniLM-L6-v2)
- **TODOs:** 3 simple completions to bridge your Vector Databases Lab knowledge

### Task 2: Document Processing 📄
**File:** `task_2_document_processing.py`
- Implement smart paragraph-based chunking
- Add 20% overlap for context preservation
- Store documents with metadata (source, section)
- **TODOs:** 3 completions for chunking logic and metadata

### Task 3: LLM Integration 🤖
**File:** `task_3_llm_integration.py`
- Configure LangChain ChatOpenAI client
- Set temperature (0.3) for focused answers
- Configure max tokens (500) for concise responses
- **TODOs:** 3 completions for LLM configuration

### Task 4: Prompt Engineering 📝
**File:** `task_4_prompt_engineering.py`
- Create system prompt for context-aware answers
- Build user prompt with retrieved chunks
- Format prompts for optimal generation
- **TODOs:** 3 completions for prompt templates

### Task 5: Complete RAG Pipeline 🚀
**File:** `task_5_complete_rag.py`
- Wire together all components
- Implement the complete RAG flow
- Add source citations to answers
- **TODOs:** 5 completions to connect everything

## 🔑 Key Concepts

### RAG Architecture
```
User Question → Embedding → Vector Search → Retrieve Chunks
                                              ↓
                                         Augment Prompt
                                              ↓
                                         Generate Answer
                                              ↓
                                         Add Citations
                                              ↓
                                         Final Response
```

### Why RAG?
- **Accuracy:** Answers based on actual documents, not general knowledge
- **Transparency:** Source citations for every answer
- **Control:** Responses limited to your document collection
- **Scalability:** Add new documents without retraining

## 🚦 Getting Started

### 1. Environment Setup
```bash
# Activate virtual environment
source venv/bin/activate

# Verify environment
python3 verify_environment.py
```

### 2. Required Packages
- `chromadb` - Vector database
- `sentence-transformers` - Embeddings
- `langchain` - RAG framework
- `langchain-openai` - LLM integration
- `numpy` - Vector operations

### 3. Environment Variables
```bash
export OPENAI_API_BASE="http://localhost:8080/v1"
export OPENAI_API_KEY="dummy-key-for-proxy"
```

## 📂 Document Collection

Your TechCorp documents are in `techcorp-docs/`:
- **policies/** - Company policies and guidelines
- **products/** - Product specifications
- **support/** - Support documentation

## 🏃 Running the Lab

Execute tasks in order:
```bash
# Task 1: Setup
python3 task_1_setup_vectorstore.py

# Task 2: Process Documents
python3 task_2_document_processing.py

# Task 3: Configure LLM
python3 task_3_llm_integration.py

# Task 4: Design Prompts
python3 task_4_prompt_engineering.py

# Task 5: Complete Pipeline
python3 task_5_complete_rag.py
```

## ✅ Success Criteria

Each task creates a marker file in `markers/`:
- `task1_setup_complete.txt`
- `task2_processing_complete.txt`
- `task3_llm_complete.txt`
- `task4_prompt_complete.txt`
- `task5_rag_complete.txt`

## 🎯 Expected Outcomes

By completing this lab, you'll have:
1. **Working RAG System** - Complete Q&A pipeline
2. **95% Accuracy** - Semantic search finding the right documents
3. **Context-Aware Answers** - LLM generating from retrieved content
4. **Source Attribution** - Every answer cites its sources
5. **Production-Ready Code** - Scalable, maintainable architecture

## 💡 Tips for Success

1. **Read the TODOs carefully** - Each has a clear hint
2. **Check line numbers** - They guide you to the exact location
3. **Test incrementally** - Run each task before moving on
4. **Review output** - Understand what each component does
5. **Use the hints** - They show exactly what to fill in

## 🆘 Troubleshooting

### Common Issues:
- **Import Error:** Run `pip install` commands from environment setup
- **API Error:** Check OPENAI_API_BASE and OPENAI_API_KEY are set
- **No documents found:** Run Task 2 to process documents first
- **Empty collection:** Ensure Task 1 completed successfully

## 🏆 Challenge Extensions

Once you complete the lab, try:
- Adding more document types
- Implementing different chunking strategies
- Testing with complex multi-hop questions
- Adding a confidence score to answers
- Building a web interface

## 📖 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Guide](https://docs.trychroma.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [RAG Best Practices](https://www.pinecone.io/learn/retrieval-augmented-generation/)

## 🎉 Congratulations!

You're building the same technology that powers ChatGPT, Claude, and enterprise AI assistants! This RAG system transforms static documents into an intelligent Q&A system.

**Remember:** You're not just finding documents anymore - you're generating intelligent answers! 🚀