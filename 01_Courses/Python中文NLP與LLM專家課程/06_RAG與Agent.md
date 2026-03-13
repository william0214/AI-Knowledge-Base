---
title: "RAG 知識擴增與 AI Agents"
date: 2026-03-12
day: Day4
tags: [RAG, Agent, LLM, LangChain, Day4]
status: todo
chapter: "§11"
---

# 06 — RAG 知識擴增與 AI Agents

> tags: #RAG #Agent #LLM #LangChain #Day4 #todo
> 對應課程章節：§11 延伸大型語言模型知識擴增 (RAG) 與 AI Agents 應用

---

## 6.1 RAG (Retrieval-Augmented Generation) 核心概念

### 💡 思考
- RAG 如何解決 LLM 的知識過時與幻覺問題？
- RAG 的 Retrieval 和 Generation 兩個階段各自的挑戰？
- Naive RAG vs Advanced RAG vs Modular RAG 的演進？

### 📌 重點
- RAG 架構：
  - 文件切割 (Chunking)
  - Embedding & 向量索引
  - 相似度檢索 (Similarity Search)
  - 上下文組合 & LLM 生成
- 

### 🔧 實作
```python
# 來源：
# 用途：基本 RAG Pipeline

# from langchain.document_loaders import TextLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.embeddings import OpenAIEmbeddings
# from langchain.vectorstores import FAISS
# from langchain.chains import RetrievalQA

```

### 📚 延伸
- [LangChain RAG 教學](https://python.langchain.com/docs/use_cases/question_answering/)
- [RAG 論文](https://arxiv.org/abs/2005.11401)

---

## 6.2 提示詞工程 (Prompt Engineering)

### 💡 思考
- System Prompt vs User Prompt 的設計原則？
- Few-shot Prompt 在中文 NLP 任務的最佳實踐？
- 如何設計 Prompt 來防止 Prompt Injection？

### 📌 重點
- Prompt 設計原則：
- LangChain PromptTemplate：
- LlamaIndex Query Engine：
- 

### 🔧 實作
```python
# 來源：
# 用途：LangChain Prompt 設計

# from langchain.prompts import ChatPromptTemplate

# prompt = ChatPromptTemplate.from_messages([
#     ("system", "你是一個專業的中文客服助手。根據以下資料回答問題：{context}"),
#     ("human", "{question}")
# ])
```

### 📚 延伸
- [OpenAI Prompt Engineering Guide](https://platform.openai.com/docs/guides/prompt-engineering)
- [LangChain Prompts](https://python.langchain.com/docs/modules/model_io/prompts/)

---

## 6.3 LangChain 與 LlamaIndex 整合

### 💡 思考
- LangChain 和 LlamaIndex 各自的定位與差異？
- 什麼場景下應該選擇 LangChain？什麼場景選 LlamaIndex？
- 如何將兩者整合使用？

### 📌 重點
- LangChain 核心概念：Chain / Agent / Memory / Tool
- LlamaIndex 核心概念：Index / Query Engine / Retriever
- LangGraph：
- 向量資料庫選型：

| 向量 DB | 特點 | 適用場景 |
|---|---|---|

### 🔧 實作
```python
# 來源：
# 用途：LangChain + LlamaIndex 整合

```

### 📚 延伸
- [LangChain 官方文件](https://python.langchain.com/)
- [LlamaIndex 官方文件](https://docs.llamaindex.ai/)
- [LangGraph](https://langchain-ai.github.io/langgraph/)

---

## 6.4 AI Agents 在 NLP 領域的應用

### 💡 思考
- AI Agent 的核心組成：Planning、Memory、Tools、Action？
- Agentic Workflow 如何實現動態任務分配？
- 多 Agent 協作 (Multi-Agent) 的架構模式？

### 📌 重點
- AI Agent 架構：
- 工具調用 (Tool Use)：
- Agentic Workflow：
- 

### 🔧 實作
```python
# 來源：
# 用途：LangChain Agent 建構

# from langchain.agents import AgentExecutor, create_openai_tools_agent

```

### 📚 延伸
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [AutoGen](https://microsoft.github.io/autogen/)

---

## 6.5 防止 AI 幻覺 (Hallucination) — 事實查核技術

### 💡 思考
- LLM 為什麼會產生幻覺？有哪幾種類型的幻覺？
- Grounding 技術如何降低幻覺風險？
- 如何設計評估指標來衡量幻覺程度？

### 📌 重點
- 幻覺類型：事實性 / 一致性 / 編造
- 防護策略：
  - RAG Grounding
  - Self-consistency checking
  - Citation / 引用標注
- 

### 🔧 實作
```python
# 來源：
# 用途：幻覺偵測 / 事實查核

```

### 📚 延伸
- [Survey of Hallucination in NLG](https://arxiv.org/abs/2202.03629)

---

## 6.6 地端 SLM 部署 (GGUF)

### 💡 思考
- GGUF 格式相比原始模型的優勢？
- CPU 推理 vs GPU 推理的效能差異？
- 什麼規模的模型適合在個人電腦上運行？

### 📌 重點
- GGUF 格式：
- llama.cpp：
- 量化等級選擇：
- 

### 🔧 實作
```python
# 來源：
# 用途：地端模型載入與推理

# from llama_cpp import Llama

# llm = Llama(model_path="./model.gguf", n_ctx=2048)
# output = llm("請問什麼是自然語言處理？", max_tokens=256)
```

### 📚 延伸
- [llama.cpp GitHub](https://github.com/ggerganov/llama.cpp)
- [GGUF 格式說明](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
- [Ollama](https://ollama.ai/)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：05_情感分析](05_情感分析.md) | [下一篇：07_LLM微調 →](07_LLM微調.md)
