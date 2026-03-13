---
title: "LLM 微調 — Fine-tuning ChatGPT 及開源模型"
date: 2026-03-12
day: Day4
tags: [LLM, FineTuning, Day4]
status: in-progress
chapter: "§10"
---

# 07 — LLM 微調：Fine-tuning ChatGPT 及開源模型

> tags: #LLM #FineTuning #Day4 #in-progress
> 對應課程章節：§10 微調 ChatGPT 及 LLM，打造產業專屬 AI 助手
> 原始講義：[PNLP上課筆記_2026-03-09.pdf](assets/PNLP上課筆記_2026-03-09.pdf)
> 主要來源頁碼：41–45, 66–67, 77–78, 98–102

---

## 7.1 微調在企業 AI 路線中的定位

### 💡 思考
- 微調是用來補知識，還是補風格、格式與行為？
- 在企業場景中，什麼時候該先做 RAG，什麼時候該直接做 fine-tuning？

### 📌 重點
- 課堂把微調放在 RAG 與部署之間，代表它被視為能力增強手段，而不是唯一解法。
- 微調更適合：
  - 穩定輸出格式
  - 特定任務行為習慣
  - 領域語氣與專屬應答風格
- 若需求是最新知識查詢，仍需 RAG 搭配。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 41-45, 77-78 頁
# 用途：微調 vs RAG 的決策參考

when_to_finetune = [
    "stable output format",
    "domain-specific response style",
    "task-specific behavior alignment",
]

when_to_use_rag = [
    "need up-to-date knowledge",
    "need source-grounded answers",
    "frequently changing documents",
]
```

### 📚 延伸
- [OpenAI Fine-tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)

---

## 7.2 HuggingFace 資源、模型倉庫與資料準備

### 💡 思考
- 為什麼課堂要求先建立 HuggingFace repo，再開始後續 Lab？
- 微調前的資料整理，比訓練技巧更重要的原因是什麼？

### 📌 重點
- HuggingFace 在課堂中同時是：
  - 模型下載來源
  - 微調成果上傳位置
  - 模型版本管理平台
- 課堂要求建立多個 repo，表示流程設計已包含「訓練後發布」這一步。
- 資料準備的核心是格式一致、品質穩定、任務定義明確。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 41-44 頁
# 用途：微調資料格式骨架

training_data = [
    {
        "messages": [
            {"role": "system", "content": "你是企業內部的知識管理助手"},
            {"role": "user", "content": "..."},
            {"role": "assistant", "content": "..."},
        ]
    }
]
```

