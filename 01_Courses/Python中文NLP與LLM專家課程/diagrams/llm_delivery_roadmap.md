# LLM Delivery Roadmap

## Fine-tuning to Deployment Roadmap

```mermaid
flowchart LR
    A[任務定義 / 問答資料] --> B[資料清洗與格式化]
    B --> C[HuggingFace Repo / Training Assets]
    C --> D[Fine-tuning\nOpenAI FT or QLoRA]
    D --> E[Adapter Merge / Model Validation]
    E --> F[GGUF 轉換與量化]
    F --> G[LM Studio 本地測試]
    G --> H[MCP 工具接入]
    H --> I[vLLM / OpenAI-compatible API]
    I --> J[企業應用系統]
```

## Knowledge and Serving Split

```mermaid
flowchart TD
    A[企業文件 / PDF / 知識庫] --> B[RAG Pipeline]
    C[微調模型] --> D[GGUF / API Model]
    B --> E[LM Studio / App Layer]
    D --> E
    F[MCP Tools] --> E
    E --> G[客服 / 知識管理 / 分析系統]
```

## Stage Mapping

```mermaid
flowchart LR
    A[07_LLM微調] --> B[GGUF / LM Studio]
    B --> C[06_RAG與Agent\nMCP / Tool Use]
    C --> D[08_企業部署\nvLLM / Serving / MLOps]
```

說明：
- 第一張圖是單一路徑，強調從資料準備到可部署模型的工程順序。
- 第二張圖是雙軌架構，強調「知識補強」與「模型能力」在應用層匯合。
- 第三張圖把知識庫筆記章節直接映射到技術交付階段。