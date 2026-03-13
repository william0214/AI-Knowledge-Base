# Knowledge Pipeline v3 — 全感官知識管線自動化專案

> tags: #Project #Pipeline #Automation #KnowledgeGraph

## 概述

個人 AI 知識庫的全感官自動化系統 — 讀、看、聽三感官輸入，搭配 Neo4j 知識圖譜與 GraphRAG 查詢。
詳細架構設計 → `03_Architecture/Knowledge_Pipeline.md`

## 六階段流水線

| 階段 | 比喻 | 模組 | 輸出位置 |
|---|---|---|---|
| **① 爬** (Crawl) | 覓食 | 讀/看/聽 三感官爬蟲群 | `09_Staging/raw/` |
| **② 消化** (Digest) | 分解食物 | `digest.py` | `09_Staging/digested/` |
| **③ 咀嚼** (Review) | 反芻把關 | `review_gate.py` | `09_Staging/reviewed/` |
| **④ 產出** (Output) | 吸收養分 | `ingest.py` | 正式目錄 |
| **⑤ 圖譜** (Graph) | 建立神經網路 | `graph_builder.py` | Neo4j |
| **⑥ 查詢** (Bot) | 大腦回答 | `bot_brain.py` | GraphRAG 回答 |

## 三感官輸入

| 感官 | 模組 | 來源 | 技術 |
|---|---|---|---|
| 讀 Read | `youtube_crawler.py` | YouTube 字幕 | `yt-dlp` |
| 讀 Read | `web_crawler.py` | 技術文章 | `httpx` + `BeautifulSoup` |
| 讀 Read | `rss_monitor.py` | RSS Feed | `feedparser` |
| 看 Vision | `pdf_extractor.py` | PDF | `PyMuPDF` + `PaddleOCR` |
| 看 Vision | `ppt_extractor.py` | PPT/PPTX | `python-pptx` |
| 看 Vision | `vision_reader.py` | 圖片/白板 | `PaddleOCR` / `GPT-4o Vision` |
| 聽 Audio | `audio_transcriber.py` | 影片/Podcast/會議 | `Whisper` + `pyannote` |

## 專案結構

```
Knowledge_Pipeline/
├── README.md
├── requirements.txt
├── .env                              ← API keys (gitignore)
├── config/
│   ├── sources.yaml                  ← 追蹤的頻道 / 網站 / RSS 來源
│   ├── review_prompt.txt             ← LLM 審核用 Prompt
│   ├── digest_prompt.txt             ← LLM 消化用 Prompt
│   ├── entity_extraction_prompt.txt  ← 實體提取 Prompt
│   └── graph_schema.yaml             ← Neo4j schema 定義
├── src/
│   ├── __init__.py
│   ├── # ── 讀 Read ──
│   ├── youtube_crawler.py            ← YouTube 字幕 + metadata 爬蟲
│   ├── web_crawler.py                ← 技術文章爬蟲
│   ├── rss_monitor.py                ← RSS 訂閱監控
│   ├── # ── 看 Vision ──
│   ├── pdf_extractor.py              ← PDF 文字/OCR 提取
│   ├── ppt_extractor.py              ← PPT 簡報提取
│   ├── vision_reader.py              ← 圖片 OCR (PaddleOCR/GPT-4o)
│   ├── # ── 聽 Audio ──
│   ├── audio_transcriber.py          ← 語音轉文字 (Whisper)
│   ├── # ── 消化 / 審核 / 入庫 ──
│   ├── digest.py                     ← LLM 摘要 + 結構化 + 實體提取
│   ├── review_gate.py                ← LLM 評分 + 人工審核 CLI
│   ├── ingest.py                     ← 自動分類入庫
│   ├── # ── 圖譜 Graph ──
│   ├── graph_builder.py              ← 實體/關係 → Neo4j
│   ├── graph_query.py                ← Cypher 查詢封裝
│   ├── # ── Bot 查詢 ──
│   └── bot_brain.py                  ← GraphRAG + Vector 混合查詢
├── docker/
│   └── docker-compose.yaml           ← Neo4j + Chroma
└── tests/
    └── ...
```

## 快速開始

```bash
# 安裝依賴
pip install -r requirements.txt

# ── 讀 Read ──
python src/youtube_crawler.py --url "https://youtube.com/watch?v=..."
python src/youtube_crawler.py --channel "3Blue1Brown" --limit 5
python src/web_crawler.py --url "https://..."
python src/rss_monitor.py --check

# ── 看 Vision ──
python src/pdf_extractor.py --file "paper.pdf"
python src/ppt_extractor.py --file "slides.pptx"
python src/vision_reader.py --image "whiteboard.jpg"

# ── 聽 Audio ──
python src/audio_transcriber.py --url "https://youtube.com/watch?v=..."
python src/audio_transcriber.py --file "meeting.mp3"

# ── 消化 / 審核 / 入庫 ──
python src/digest.py
python src/review_gate.py
python src/ingest.py

# ── 圖譜 ──
docker compose -f docker/docker-compose.yaml up -d   # 啟動 Neo4j
python src/graph_builder.py
python src/graph_query.py --concept "RAG"

# ── Bot 查詢 ──
python src/bot_brain.py --ask "學完 Embedding 下一步學什麼？"
```

## 技術選型

| 用途 | 技術 | 成本 |
|---|---|---|
| YouTube 爬蟲 | `yt-dlp` | 免費 |
| 網頁爬蟲 | `httpx` + `BeautifulSoup4` | 免費 |
| RSS 監控 | `feedparser` | 免費 |
| PDF 解析 | `PyMuPDF` + `PaddleOCR` | 免費 |
| PPT 解析 | `python-pptx` | 免費 |
| 圖片 OCR | `PaddleOCR` / `GPT-4o Vision` | 免費/付費 |
| 語音辨識 | `openai-whisper` (large-v3) | 免費 |
| 講者分離 | `pyannote-audio` | 免費 |
| LLM | `openai` SDK (GPT-4o) | 付費 |
| 知識圖譜 | `Neo4j Community` (Docker) | 免費 |
| 向量資料庫 | `Chroma` / `FAISS` | 免費 |
| CLI 介面 | `rich` | 免費 |
| 設定管理 | `PyYAML` + `python-dotenv` | 免費 |

## 開發優先序

| 優先序 | 階段 | 狀態 |
|---|---|---|
| P0 | Stage 1 讀 (Crawl) | ✅ v1 已實作 |
| P1 | Stage 2-4 消化+咀嚼+產出 | ✅ v1 已實作 |
| P2 | Stage 1 聽 (Whisper) | 📋 已規劃 |
| P3 | Stage 5 圖譜化 (Neo4j) | 📋 已規劃 |
| P4 | Stage 1 看 (OCR/Vision) | 📋 已規劃 |
| P5 | Stage 6 Bot 查詢 (GraphRAG) | 📋 已規劃 |
