# Copilot Instructions for AI Agent Basics

## Project Overview
**ai-agent-basics** is a progressive learning codebase structured as 7 interconnected labs that build AI/ML competency from raw API calls to advanced agent orchestration. This is an **educational repository** where each task is intentionally small to guide learners step-by-step.

### Architecture: Progressive Learning Stack
```
Lab 1: Raw OpenAI API → Lab 2: LangChain Abstraction → Lab 3: Prompt Engineering
                                    ↓                         ↓
                            Lab 4: Vector Databases    Lab 5: RAG Pipeline
                                    ↓                         ↓
                            Lab 6: LangGraph Workflows → Lab 7: MCP Tool Integration
```

## Critical Concepts for AI Agents

### 1. Task Structure & Learning Design
**Each module uses a consistent pattern:**
- `verify_environment.py` - Pre-flight checks (MUST run first, creates `markers/environment_verified.txt`)
- `task_N_*.py` - Progressive micro-tasks with explicit `TODO` comments marking exact lines to complete
- `tee_loger.py` - Output duplication to both stdout and `markers/task_N_log.txt`
- `markers/` directory - Completion tracking files (one per task)

**Pattern Recognition:**
- Tasks are intentionally small (1-3 lines per TODO) to build confidence
- State accumulates: later tasks depend on earlier ones completing
- Each file has detailed ASCII diagrams explaining data flow (see Task 3 examples in `6-langgraph/`)

### 2. Environment Setup (Critical!)
**The project requires `.env` file with:**
```
OPENAI_API_KEY=sk-...
OPENAI_API_BASE=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-nano
```

**Virtual environment must be activated** - all pip packages (openai, langchain, mcp) are in `.venv/`, and `verify_environment.py` explicitly checks this and provides remediation steps.

### 3. Module-Specific Patterns

#### Lab 1: Raw OpenAI API (Foundational)
- **Key import pattern:** `from openai import OpenAI`
- **Response access:** `response.choices[0].message.content` (nested structure)
- **Token usage:** Always available in `response.usage.{prompt,completion,total}_tokens`
- **Common mistake:** Accessing response without checking `response.choices` length

#### Lab 2: LangChain (Abstraction Layer)
- **Provider abstraction:** `ChatOpenAI`, `ChatGoogleGenerativeAI`, `ChatXAI` all share same interface
- **Response simplification:** `response.content` (not nested) - handles provider differences
- **Output parsers:** `StrOutputParser()`, `CommaSeparatedListOutputParser()` transform raw responses
- **Chains:** Use pipe operator `|` to compose: `prompt | model | parser`

#### Lab 3: Prompt Engineering
- **Progression:** Zero-shot → One-shot → Few-shot → Chain-of-thought
- **Pattern:** Each approach is a different prompt structure, same API underneath
- **Key insight:** Better prompts = better outputs without changing model

#### Lab 4: Vector Databases
- **Embeddings flow:** Documents → Split → Embed (OpenAI) → Store → Query
- **Key file:** `requirements.txt` specifies vector DB library (e.g., FAISS, Chroma)
- **Common pattern:** Process once, persist, reuse embeddings

#### Lab 5: RAG (Retrieval Augmented Generation)
- **Architecture:** Retriever + Prompt Template + LLM (3-step pipeline)
- **Data flow:** Query → Retrieve docs → Inject into prompt → LLM generates answer
- **Files built incrementally:** Tasks add components, final task connects all

#### Lab 6: LangGraph (Stateful Workflows)
- **Core abstraction:** `StateGraph(State)` where State is `TypedDict` with fields
- **Node pattern:** Functions take `state` dict, return PARTIAL updates (only changed fields)
- **Execution:** State flows through graph, accumulated at each node
- **Graph lifecycle:** `add_node()` → `add_edge()` → `set_entry_point()` → `compile()` → `invoke()`
- **Key insight:** State is immutable within nodes, updates are additive

#### Lab 7: MCP (Tool Integration)
- **Server pattern:** `FastMCP(name)` + `@mcp.tool()` decorated functions
- **Tool schema:** Functions automatically become MCP tools with input parameters
- **Naming convention:** Tools bound to LLM become `mcp__<server>__<tool_name>`
- **Files:** Standalone `mcp_servers/` directory with `calculator_server.py` and `weather_server.py`
- **Integration:** MCP tools bind to LLM via `llm.bind_tools([tools])`, then router decides which to call

### 4. Common Workflows & Commands

**Verifying setup (run first in each module):**
```bash
cd <module-directory>
python verify_environment.py
```

**Running a task:**
```bash
python task_N_*.py  # Will log to markers/task_N_log.txt AND stdout (via Tee)
```

**Checking completion:**
```bash
ls markers/  # Look for task_N_complete.txt files
```

**Debugging imports:**
- All imports use absolute paths (e.g., `from tee_loger import setup_log`)
- Each module is self-contained; don't import across module boundaries
- LangChain variants use provider-specific imports: `from langchain_openai import ChatOpenAI`

### 5. Data Flow Patterns to Understand

**Simple Chain (Lab 2):**
```
PromptTemplate → LLM → OutputParser → structured output
```

**Graph Execution (Lab 6):**
```
Initial State → Node1 (transform) → Node2 (transform) → END
                 ↑ state                ↑ state updates
             accumulates            accumulates
```

**MCP Integration (Lab 7):**
```
User Query → LLM + MCP Tools → Router → Select Tool → Execute → Return to LLM
                              (intelligent routing decides which tool)
```

### 6. File Reference Guide

| File | Purpose |
|------|---------|
| `verify_environment.py` | Environment validation (creates `markers/environment_verified.txt`) |
| `tee_loger.py` | Dual output to stdout + log file |
| `task_N_*.py` | Actual learning task with TODOs |
| `markers/task_N_complete.txt` | Completion marker (created by task) |
| `markers/task_N_log.txt` | Tee'd output log |
| `mcp_servers/*.py` | Standalone MCP server implementations |

### 7. Key Conventions & Gotchas

1. **Virtual Environment:** CRITICAL. `verify_environment.py` explicitly checks and warns if not active
2. **Marker Files:** Check for task completion via `markers/` existence, not function success
3. **Tee Logger:** All stdout automatically duals to log file; don't manually create logs
4. **State Updates:** In LangGraph, nodes return PARTIAL state updates, not full state
5. **MCP Tool Names:** Generated as `mcp__<server>__<function_name>`, affects router logic
6. **Error Handling:** Most tasks have basic error checks; focus on completion markers
7. **API Keys:** `.env` values are read via `load_dotenv()` before any API calls

## When Assisting Users

- **For Task Help:** Reference the specific line numbers from TODO comments and explain the conceptual pattern
- **For Debugging:** First verify `verify_environment.py` passes; check `.env` and virtual environment
- **For Architecture:** Explain data flow using the diagrams embedded in task files
- **For Extensions:** Suggest adding to the appropriate module (don't create new modules without context)

## References
- Each module's `README.md` contains detailed learning objectives and concept explanations
- Task files have ASCII diagrams showing data flow (see `task_3_connecting_edges.py` for examples)
- Use `markers/` directory to understand completion status across the learning journey
