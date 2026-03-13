# Knowledge Pipeline — 知識管線自動化專案

> tags: #Project #Pipeline #Automation

## 概述

個人 AI 知識庫的自動化搜集、消化、審核、入庫系統。

## 四階段流水線

| 階段 | 比喻 | 模組 | 輸出位置 |
|---|---|---|---|
| **爬** (Crawl) | 覓食 | `youtube_crawler.py` / `web_crawler.py` | `09_Staging/raw/` |
| **消化** (Digest) | 分解食物 | `digest.py` | `09_Staging/digested/` |
| **咀嚼** (Review) | 反芻把關 | `review_gate.py` | `09_Staging/reviewed/` |
| **產出** (Output) | 吸收養分 | `ingest.py` | 正式目錄 + `08_Bot_Knowledge/` |

## 專案結構

```
Knowledge_Pipeline/
├── README.md
├── requirements.txt
├── config/
│   ├── sources.yaml          ← 追蹤的頻道 / 網站 / RSS 來源
│   └── review_prompt.txt     ← LLM 審核用 Prompt
├── src/
│   ├── __init__.py
│   ├── youtube_crawler.py    ← YouTube 字幕 + metadata 爬蟲
│   ├── web_crawler.py        ← 技術文章爬蟲
│   ├── digest.py             ← LLM 自動摘要 / 結構化 / 分類
│   ├── review_gate.py        ← LLM 評分 + 人工審核 CLI
│   └── ingest.py             ← 自動分類入庫 + 更新索引
└── tests/
    └── ...
```

## 快速開始

```bash
# 安裝依賴
pip install -r requirements.txt

# 爬取 YouTube 影片
python src/youtube_crawler.py --url "https://youtube.com/watch?v=..."

# 爬取指定頻道的最新影片
python src/youtube_crawler.py --channel "3Blue1Brown" --limit 5

# 爬取技術文章
python src/web_crawler.py --url "https://..."

# 消化（LLM 結構化）
python src/digest.py

# 審核（互動式）
python src/review_gate.py

# 入庫
python src/ingest.py
```

## 技術選型

| 用途 | 技術 | 原因 |
|---|---|---|
| YouTube 爬蟲 | `yt-dlp` | 免費、不需 API key、支援字幕 |
| 網頁爬蟲 | `httpx` + `BeautifulSoup4` | 輕量、async 支持 |
| LLM 呼叫 | `openai` SDK | 相容 OpenAI / Azure OpenAI |
| 設定管理 | `PyYAML` | 簡單直覺的來源清單管理 |
| CLI 介面 | `rich` | 美觀的終端互動介面 |
