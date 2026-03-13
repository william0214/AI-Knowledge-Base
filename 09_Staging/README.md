# 09_Staging — Knowledge Pipeline 暫存區

> tags: #Meta #Pipeline

## 目的

Knowledge Pipeline 的中繼站。所有新知識**必須先經過這裡**，不得直接寫入正式目錄。

## 四階段流程

```
爬 (Crawl) → raw/        原始抓取內容
消化 (Digest) → digested/   LLM 結構化處理後的版本
咀嚼 (Review) → reviewed/   人工審核通過的版本
產出 (Output) → 正式目錄     入庫到 10_Learning/ 等目錄
```

## 子目錄

| 目錄 | 階段 | 說明 |
|---|---|---|
| `raw/` | 爬 (Crawl) | 爬蟲原始輸出，未經處理的 Markdown / JSON |
| `digested/` | 消化 (Digest) | LLM 自動摘要、結構化、分類後的版本 |
| `reviewed/` | 咀嚼 (Review) | 人工審核通過、待入庫的最終版本 |

## 檔案命名

所有暫存檔案統一格式：

```
YYYY-MM-DD_來源類型_標題.md
```

範例：
- `2026-03-13_youtube_3Blue1Brown_Attention機制.md`
- `2026-03-13_article_RAG_Best_Practices.md`

## 注意事項

- `raw/` 和 `digested/` 的內容是暫時的，定期清理
- `reviewed/` 通過入庫後檔案會被移走
- 不要手動把檔案放進正式目錄，一律走 Pipeline
