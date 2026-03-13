# 個人 AI 知識庫 — My AI Brain 🧠

> **數位第二大腦** — 將學習、工作、思考的知識結構化，最終成為個人 AI 機器人的記憶來源。
>
> 📍 Azure DevOps：`https://dev.azure.com/wei-yuanhuang/_git/myKnowledge`
> 📅 建立日期：2026/03/13

---

## Knowledge Pipeline 知識管線

:::mermaid
graph TD
    subgraph "1.Crawl"
        S1[外訓課程] --> C1[01_Courses]
        S2[YouTube] --> YC[youtube_crawler.py]
        S3[技術文章] --> WC[web_crawler.py]
        S4[工作專案] --> C3[11_Projects]
        S5[研討會] --> C5[13_Insights]
        YC --> RAW[09_Staging/raw/]
        WC --> RAW
    end

    subgraph "2.Digest"
        RAW --> DG[digest.py]
        DG -->|LLM| DIG[09_Staging/digested/]
    end

    subgraph "3.Review"
        DIG --> RG[review_gate.py]
        RG -->|LLM 評分| SCORE{總分判定}
        SCORE -->|pass| REV[09_Staging/reviewed/]
        SCORE -->|needs-review| HUMAN[人工把關]
        SCORE -->|reject| REJ[rejected/]
        HUMAN -->|approve| REV
    end

    subgraph "4.Output"
        REV --> ING[ingest.py]
        C1 --> P1[02_Concepts]
        ING --> YT[10_Learning/]
        ING --> CON[02_Concepts/]
        ING --> ARC[03_Architecture/]
        ING --> BOT[08_Bot_Knowledge]
        P1 --> BOT
    end

    style RAW fill:#e3f2fd,stroke:#1976d2
    style DIG fill:#fff3e0,stroke:#f57c00
    style REV fill:#e8f5e9,stroke:#388e3c
    style REJ fill:#ffebee,stroke:#d32f2f
    style BOT fill:#f9a825,stroke:#f57f17,color:#000
:::
