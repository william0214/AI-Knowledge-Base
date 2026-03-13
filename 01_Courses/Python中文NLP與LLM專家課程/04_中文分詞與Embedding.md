---
title: "中文分詞與 Embedding"
date: 2026-03-10
day: Day2
tags: [NLP, Embedding, Day2]
status: todo
chapter: "§5, §6"
---

# 04 — 中文分詞與 Embedding

> tags: #NLP #Embedding #Day2 #todo
> 對應課程章節：§5 Tokenization & Embedding + §6 文章分類與語意理解

---

## 4.1 中文分詞技術

### 💡 思考
- 中文分詞為什麼比英文困難？（沒有天然空格分隔）
- Ckip、Jieba、HuggingFace Tokenizer 各自的優缺點？
- 分詞精度對下游 NLP 任務（如情感分析）的影響有多大？

### 📌 重點
- Jieba 分詞：
  - 精確模式 / 全模式 / 搜尋引擎模式
- CKIP Tagger：
  - 中研院開發，繁體中文專用
- HuggingFace Tokenizer：
  - BPE / WordPiece / SentencePiece
- 

### 🔧 實作
```python
# 來源：
# 用途：三種分詞工具比較

# Jieba
import jieba
words_jieba = jieba.cut("自然語言處理是人工智慧的重要領域")
print("Jieba:", " / ".join(words_jieba))

# CKIP
# from ckip_transformers.nlp import CkipWordSegmenter
# ws_driver = CkipWordSegmenter(model="bert-base")
# result = ws_driver(["自然語言處理是人工智慧的重要領域"])

# HuggingFace Tokenizer
# from transformers import AutoTokenizer
# tokenizer = AutoTokenizer.from_pretrained("bert-base-chinese")
# tokens = tokenizer.tokenize("自然語言處理是人工智慧的重要領域")
```

### 📚 延伸
- [Jieba GitHub](https://github.com/fxsjy/jieba)
- [CKIP Transformers](https://github.com/ckiplab/ckip-transformers)
- [HuggingFace Tokenizers](https://huggingface.co/docs/tokenizers/)

---

## 4.2 語意向量化技術 (Word Embedding)

### 💡 思考
- Word2Vec 的 CBOW 和 Skip-gram 模型有何差異？
- 為什麼 Word2Vec 能捕捉語意關係（如：國王 - 男人 + 女人 ≈ 女王）？
- 預訓練 Transformer Embedding 相比 Word2Vec 的優勢？

### 📌 重點
- Word2Vec：
- Doc2Vec：
- Sentence Transformers：
- 預訓練模型 Embedding：
- 

### 🔧 實作
```python
# 來源：
# 用途：Word2Vec 訓練與語意相似度查詢

from gensim.models import Word2Vec

# sentences = [["自然", "語言", "處理"], ["機器", "學習", "深度", "學習"]]
# model = Word2Vec(sentences, vector_size=100, window=5, min_count=1)
# similar = model.wv.most_similar("自然", topn=5)
```

### 📚 延伸
- [Gensim Word2Vec](https://radimrehurek.com/gensim/models/word2vec.html)
- [Sentence Transformers](https://www.sbert.net/)
- [Word2Vec 論文](https://arxiv.org/abs/1301.3781)

---

## 4.3 思維鏈推理 (CoT) 在語義關聯推導的應用

### 💡 思考
-  (CoT) 如何幫助模型進行多步驟語義推理？
- CoT 在哪些 NLP 任務中特別有效？
- Zero-shot CoT vs Few-shot CoT 的差異？

### 📌 重點
- CoT 原理：
- 應用場景：
- Prompt 設計要點：
- 

### 🔧 實作
```python
# 來源：
# 用途：CoT Prompt 範例

cot_prompt = """
請一步一步分析以下文本的語意關聯：
文本：...

步驟 1：識別關鍵詞
步驟 2：分析詞彙間的語意關係
步驟 3：推導整體語意
"""
```

### 📚 延伸
- [Chain-of-Thought Prompting (論文)](https://arxiv.org/abs/2201.11903)

---

## 4.4 詞袋模型 (Bag of Words) 與 TF-IDF

### 💡 思考
- BoW 模型為什麼忽略詞序？這在什麼場景下是可接受的？
- TF-IDF 如何平衡「詞頻」與「文件稀有度」？
- TF-IDF 的限制是什麼？Embedding 方法如何克服？

### 📌 重點
- Bag of Words：
- TF-IDF 公式：$\text{TF-IDF}(t,d) = \text{TF}(t,d) \times \log\frac{N}{\text{DF}(t)}$
- 特徵工程：
- 

### 🔧 實作
```python
# 來源：
# 用途：TF-IDF 特徵提取

from sklearn.feature_extraction.text import TfidfVectorizer

# corpus = ["文本一的內容", "文本二的內容", "文本三的內容"]
# vectorizer = TfidfVectorizer()
# tfidf_matrix = vectorizer.fit_transform(corpus)
```

### 📚 延伸
- [scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)

---

## 4.5 Naive Bayes 與 XGBoost 在文本分類的實戰

### 💡 思考
- Naive Bayes 為什麼在文本分類上表現不錯？
- XGBoost 在 NLP 任務中通常扮演什麼角色？
- 傳統 ML 分類器 vs 深度學習分類器的選擇時機？

### 📌 重點
- Naive Bayes 分類器：
- XGBoost：
- 模型評估指標：Precision / Recall / F1-Score
- 

### 🔧 實作
```python
# 來源：
# 用途：XGBoost 文本分類

# import xgboost as xgb
# from sklearn.metrics import classification_report

```

### 📚 延伸
- [XGBoost 官方文件](https://xgboost.readthedocs.io/)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：03_資料採集與前處理](03_資料採集與前處理.md) | [下一篇：05_情感分析 →](05_情感分析.md)
