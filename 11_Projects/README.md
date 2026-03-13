# 11_Projects — 工作專案經驗

> tags: #Meta

## 目的

記錄工作專案的技術決策、實作經驗、踩坑紀錄與解決方案，累積可複用的實戰知識。

## 結構規範

每個專案建立一個獨立子目錄，結構如下：

```
11_Projects/
└── 專案名稱/
    ├── README.md        ← 專案概述、架構、技術棧
    ├── notes/           ← 開發筆記、問題紀錄
    │   └── YYYY-MM-DD_主題.md
    └── assets/          ← 截圖、設定檔、範例資料
```

## 建議內容

- **README.md**：專案背景、架構圖（Mermaid）、技術選型、學到的教訓
- **notes/**：每次有值得記錄的技術決策或問題解決過程，寫一篇筆記
- **assets/**：相關的截圖、設定範本、測試資料

## 範例

```
11_Projects/
├── 客服機器人_POC/
│   ├── README.md
│   ├── notes/
│   │   ├── 2026-03-20_RAG_pipeline_設計.md
│   │   └── 2026-03-25_向量資料庫_選型.md
│   └── assets/
│       └── architecture_v1.png
└── 內部知識搜尋系統/
    ├── README.md
    └── notes/
```