### 📚 延伸
- [HuggingFace Hub](https://huggingface.co/docs/hub/index)

---

## 7.3 QLoRA、4-bit 量化與低成本微調

### 💡 思考
- QLoRA 真正降低的是顯存、算力，還是微調門檻？
- 為什麼 4-bit 量化能讓更多開源模型進入單卡訓練範圍？

### 📌 重點
- 課堂微調主軸之一是 QLoRA。
- 核心概念：
  - LoRA：只訓練低秩 adapter，而非整個模型。
  - QLoRA：在 LoRA 基礎上加入 4-bit 量化，進一步降低資源需求。
- 這條路線是企業私有化與開源模型落地的關鍵技術之一。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 66-67, 98-100 頁
# 用途：QLoRA 設定骨架

# from peft import LoraConfig
# from transformers import BitsAndBytesConfig

# bnb_config = BitsAndBytesConfig(
#     load_in_4bit=True,
#     bnb_4bit_quant_type="nf4",
# )

# lora_config = LoraConfig(
#     r=16,
#     lora_alpha=32,
#     lora_dropout=0.05,
#     task_type="CAUSAL_LM",
# )
```

### 📚 延伸
- [QLoRA 論文](https://arxiv.org/abs/2305.14314)
- [PEFT](https://huggingface.co/docs/peft/)

---

## 7.4 Adapter 合併與模型發布

### 💡 思考
- Adapter 合併後，應該怎麼確認模型沒有退化？
- 微調後模型是保存 adapter 即可，還是要輸出完整模型？

### 📌 重點
- 課堂內容涵蓋 LoRA / QLoRA adapter 合併。
- 這一步的意義是把增量權重整理成更易部署或共享的形式。
- 合併之後仍需重新驗證輸出品質、任務成功率與格式穩定度。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 100-102 頁
# 用途：Adapter merge 示意

# from peft import PeftModel
# base_model = AutoModelForCausalLM.from_pretrained("base_model_path")
# peft_model = PeftModel.from_pretrained(base_model, "adapter_path")
# merged_model = peft_model.merge_and_unload()
```

### 📚 延伸
- [PEFT Merge Adapters](https://huggingface.co/docs/peft/conceptual_guides/lora#merge-lora-weights-into-the-base-model)

---

## 7.5 OpenAI Fine-tuning 與企業知識任務

### 💡 思考
- OpenAI 微調適合做知識回答，還是更適合格式 / 任務行為調整？
- 若企業已有 RAG，還需要 OpenAI fine-tuning 嗎？

### 📌 重點
- 課堂明確涵蓋 OpenAI 微調工作流：
  - 準備 JSONL 資料
  - 上傳訓練檔
  - 建立 fine-tune job
  - 監看訓練狀態
  - 使用微調後模型
- 實務上比較合理的分工通常是：
  - RAG 補知識
  - Fine-tuning 補格式、風格、行為

### 🔧 實作
```python
# 來源：課程講義 PDF 第 77-78 頁
# 用途：OpenAI fine-tuning 流程骨架

# from openai import OpenAI
# client = OpenAI()

# file = client.files.create(
#     file=open("training_data.jsonl", "rb"),
#     purpose="fine-tune",
# )

# job = client.fine_tuning.jobs.create(
#     training_file=file.id,
#     model="gpt-4o-mini-2024-07-18",
# )
```

### 📚 延伸
- [OpenAI Fine-tuning](https://platform.openai.com/docs/guides/fine-tuning)

---

## 7.6 開源模型微調：LLaMA、Mistral、Gemma

### 💡 思考
- 開源模型微調與閉源 API 微調，差別主要在控制權、成本還是維運責任？
- 哪些情況下開源模型值得承擔額外部署成本？

### 📌 重點
- 課程把 LLaMA、Mistral、Gemma 放在同一條開源模型線上比較。
- 開源模型路線的主要價值：
  - 可私有化
  - 可控部署
  - 可結合量化與本地推理
- 代價是更高的環境、部署與效能調校成本。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 98-102 頁
# 用途：開源模型微調骨架

# from transformers import AutoModelForCausalLM, AutoTokenizer
# from trl import SFTTrainer
```

### 📚 延伸
- [Llama](https://www.llama.com/)
- [Mistral](https://mistral.ai/)
- [Gemma](https://ai.google.dev/gemma)
- [llm_delivery_roadmap.md](diagrams/llm_delivery_roadmap.md)

---

## 7.7 圖表補述：從微調到部署的技術路線

### 💡 思考
- 微調完成後，為什麼還需要 GGUF、LM Studio、MCP、vLLM 這些後續環節？
- 哪些步驟屬於模型產製，哪些步驟已進入應用與服務治理？

### 📌 重點
- 技術路線可拆成一條主線：
  - `資料清洗與格式化` -> `Fine-tuning / QLoRA` -> `Adapter Merge` -> `GGUF 轉換與量化` -> `LM Studio 本地驗證` -> `MCP 工具接入` -> `vLLM / API Serving`
- 其中：
  - 微調、合併、量化屬於模型產製。
  - LM Studio、MCP、vLLM 屬於測試、工具整合與服務化。
- 若系統還要查企業知識，則會額外與 RAG 流程在應用層匯合。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 66-67, 77-78, 97-117 頁
# 用途：保存微調後交付路徑

delivery_roadmap = [
    "data_preparation",
    "fine_tuning_or_qlora",
    "adapter_merge",
    "gguf_conversion",
    "lm_studio_validation",
    "mcp_integration",
    "vllm_serving",
]
```

### 📚 延伸
- [llm_delivery_roadmap.md](diagrams/llm_delivery_roadmap.md)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：06_RAG與Agent](06_RAG與Agent.md) | [下一篇：08_企業部署 →](08_企業部署.md)
