# Knowledge Pipeline 操作手冊

> tags: #SOP #Pipeline #Workflow

## 概述

Knowledge Pipeline 四階段操作流程：**爬 → 消化 → 咀嚼 → 產出**

## 前置準備

### 1. 安裝依賴

```bash
cd 11_Projects/Knowledge_Pipeline
pip install -r requirements.txt
```

### 2. 設定環境變數

在 `11_Projects/Knowledge_Pipeline/` 建立 `.env` 檔：

```
OPENAI_API_KEY=sk-xxxxxxxx
OPENAI_MODEL=gpt-4o
# 如果用 Azure OpenAI:
# OPENAI_BASE_URL=https://your-resource.openai.azure.com/
```

### 3. 設定來源清單

編輯 `config/sources.yaml`，加入要追蹤的 YouTube 頻道和網站。

---

## 日常操作

### Stage 1: 爬取 (Crawl)

```bash
# 爬取單一 YouTube 影片
python src/youtube_crawler.py --url "https://youtube.com/watch?v=xxxxx"

# 爬取頻道最新 5 部影片
python src/youtube_crawler.py --channel "https://www.youtube.com/@AndrejKarpathy" --limit 5

# 從 sources.yaml 批量爬取所有來源
python src/youtube_crawler.py --config

# 爬取技術文章
python src/web_crawler.py --url "https://lilianweng.github.io/posts/..."

# 從 sources.yaml 批量爬取所有網站
python src/web_crawler.py --config
```

**結果**：原始 Markdown 檔會出現在 `09_Staging/raw/`

### Stage 2: 消化 (Digest)

```bash
# 消化所有 raw/ 中的檔案
python src/digest.py

# 消化指定檔案
python src/digest.py --file ../../09_Staging/raw/2026-03-13_youtube_xxx.md

# 預覽模式（不呼叫 LLM）
python src/digest.py --dry-run
```

**結果**：LLM 結構化後的 Markdown 會出現在 `09_Staging/digested/`

### Stage 3: 咀嚼 / 審核 (Review)

```bash
# 互動式審核（推薦）— LLM 評分 + 人工把關
python src/review_gate.py

# 純 LLM 自動審核（不需人工介入）
python src/review_gate.py --auto-only

# 審核指定檔案
python src/review_gate.py --file ../../09_Staging/digested/xxx.md
```

**互動操作**：
- `approve` — 通過，移到 `reviewed/`
- `reject` — 拒絕，移到 `rejected/`
- `view` — 查看完整內容
- `skip` — 跳過，稍後再審

### Stage 4: 入庫 (Ingest)

```bash
# 入庫所有通過審核的檔案
python src/ingest.py

# 預覽入庫結果（不實際執行）
python src/ingest.py --dry-run

# 入庫指定檔案
python src/ingest.py --file ../../09_Staging/reviewed/xxx.md
```

**結果**：檔案自動分發到正式目錄 + `08_Bot_Knowledge/INDEX.md` 更新

---

## 一鍵全流程

```bash
cd 11_Projects/Knowledge_Pipeline

# 爬 → 消化 → 審核（互動）→ 入庫
python src/youtube_crawler.py --config && \
python src/web_crawler.py --config && \
python src/digest.py && \
python src/review_gate.py && \
python src/ingest.py
```

---

## 新增來源

編輯 `config/sources.yaml`：

```yaml
youtube:
  channels:
    - name: "新頻道名稱"
      url: "https://www.youtube.com/@channel"
      tags: ["#標籤1", "#標籤2"]
      language: "en"

websites:
  blogs:
    - name: "新部落格"
      url: "https://blog.example.com"
      tags: ["#標籤"]
      selector: "article"   # 文章主體的 CSS selector
```

---

## 疑難排解

| 問題 | 解法 |
|---|---|
| `yt-dlp` 找不到 | `pip install yt-dlp` 或 `brew install yt-dlp` |
| 字幕抓不到 | 影片可能沒有字幕，檢查 `subtitle_languages` 設定 |
| LLM API 錯誤 | 確認 `.env` 中的 `OPENAI_API_KEY` 是否正確 |
| 入庫分類錯誤 | 檢查審核記錄中的「建議分類」是否正確 |
| `raw/` 檔案堆積 | 執行 `python src/digest.py` 消化 |
