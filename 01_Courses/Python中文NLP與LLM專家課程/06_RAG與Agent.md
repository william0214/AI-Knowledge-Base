---
title: "RAG 知識擴增與 AI Agents"
date: 2026-03-12
day: Day4
tags: [RAG, Agent, LLM, LangChain, Day4]
status: in-progress
chapter: "§11"
---

# 06 — RAG 知識擴增與 AI Agents

> tags: #RAG #Agent #LLM #LangChain #Day4 #in-progress
> 對應課程章節：§11 延伸大型語言模型知識擴增 (RAG) 與 AI Agents 應用
> 原始講義：[PNLP上課筆記_2026-03-09.pdf](assets/PNLP上課筆記_2026-03-09.pdf)
> 主要來源頁碼：54–60, 68–76, 79–90, 103–110

---

## 6.1 RAG 的核心流程與企業用途

### 💡 思考
- RAG 真正解決的是知識缺口，還是回答可驗證性問題？
- 文件切塊、向量化、檢索、生成四個步驟裡，哪一步最容易出錯？

### 📌 重點
- 課堂中的 RAG 核心流程包括：
  - 文件切割
  - Embedding
  - 向量索引
  - 相似度檢索
  - 內容拼接後交給 LLM 生成
- RAG 的主要用途是讓模型回答建立在企業文件、知識庫與最新資料之上。
- 這也是課程後段企業知識管理與客服應用的基礎架構。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 54-60 頁
# 用途：基本 RAG Pipeline 骨架

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_openai import OpenAIEmbeddings
# from langchain_community.vectorstores import FAISS
# from langchain.chains import RetrievalQA
```

### 📚 延伸
- [LangChain RAG](https://python.langchain.com/docs/tutorials/rag/)
- [RAG 論文](https://arxiv.org/abs/2005.11401)

---

## 6.2 Prompt Engineering 與 RAG 回答品質

### 💡 思考
- Prompt 不佳時，RAG 為什麼仍然可能答非所問？
- 防止 prompt injection 時，系統提示與資料來源控制誰更重要？

### 📌 重點
- 課堂把 Prompt Engineering 視為 RAG 成敗的重要一層。
- 需要明確區分：
  - system role 的行為約束
  - user query 的任務意圖
  - retrieved context 的可引用內容
- RAG 不只是檢索，還包含如何讓模型正確使用檢索結果。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 58-60 頁
# 用途：RAG Prompt 模板示意

# from langchain_core.prompts import ChatPromptTemplate

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你只能根據提供的知識內容回答，若資料不足請明說。"),
#     ("human", "問題：{question}\n\n參考資料：{context}"),
# ])
```

### 📚 延伸
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)

---

## 6.3 LangChain、LlamaIndex 與 LangGraph 的分工

### 💡 思考
- LangChain 與 LlamaIndex 最大差異是 workflow orchestration 還是 data interface？
- LangGraph 在課堂脈絡裡，是為了多步驟流程控制還是多 Agent？

### 📌 重點
- LangChain：偏流程編排、工具整合、Agent 與 chain 組裝。
- LlamaIndex：偏資料索引、Retriever、Query Engine 與知識存取。
- LangGraph：補上較可控的狀態流與節點式任務編排。
- 課堂安排顯示三者不是互斥，而是可依系統層次組合使用。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 68-76, 103-106 頁
# 用途：框架角色對照

framework_roles = {
    "LangChain": ["chains", "agents", "tools", "workflow orchestration"],
    "LlamaIndex": ["index", "retriever", "query engine", "data connectors"],
    "LangGraph": ["state graph", "multi-step control", "agent workflow"],
}
```

### 📚 延伸
- [LangChain](https://python.langchain.com/)
- [LlamaIndex](https://docs.llamaindex.ai/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

---

## 6.4 AI Agent、Tools 與 MCP

### 💡 思考
- 課堂中的 Agent 是聊天機器人升級版，還是能執行任務的工作流節點？
- MCP 在這條技術線上扮演的是什麼角色？

### 📌 重點
- 課堂後段已經從單輪問答擴展到 Agentic Workflow。
- Agent 的核心不是多說話，而是：
  - 理解任務
  - 選工具
  - 呼叫外部能力
  - 維持中間狀態
- MCP 被納入課綱，代表老師已把模型與工具之間的標準介面視為企業落地能力之一。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 79-90, 108-110 頁
# 用途：Agent 元件摘要

agent_components = [
    "planning",
    "tool use",
    "memory",
    "state management",
    "external system integration",
]
```

