# Course Learning Map

## 01-08 Learning Map

```mermaid
flowchart TD
    A[01 課程總覽\n課程定位 / Lesson 地圖 / 平台資源]
    B[02 NLP 基礎\n分類問題 / 傳統模型 / 深度模型觀念]
    C[03 資料採集與前處理\n爬蟲 / JSON / 清洗 / 訓練集建立]
    D[04 中文分詞與 Embedding\nJieba / CKIP / TF-IDF / Word2Vec]
    E[05 情感分析\nBaseline / RNN / BERT / 細粒度分類]
    F[06 RAG 與 Agent\n檢索增強 / Prompt / LangGraph / MCP]
    G[07 LLM 微調\nFine-tuning / QLoRA / GGUF]
    H[08 企業部署\nAPI / LM Studio / vLLM / MLOps]

    A --> B
    A --> C
    B --> D
    C --> D
    D --> E
    B --> E
    E --> F
    D --> F
    F --> G
    G --> H
    F --> H
```

## Learning Stages

```mermaid
flowchart LR
    A[基礎理解\n01-02] --> B[資料與特徵工程\n03-04]
    B --> C[任務模型化\n05]
    C --> D[LLM 能力擴增\n06-07]
    D --> E[系統交付與維運\n08]
```

## Concept Dependency View

```mermaid
flowchart LR
    A[資料來源] --> B[前處理]
    B --> C[分詞 / Embedding]
    C --> D[分類 / 情感分析]
    D --> E[RAG / Agent]
    E --> F[Fine-tuning]
    F --> G[Deployment]
    E --> G
```

說明：
- 第一張圖用章節檔案當節點，表示知識庫閱讀順序與依賴關係。
- 第二張圖把 01-08 壓成五個學習階段，方便從課程節奏理解全貌。
- 第三張圖則抽象成概念依賴鏈，方便之後延伸到別的課程或專案。