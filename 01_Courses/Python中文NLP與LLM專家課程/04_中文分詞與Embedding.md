---
title: "中文分詞與 Embedding"
date: 2026-03-10
day: Day2
tags: [NLP, Embedding, Day2]
status: in-progress
chapter: "§5, §6"
---

# 04 — 中文分詞與 Embedding

> tags: #NLP #Embedding #Day2 #in-progress
> 對應課程章節：§5 Tokenization & Embedding + §6 文章分類與語意理解
> 原始講義：[PNLP上課筆記_2026-03-09.pdf](assets/PNLP上課筆記_2026-03-09.pdf)
> 主要來源頁碼：17–24, 33

---

## 4.1 Jieba 與 CKIP 的中文分詞實務

### 💡 思考
- 為什麼中文分詞會直接影響後續分類與情感分析？
- 繁體中文場景下，Jieba 與 CKIP 的選型邏輯是什麼？

### 📌 重點
- 課堂核心分詞工具是 Jieba 與 CKIP Transformers。
- Jieba 適合快速 baseline、詞頻與 TF-IDF 特徵工程。
- CKIP 更適合繁體中文，並能延伸到詞性標記與 NER。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 17, 19 頁
# 用途：Jieba / CKIP 分詞示意

import jieba

words = jieba.cut("自然語言處理是人工智慧的重要領域")
print(" / ".join(words))

# from ckip_transformers.nlp import CkipWordSegmenter
# ws_driver = CkipWordSegmenter(device=-1)
# print(ws_driver(["自然語言處理是人工智慧的重要領域"]))
```

### 📚 延伸
- [Jieba GitHub](https://github.com/fxsjy/jieba)
- [CKIP Transformers](https://github.com/ckiplab/ckip-transformers)

---

## 4.2 CKIP Transformers 的分詞、詞性與 NER

### 💡 思考
- 為什麼 CKIP 在繁體中文 NLP 任務中很有優勢？
- NER 對企業文件、客服與新聞分析有哪些直接用途？

### 📌 重點
- CKIP 的主要元件：
  - `CkipWordSegmenter`
  - `CkipPosTagger`
  - `CkipNerChunker`
- 課堂示例包含人名、組織、地點、日期、貨幣等實體抽取。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 19-20 頁
# 用途：CKIP NER 示意

from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker

ws_driver = CkipWordSegmenter(device=-1)
pos_driver = CkipPosTagger(device=-1)
ner_driver = CkipNerChunker(device=-1)
```

### 📚 延伸
- [CKIP 線上 Demo](https://ckip.iis.sinica.edu.tw/service/transformers/)

---

## 4.3 詞性、N-Gram 與字典更新

### 💡 思考
- 為什麼分詞器需要持續更新字典？
- N-Gram 除了建模，也能如何回饋分詞品質？

### 📌 重點
- 課堂列出 Jieba 常見詞性標籤，幫助後續特徵工程與實體辨識。
- N-Gram 概念包含 Unigram、Bigram、Trigram。
- 常見做法是從語料中找高共現詞，再回填自定義字典改善新詞切分。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 21, 33 頁
# 用途：N-Gram 概念索引

n_grams = {
    1: "Unigram",
    2: "Bigram",
    3: "Trigram",
}
```

### 📚 延伸
- [NLTK](https://www.nltk.org/)

---

## 4.4 TF-IDF、Word2Vec 與語意向量化

### 💡 思考
- 稀疏向量與 dense embedding 的應用邊界在哪裡？
- Word2Vec 適合哪些語意探索任務，而不一定適合哪些分類任務？

### 📌 重點
- TF-IDF：適合關鍵詞、可解釋分類 baseline、文件相似度初步分析。
- Word2Vec：適合語意相似詞、人物關係與語義空間探索。
- 課堂案例包含劇本分析、人物關聯與 Beauty 類別語料。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 24 頁
# 用途：Word2Vec 訓練骨架

from gensim.models import Word2Vec

# sentences = [["自然語言", "處理"], ["機器學習", "深度學習"]]
# model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)
```

### 📚 延伸
- [Gensim Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)
- [Sentence Transformers](https://www.sbert.net/)

---

## 4.5 CKIP 效能測試與工具選型

### 💡 思考
- 分詞精度與吞吐量，哪一個在企業批次任務更重要？
- 什麼規模的語料才值得切到 GPU？

### 📌 重點
- 課堂提供 CKIP 測試數據：
  - CPU 1 thread：140s / 100 篇
  - CPU 24 threads：27s / 100 篇
  - GPU 3090：24s / 1000 篇
- 對社群監控、新聞分類或知識管線，GPU 可顯著提升吞吐量。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 23 頁
# 用途：保留 CKIP 效能摘要

ckip_benchmark = {
    "cpu_1_thread": "140s / 100 docs",
    "cpu_24_threads": "27s / 100 docs",
    "gpu_3090": "24s / 1000 docs",
}
```

### 📚 延伸
- [CKIP Transformers](https://github.com/ckiplab/ckip-transformers)

---

## 4.6 圖表補述：CKIP 效能比較圖

### 💡 思考
- 效能圖真正要傳達的是單次速度，還是批次吞吐量？
- 同一套分詞流程在 CPU 與 GPU 上的部署策略，應該如何切分？

### 📌 重點
- 講義第 23 頁可視為一張效能趨勢圖：
  - 橫軸是 CPU thread 數與 GPU 平台。
  - 縱軸是處理時間。
- 箭頭關係是：`thread 數增加` -> `CPU 耗時下降`。
- 另一條對照線是：`3090 GPU` 在更大資料量下仍維持低耗時，代表 GPU 更適合大批量中文斷詞與 NER。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 23 頁
# 用途：保留圖表數據以支援效能判讀

ckip_benchmark = {
    "cpu_1_thread": "140s / 100 docs",
    "cpu_24_threads": "27s / 100 docs",
    "gpu_3090": "24s / 1000 docs",
}
```

### 📚 延伸
- [04_中文分詞與Embedding](04_中文分詞與Embedding.md)
- [ckip_benchmark.md](diagrams/ckip_benchmark.md)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：03_資料採集與前處理](03_資料採集與前處理.md) | [下一篇：05_情感分析 →](05_情感分析.md)
