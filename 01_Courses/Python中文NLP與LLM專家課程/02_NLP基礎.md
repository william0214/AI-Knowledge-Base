---
title: "NLP 基礎 — 機器學習核心算法與機率模型"
date: 2026-03-09
day: Day1-Day2
tags: [NLP, ML, Day1, Day2]
status: in-progress
chapter: "§3, §4"
---

# 02 — NLP 基礎：機器學習核心算法與機率模型

> tags: #NLP #ML #Day1 #Day2 #in-progress
> 對應課程章節：§3 機器學習速成 + §4 機率生成模型與分類模型
> 原始講義：[PNLP上課筆記_2026-03-09.pdf](assets/PNLP上課筆記_2026-03-09.pdf)
> 主要來源頁碼：24–31, 36–37

---

## 2.1 文本分類的基礎模型路線

### 💡 思考
- 為什麼課程同時涵蓋 Naive Bayes、SVM、XGBoost、RNN 與 BERT？
- 企業專案中，baseline 為什麼通常不是直接從大型模型開始？

### 📌 重點
- 課堂實務流程反映典型 NLP 專案做法：
  - 先用 TF-IDF + 傳統分類器做 baseline。
  - 再導入 RNN 或 BERT 做效果提升。
- 經典模型重點在低成本、快迭代、可解釋；深度模型重點在語境理解與更高上限。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 24-31 頁
# 用途：保存文本分類模型光譜

model_spectrum = {
	"traditional": ["Naive Bayes", "Logistic Regression", "SVM", "XGBoost"],
	"deep_learning": ["RNN", "BERT"],
}
```

### 📚 延伸
- [scikit-learn](https://scikit-learn.org/stable/)
- [Transformers](https://huggingface.co/docs/transformers/)

---

## 2.2 Naive Bayes、SVM 與 XGBoost 的角色分工

### 💡 思考
- 為什麼 Naive Bayes 對 TF-IDF 特徵常常表現不差？
- SVM 與 XGBoost 各自適合什麼任務邊界？

### 📌 重點
- Naive Bayes：適合稀疏高維特徵，是文本分類最常見 baseline 之一。
- SVM：在中小型文本分類任務中穩定，常與 TF-IDF 搭配。
- XGBoost：適合拿來做更強的表格化特徵分類比較，或混合多種特徵。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 25, 29, 31 頁
# 用途：傳統分類 baseline 依賴

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC

# import xgboost as xgb
```

### 📚 延伸
- [Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- [LinearSVC](https://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html)

---

## 2.3 梯度下降、RNN 與 BERT 的訓練觀念

### 💡 思考
- 深度模型和傳統模型最大的訓練差異在哪裡？
- `max_len`、batch size、validation split 為什麼在 BERT 任務中特別重要？

### 📌 重點
- RNN 與 BERT 都依賴梯度下降類最佳化器。
- 課堂中 BERT 訓練重點包含：載入資料、切分訓練驗證集、決定 `max_len`、建立 Dataset / Dataloader、訓練與未見資料評估。
- RNN 課程則強調 K-Fold、Save / Load 與 Fine-Tuning。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 28-29, 36-37 頁
# 用途：深度文本分類訓練流程索引

deep_training_steps = [
	"load_dataset",
	"prepare_train_valid_split",
	"decide_max_len",
	"build_dataset_and_dataloader",
	"train_model",
	"evaluate_on_unseen_data",
]
```

### 📚 延伸
- [Adam optimizer](https://pytorch.org/docs/stable/generated/torch.optim.Adam.html)
- [PyTorch DataLoader](https://pytorch.org/docs/stable/data.html)

---

## 2.4 Multi-Class 與 Multi-Label 問題定義

### 💡 思考
- 一筆資料只能有一個標籤，和可同時擁有多個標籤，在標註與評估上差異多大？
- 哪些企業文本任務更符合 multi-label？

### 📌 重點
- Multi-Class：一筆資料只屬於單一類別。
- Multi-Label：一筆資料可同時屬於多個類別。
- 課堂中的說明例子包含垃圾郵件判斷、正中負情感分類、新聞多主題標註與電影多類型標註。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 30 頁
# 用途：分類問題定義範例

classification_tasks = {
	"multi_class": ["spam detection", "sentiment 3-way classification"],
	"multi_label": ["news topic tagging", "movie genre tagging"],
}
```

### 📚 延伸
- [Multiclass and multilabel algorithms](https://scikit-learn.org/stable/modules/multiclass.html)

---

## 2.5 從傳統 NLP 到 Transformer 的演進脈絡

### 💡 思考
- 為什麼這門課沒有直接從 LLM 開始，而是先經過 TF-IDF、Bayes、RNN？
- Transformer 相對前代模型，真正改變了什麼？

### 📌 重點
- 傳統 NLP 方法擅長快速建立可解釋 baseline。
- RNN 引入序列建模，但在長距依賴與平行化上有限制。
- BERT / Transformer 讓上下文表示能力大幅提升，成為後續 RAG 與 Agent 的技術基礎。

### 🔧 實作
```python
# 來源：課程講義 PDF 第 17, 24-29, 36-38 頁
# 用途：保存模型演進順序

evolution_path = [
	"Bag of Words / TF-IDF",
	"Naive Bayes / SVM / XGBoost",
	"RNN / LSTM",
	"BERT / Transformer",
	"RAG / Agent / Fine-tuning",
]
```

### 📚 延伸
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：01_課程總覽](01_課程總覽.md) | [下一篇：03_資料採集與前處理 →](03_資料採集與前處理.md)
