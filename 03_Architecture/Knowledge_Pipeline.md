# Knowledge Pipeline — 知識管線架構設計

> tags: #Architecture #Pipeline #Automation

## 概述

Knowledge Pipeline 是一套四階段的知識自動化流水線，從原始知識來源到 AI Bot 可用知識庫的完整流程。

## 架構圖

:::mermaid
graph TD
    subgraph "Stage 1: 爬 Crawl 🕷️"
        Y[YouTube 頻道/影片] --> YC[youtube_crawler.py]
        W[技術部落格/文章] --> WC[web_crawler.py]
        M[手動輸入] --> RAW
        YC --> RAW[09_Staging/raw/]
        WC --> RAW
    end

    subgraph "Stage 2: 消化 Digest 🧬"
        RAW --> DG[digest.py]
        DG -->|呼叫 LLM| LLM1[GPT-4o]
        LLM1 -->|摘要/結構化/分類| DIG[09_Staging/digested/]
    end

    subgraph "Stage 3: 咀嚼 Review 🔍"
        DIG --> RG[review_gate.py]
        RG -->|LLM 評分| LLM2[GPT-4o]
        LLM2 -->|5 維度評分| SCORE{總分判定}
        SCORE -->|≥18 自動通過| REV[09_Staging/reviewed/]
        SCORE -->|13-17 人工審核| HUMAN[👤 人工把關]
        SCORE -->|≤12 建議拒絕| REJ[09_Staging/rejected/]
        HUMAN -->|approve| REV
        HUMAN -->|reject| REJ
    end

    subgraph "Stage 4: 產出 Output 📦"
        REV --> ING[ingest.py]
        ING -->|YouTube| YT[10_Learning/YouTube/]
        ING -->|文章| ART[10_Learning/Articles/]
        ING -->|概念| CON[02_Concepts/]
        ING -->|架構| ARC[03_Architecture/]
        ING -->|更新索引| BOT[🤖 08_Bot_Knowledge/]
    end

    style RAW fill:#e3f2fd,stroke:#1976d2
    style DIG fill:#fff3e0,stroke:#f57c00
    style REV fill:#e8f5e9,stroke:#388e3c
    style REJ fill:#ffebee,stroke:#d32f2f
    style BOT fill:#f9a825,stroke:#f57f17,color:#000
:::

## 四階段說明

### Stage 1: 爬 (Crawl) 🕷️

**目的**：從外部來源自動搜集原始知識素材

| 模組 | 來源 | 技術 | 輸出 |
|---|---|---|---|
| `youtube_crawler.py` | YouTube 影片 | `yt-dlp`（字幕 + metadata） | Markdown |
| `web_crawler.py` | 技術部落格 | `httpx` + `BeautifulSoup` | Markdown |

**輸出格式**：統一的 Markdown，包含 metadata 表格 + 原始內容

**輸出位置**：`09_Staging/raw/`

### Stage 2: 消化 (Digest) 🧬

**目的**：LLM 自動處理原始內容，產出結構化筆記

**處理項目**：
1. 自動摘要（3-5 句話）
2. 關鍵重點提取（5-10 個 bullet points）
3. 核心概念整理
4. 程式碼 / 實作要點
5. 分類建議 + 標籤建議

**LLM**：GPT-4o（可替換為其他模型）

**輸出位置**：`09_Staging/digested/`

### Stage 3: 咀嚼 (Review) 🔍

**目的**：品質把關，確保入庫知識的品質

**雙軌制**：
1. **LLM 自動評分**：五個維度各 1-5 分
   - 相關性 (Relevance)
   - 正確性 (Accuracy)
   - 可操作性 (Actionability)
   - 時效性 (Timeliness)
   - 獨特性 (Uniqueness)

2. **人工最終把關**：CLI 互動介面
   - `approve` — 通過
   - `reject` — 拒絕
   - `view` — 查看完整內容
   - `skip` — 稍後再看

**判定規則**：

| 總分 | 判定 | 動作 |
|---|---|---|
| ≥ 18 | 自動通過 | 直接移至 `reviewed/` |
| 13-17 | 需人工審核 | 等待你的決定 |
| ≤ 12 | 建議拒絕 | 移至 `rejected/` |

### Stage 4: 產出 (Output) 📦

**目的**：將審核通過的知識自動分發到正確目錄

**入庫邏輯**：
1. 偵測審核建議的分類
2. 產生正式檔名
3. 清理流程標籤、套用正式標籤
4. 寫入目標目錄
5. 更新 `08_Bot_Knowledge/INDEX.md`

**分類對應**：

| 內容類型 | 入庫目錄 |
|---|---|
| YouTube 筆記 | `10_Learning/YouTube/` |
| 技術文章 | `10_Learning/Articles/` |
| 線上課程 | `10_Learning/Online_Courses/` |
| 核心概念 | `02_Concepts/` |
| 架構設計 | `03_Architecture/` |
| Prompt 範本 | `05_Prompts/` |
| SOP | `12_SOP/` |
| 產業趨勢 | `13_Insights/Trends/` |

## 技術選型

| 用途 | 技術 | 原因 |
|---|---|---|
| YouTube 爬蟲 | `yt-dlp` | 免費、不需 API key、支援字幕下載 |
| 網頁爬蟲 | `httpx` + `BeautifulSoup4` | 輕量、支援 async、HTML 解析強 |
| LLM 呼叫 | `openai` SDK | 相容 OpenAI / Azure OpenAI |
| 設定管理 | `PyYAML` | 人類可讀的來源清單管理 |
| CLI 介面 | `rich` | 美觀的終端表格、面板、進度條 |
| 環境變數 | `python-dotenv` | 安全管理 API keys |

## 資料流格式

所有中間檔案統一為 Markdown，遵循知識庫的寫作規範：

```
# 標題

> tags: #標籤1 #標籤2

## 基本資訊
| 項目 | 內容 |
|---|---|
| 來源 | ... |
| 日期 | ... |

## 內容
...

## LLM 消化結果
...

## 審核記錄
...
```

## 未來擴展

- [ ] RSS Monitor — 訂閱 RSS feed 自動推送新內容
- [ ] Scheduler — 定時排程自動爬取（cron / GitHub Actions）
- [ ] Web UI — 替代 CLI 的網頁審核介面
- [ ] Vector Embedding — 入庫時同步產生 embedding 存入向量資料庫
- [ ] 重複偵測 — 入庫前比對已有知識，避免重複
