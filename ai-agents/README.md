# AI Agents — Curated Repository Library

20 open-source repositories for learning and building AI agents, organised by
layer of the agent stack. Each one is a **git submodule** pinned to the upstream
commit it had on 2026-11-12, so this repo stays small and each project keeps
its own history.

## Get the code

```bash
./scripts/fetch-ai-agents.sh                        # everything (several GB)
./scripts/fetch-ai-agents.sh 03-memory-knowledge    # one category
./scripts/fetch-ai-agents.sh 01-agent-frameworks/langgraph   # one repo
./scripts/fetch-ai-agents.sh --update               # move all to latest upstream
```

Fetches are shallow (`--depth 1`), so you get current source without full history.

## How the layers fit together

```
            ┌──────────────────────────────────────────────┐
  Apps      │ 04 Autonomous agents: OpenHands, Browser Use │
            ├──────────────────────────────────────────────┤
  Orchestr. │ 01 Frameworks: LangGraph, CrewAI, ADK, ...   │
            │ 02 Visual / workflow: Flowise, Dify, n8n     │
            ├──────────────────────────────────────────────┤
  State     │ 03 Memory & knowledge: LlamaIndex, Mem0,     │
            │    Graphiti, Cognee                          │
            ├──────────────────────────────────────────────┤
  Tools     │ MCP servers (standard tool interface)        │
            └──────────────────────────────────────────────┘
```

An agent is a loop: at step *t* the policy (the LLM) maps state to an action,
the environment (tools) returns an observation, and memory updates the state:

$$a_t = \pi_\theta(s_t),\qquad o_t = \mathrm{Env}(a_t),\qquad s_{t+1} = M(s_t, a_t, o_t)$$

Frameworks (01/02) implement the loop and the control flow around π, MCP
standardises `Env`, and memory systems (03) implement `M` beyond the context window.

---

## 01 · Agent Frameworks

| Repo | What it's for | Path |
|---|---|---|
| [LangGraph](https://github.com/langchain-ai/langgraph) | Stateful, multi-step agents as graphs with checkpoints | `01-agent-frameworks/langgraph` |
| [CrewAI](https://github.com/crewAIInc/crewAI) | Role-based collaborative multi-agent teams | `01-agent-frameworks/crewai` |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | Agents with tools, handoffs and guardrails | `01-agent-frameworks/openai-agents-sdk` |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | Enterprise agents (.NET + Python), successor to AutoGen/Semantic Kernel | `01-agent-frameworks/microsoft-agent-framework` |
| [Google ADK](https://github.com/google/adk-python) | Build, evaluate and orchestrate agents | `01-agent-frameworks/google-adk` |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | Type-safe agents with validated structured outputs | `01-agent-frameworks/pydantic-ai` |
| [Agno](https://github.com/agno-agi/agno) | Multimodal agent applications and runtime | `01-agent-frameworks/agno` |
| [smolagents](https://github.com/huggingface/smolagents) | Lightweight agents that act by writing code | `01-agent-frameworks/smolagents` |

## 02 · Agent Workflows & Integrations

| Repo | What it's for | Path |
|---|---|---|
| [Flowise](https://github.com/FlowiseAI/Flowise) | Visual drag-and-drop LLM workflow builder | `02-workflows-integrations/flowise` |
| [Dify](https://github.com/langgenius/dify) | Production LLM app platform (RAG, agents, ops) | `02-workflows-integrations/dify` |
| [n8n](https://github.com/n8n-io/n8n) | Workflow automation with AI nodes and 400+ integrations | `02-workflows-integrations/n8n` |
| [MCP Reference Servers](https://github.com/modelcontextprotocol/servers) | Reference Model Context Protocol tool servers | `02-workflows-integrations/mcp-servers` |

## 03 · Memory & Knowledge

| Repo | What it's for | Path |
|---|---|---|
| [LlamaIndex](https://github.com/run-llama/llama_index) | Connect agents to external data (indexing, RAG) | `03-memory-knowledge/llamaindex` |
| [Mem0](https://github.com/mem0ai/mem0) | Persistent long-term memory layer for agents | `03-memory-knowledge/mem0` |
| [Graphiti](https://github.com/getzep/graphiti) | Temporal knowledge graphs (facts with validity time) | `03-memory-knowledge/graphiti` |
| [Cognee](https://github.com/topoteretes/cognee) | AI memory via knowledge-graph + vector pipelines | `03-memory-knowledge/cognee` |

## 04 · Autonomous Agents & Learning

| Repo | What it's for | Path |
|---|---|---|
| [OpenHands](https://github.com/OpenHands/OpenHands) | Autonomous software-engineering agents | `04-autonomous-agents-learning/openhands` |
| [Browser Use](https://github.com/browser-use/browser-use) | Agents that operate a web browser | `04-autonomous-agents-learning/browser-use` |
| [AI Agents for Beginners](https://github.com/microsoft/ai-agents-for-beginners) | Microsoft's lesson-by-lesson agent course | `04-autonomous-agents-learning/ai-agents-for-beginners` |
| [Awesome LLM Apps](https://github.com/Shubhamsaboo/awesome-llm-apps) | Catalogue of runnable LLM / agent apps | `04-autonomous-agents-learning/awesome-llm-apps` |

---

## Suggested learning path

1. **AI Agents for Beginners** — concepts and vocabulary.
2. **smolagents** — the whole agent loop in a small codebase; read it end to end.
3. **LangGraph** or **Pydantic AI** — explicit state and typed outputs.
4. **MCP servers** — how tools are exposed to any agent.
5. **Mem0 / Graphiti** — add memory that survives across sessions.
6. **OpenHands / Browser Use** — study a full autonomous agent in production.
7. Pick one problem from **Awesome LLM Apps** and build it for real.