### 📚 延伸
- [Model Context Protocol](https://modelcontextprotocol.io/)
- [AutoGen](https://microsoft.github.io/autogen/)

---

## 6.5 幻覺控制、Grounding 與引用

### 💡 思考
- 為什麼加了 RAG 仍然可能有 hallucination？
- Grounding、citation、self-check 之間該如何分工？

### 📌 重點
- 課堂把 RAG 與 hallucination 控制綁在一起看待。
- 常見控制方式：
  - 僅根據檢索內容作答
  - 要求引用來源
  - 在資料不足時明確拒答
  - 針對回覆做自我一致性檢查
- 這些做法比單純調 prompt 更接近可審核的企業系統。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 58-60, 79-80 頁
# 用途：回答守則

answer_policy = {
    "must_ground_in_context": True,
    "must_cite_source": True,
    "allow_refusal_when_context_missing": True,
}
```

### 📚 延伸
- [Survey of Hallucination in NLG](https://arxiv.org/abs/2202.03629)

---

## 6.6 GGUF、地端 SLM 與離線知識應用

### 💡 思考
- GGUF 在企業私有化路線裡，最重要的價值是成本、隱私，還是可部署性？
- 什麼情況下 CPU 可接受，什麼情況一定要 GPU？

### 📌 重點
- 課堂把 GGUF、LM Studio、私有化部署放在同一條脈絡上。
- GGUF 適合量化後的本地推理與快速測試。
- 這條路線特別適合：
  - 離線環境
  - 敏感資料場景
  - 小型部門知識助手

### 🔧 實作
```python
# 來源：課程講義 PDF 第 86-90, 107-110 頁
# 用途：地端 GGUF 載入示意

# from llama_cpp import Llama

# llm = Llama(model_path="./model.gguf", n_ctx=2048)
# output = llm("請說明 RAG 的用途", max_tokens=256)
```

### 📚 延伸
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [Ollama](https://ollama.com/)

---

## 6.7 圖表補述：RAG、LangGraph 與 MCP 流程圖

### 💡 思考
- 這幾張圖共同強調的是模型能力，還是系統接線方式？
- 哪些箭頭代表資料流，哪些箭頭代表控制流？

### 📌 重點
- RAG 圖的核心流程可還原為：
  - `文件資料夾` -> `文件切割` -> `Embedding` -> `向量索引`
  - `使用者問題` -> `Retriever` -> `相關 chunks` -> `Gemini / LLM` -> `答案`
- LangGraph Agent 圖的核心流程可還原為：
  - `使用者請求` -> `route_tools` -> `順序節點或並行節點` -> `BasicToolNode` -> `LLM 決策` -> `最終回答`
- MCP 圖的核心流程可還原為：
  - `FastMCP Server` 提供 `get_time` / `get_date_info`
  - `LM Studio` 讀取 `mcp.json` 註冊 `MyTimeServer`
  - `聊天輸入` -> `@MyTimeServer.get_time()` -> `MCP Server` -> `時間字串`

### 🔧 實作
```python
# 來源：課程講義 PDF 第 56-58, 86, 105-109 頁
# 用途：保存圖表中的核心流程節點

rag_flow = [
    "documents",
    "chunking",
    "embedding",
    "vector_index",
    "retrieval",
    "llm_generation",
]

langgraph_flow = [
    "user_request",
    "route_tools",
    "sequential_or_parallel_nodes",
    "tool_execution",
    "llm_decision",
    "final_response",
]

mcp_flow = [
    "mcp_server",
    "mcp_client_or_lm_studio",
    "tool_call",
    "tool_result",
]
```

### 📚 延伸
- [06_RAG與Agent](06_RAG與Agent.md)
- [rag_agent_mcp_flows.md](diagrams/rag_agent_mcp_flows.md)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：05_情感分析](05_情感分析.md) | [下一篇：07_LLM微調 →](07_LLM微調.md)
