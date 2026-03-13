---
title: "NLP 基礎 — 機器學習核心算法與機率模型"
date: 2026-03-09
day: Day1-Day2
tags: [NLP, ML, Day1, Day2]
status: todo
chapter: "§3, §4"
---

# 02 — NLP 基礎：機器學習核心算法與機率模型

> tags: #NLP #ML #Day1 #Day2 #todo
> 對應課程章節：§3 機器學習速成 + §4 機率生成模型與分類模型

---

## 2.1 決策樹 (Decision Tree) 在 NLP 的應用

### 💡 思考
- 決策樹如何用於文本分類？其優勢與限制？
- 在 NLP 場景中，決策樹的特徵通常是什麼？
- 過擬合 (Overfitting) 在文本分類中如何表現？

### 📌 重點
- 決策樹原理：
- 特徵選擇：
- 剪枝策略：
- 

### 🔧 實作
```python
# 來源：
# 用途：決策樹文本分類

from sklearn.tree import DecisionTreeClassifier

```

### 📚 延伸
- [scikit-learn DecisionTree](https://scikit-learn.org/stable/modules/tree.html)

---

## 2.2 隨機森林 (Random Forest) 在 NLP 的應用

### 💡 思考
- Random Forest 相比單一決策樹的優勢？
- Bagging 策略如何提升文本分類的穩定性？

### 📌 重點
- 隨機森林原理：
- Bagging 策略：
- 特徵重要性排序：
- 

### 🔧 實作
```python
# 來源：
# 用途：隨機森林文本分類

from sklearn.ensemble import RandomForestClassifier

```

### 📚 延伸
- [scikit-learn RandomForest](https://scikit-learn.org/stable/modules/ensemble.html#random-forests)

---

## 2.3 梯度下降 (Gradient Descent) 最佳化策略

### 💡 思考
- SGD、Mini-batch GD、Adam 各自的適用場景？
- Learning Rate 的選擇對 NLP 模型訓練有什麼影響？
- 為什麼深度學習中 Adam 優化器最為普及？

### 📌 重點
- Gradient Descent 原理：
- SGD vs Adam：
- Learning Rate 調整策略：
- 

### 🔧 實作
```python
# 來源：
# 用途：梯度下降視覺化 / 不同優化器比較

```

### 📚 延伸
- [An overview of gradient descent optimization algorithms](https://ruder.io/optimizing-gradient-descent/)

---

## 2.4 貝氏分類 (Bayesian Classification) 在中文語意分析的應用

### 💡 思考
- 貝氏定理在文本分類中如何運作？
- Naive Bayes 的「Naive」假設在中文文本上合理嗎？
- 中文語意分析與英文的差異有哪些？

### 📌 重點
- 貝氏定理：$P(A|B) = \frac{P(B|A) \cdot P(A)}{P(B)}$
- Naive Bayes 假設：
- 中文應用考量：
- 

### 🔧 實作
```python
# 來源：
# 用途：Naive Bayes 中文文本分類

from sklearn.naive_bayes import MultinomialNB

```

### 📚 延伸
- [scikit-learn Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)

---

## 2.5 HMM（隱馬爾可夫模型）與 Transformer 的對比

### 💡 思考
- HMM 在 NLP 中的經典應用場景（如 POS tagging）？
- 為什麼 Transformer 能取代 HMM 和 RNN？
- Self-Attention 相比 HMM 的狀態轉移有何優勢？

### 📌 重點
- HMM 模型：
- Transformer 架構：
- 兩者比較：

| 特性 | HMM | Transformer |
|---|---|---|
| 序列建模 | | |
| 長距離依賴 | | |
| 平行運算 | | |
| 訓練效率 | | |

### 🔧 實作
```python
# 來源：
# 用途：HMM vs Transformer 對比實驗

```

### 📚 延伸
- [Hidden Markov Models 教學](https://web.stanford.edu/~jurafsky/slp3/A.pdf)

---

## 課堂筆記（自由記錄區）



---

> [⬅️ 上一篇：01_課程總覽](01_課程總覽.md) | [下一篇：03_資料採集與前處理 →](03_資料採集與前處理.md)
