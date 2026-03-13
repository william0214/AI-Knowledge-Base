# 個人 AI 知識庫 — My AI Brain 🧠

> **數位第二大腦** — 將學習、工作、思考的知識結構化，最終成為個人 AI 機器人的記憶來源。
>
> 📍 Azure DevOps：`https://dev.azure.com/wei-yuanhuang/_git/myKnowledge`
> 📅 建立日期：2026/03/13

---

## 願景

:::mermaid
graph LR
    A[� 學習<br>課程/YouTube/文章] --> B[📝 記錄<br>結構化筆記]
    C[💼 工作<br>專案/問題解決] --> B
    D[🌐 觀察<br>趨勢/研討會] --> B
    B --> E[🧩 提取<br>概念卡/SOP]
    E --> F[🏗️ 架構<br>設計文件]
    F --> G[🤖 Bot Knowledge<br>AI 機器人大腦]
    style G fill:#f9a825,stroke:#f57f17,color:#000
:::

> 💡 這個知識庫不只是筆記倉庫，而是一套**知識流水線**：
> 從「輸入」（學習 / 工作 / 觀察）→「處理」（記錄 / 提取 / 架構化）→「輸出」（AI Bot 的可用知識）

---

## 目錄結構

```
AI-Knowledge-Base/
├─ 00_Meta/            ← 知識庫規範與說明
├─ 01_Courses/         ← 外訓課程筆記（按課程分資料夾）
├─ 02_Concepts/        ← 概念知識卡（NLP / LLM / RAG / Agents / MLOps）
├─ 03_Architecture/    ← 架構設計文件
├─ 04_Experiments/     ← 實驗記錄（embeddings / fine-tuning / prompting / evaluation）
├─ 05_Prompts/         ← Prompt 範本庫
├─ 06_Datasets/        ← 資料集說明與來源
├─ 07_Diagrams/        ← 架構圖 / 流程圖
├─ 08_Bot_Knowledge/   ← Bot 知識庫素材（最終輸出）
├─ 10_Learning/        ← 技術學習筆記（YouTube / 線上課程 / 文章）
├─ 11_Projects/        ← 工作專案經驗
├─ 12_SOP/             ← 個人 SOP / 工具備忘
├─ 13_Insights/        ← 產業趨勢 / 技術觀點
└─ 99_Archive/         ← 歸檔
```

---

## 快速導航

### 📚 外訓課程

<details>
<summary><b>Python 中文 NLP 與 LLM 專家課程</b>（恆逸資訊，2026/03/09-12）</summary>

| 檔案 | 對應課程章節 | 上課日 |
|---|---|---|
| [01_課程總覽](01_Courses/Python中文NLP與LLM專家課程/01_課程總覽.md) | §1 ChatGPT 崛起與 NLP 基礎 | Day 1 |
| [02_NLP基礎](01_Courses/Python中文NLP與LLM專家課程/02_NLP基礎.md) | §3 ML速成 + §4 機率生成模型 | Day 1-2 |
| [03_資料採集與前處理](01_Courses/Python中文NLP與LLM專家課程/03_資料採集與前處理.md) | §2 文字資料採集與前處理 | Day 1 |
| [04_中文分詞與Embedding](01_Courses/Python中文NLP與LLM專家課程/04_中文分詞與Embedding.md) | §5 Tokenization & Embedding + §6 文章分類 | Day 2 |
| [05_情感分析](01_Courses/Python中文NLP與LLM專家課程/05_情感分析.md) | §7 情感分析 + §8 姓名性別預測 | Day 3 |
| [06_RAG與Agent](01_Courses/Python中文NLP與LLM專家課程/06_RAG與Agent.md) | §11 RAG 知識擴增與 AI Agents | Day 4 |
| [07_LLM微調](01_Courses/Python中文NLP與LLM專家課程/07_LLM微調.md) | §10 Fine-tuning ChatGPT 及 LLM | Day 4 |
| [08_企業部署](01_Courses/Python中文NLP與LLM專家課程/08_企業部署.md) | §9 NLP 應用案例分析 | Day 3 |
| [09_外訓心得](01_Courses/Python中文NLP與LLM專家課程/09_外訓心得.md) | 完課心得報告 | — |

</details>

### 🏗️ 架構設計

- [企業AI資料中臺](03_Architecture/企業AI資料中臺.md)
- [客服機器人架構](03_Architecture/客服機器人架構.md)
- [知識管理問答系統](03_Architecture/知識管理問答系統.md)
- [私有化LLM部署](03_Architecture/私有化LLM部署.md)

### 📖 學習 / 專案 / SOP / 觀點

| 領域 | 入口 | 說明 |
|---|---|---|
| 技術學習 | [10_Learning/](10_Learning/README.md) | YouTube 筆記、線上課程、文章筆記 |
| 工作專案 | [11_Projects/](11_Projects/README.md) | 專案經驗、技術決策、踩坑紀錄 |
| 個人 SOP | [12_SOP/](12_SOP/README.md) | 工具備忘、環境設定、工作流程 |
| 產業觀點 | [13_Insights/](13_Insights/README.md) | 趨勢分析、研討會心得、技術反思 |

### 📋 規範文件

- [知識庫說明](00_Meta/知識庫說明.md) — 知識庫的目的與使用方式
- [標籤規範](00_Meta/標籤規範.md) — 標籤的分類與使用規則
- [寫作規範](00_Meta/寫作規範.md) — Markdown 格式與模板規範

---

## 標籤速查

| 類別 | 標籤 |
|---|---|
| 主題 | `#NLP` `#LLM` `#RAG` `#Agent` `#MLOps` `#Embedding` `#FineTuning` `#Prompt` |
| 來源 | `#Course` `#SelfStudy` `#Project` `#Conference` |
| 類型 | `#SOP` `#Trend` `#BookNote` `#ArticleNote` |
| 狀態 | `#todo` `#in-progress` `#done` `#review` |
| 日期 | `#Day1` `#Day2` `#Day3` `#Day4` |

## 技術棧

| 領域 | 技術 |
|---|---|
| 語言 | Python |
| NLP | jieba, CKIP, HuggingFace Transformers |
| LLM | ChatGPT, LLaMA, Mistral, Gemma |
| 框架 | LangChain, LlamaIndex |
| 向量 DB | FAISS, Chroma, Weaviate |
| 資料庫 | MongoDB, Neo4j |
| 部署 | Azure, Docker, FastAPI |
| 版控 | Azure DevOps Git |

## 知識流水線

:::mermaid
graph TD
    subgraph 知識輸入來源
        S1[📚 外訓課程]
        S2[� YouTube / 文章]
        S3[🎓 線上課程]
        S4[💼 工作專案]
        S5[🎤 研討會]
        S6[🌐 產業觀察]
    end

    S1 --> C1[01_Courses]
    S2 --> C2[10_Learning]
    S3 --> C2
    S4 --> C3[11_Projects]
    S4 --> C4[12_SOP]
    S5 --> C5[13_Insights]
    S6 --> C5

    subgraph 知識處理
        P1[02_Concepts<br>概念提取]
        P2[03_Architecture<br>架構設計]
        P3[05_Prompts<br>提示詞範本]
    end

    C1 --> P1
    C2 --> P1
    C3 --> P2
    C4 --> P3
    C5 --> P1

    P1 --> BOT[🤖 08_Bot_Knowledge<br>AI 機器人大腦]
    P2 --> BOT
    P3 --> BOT

    style BOT fill:#f9a825,stroke:#f57f17,color:#000
:::
