---
title: DS-Study-Note-4 Metrics
date: 2022-04-26 22:28:19
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
description: "Metrics are used for model training and evaluation. It reveals a model's performance on a given dataset."
key_concepts:
  - Evaluation Metrics
  - Classification
series: Data Science
series_index: 4
takeaways:
  - Accuracy alone is misleading for imbalanced datasets; use precision, recall, and F1 instead
  - ROC curves plot true positive rate vs false positive rate; AUC summarizes overall classifier quality
  - Macro-F1 treats all classes equally while micro-F1 weights by class frequency
  - Cost curves help choose classifiers when different types of errors have different business costs
---

{% asset_img metric.png DS Study Note 4 cover: Machine Learning Evaluation Metrics %}

Metrics are used for model training and evaluation. It reveals a model's performance on a given dataset.
<!-- more -->
# Preliminary
We use:
-  $f$ to denote our model (function) 
- $D$ to denote the dataset used, $m$ as the sample it contains.

# Error rate
Defined as the number of **incorrectly** classified samples divide the number of total samples.
$$ E(f;D) = \frac{1}{m}\sum_{i=1}^m \mathbb{I}(f(x_i) \ne y_i)        $$
Similarly, the continuous form:
$$E(f;D) =\int_{x \sim D} \mathbb{I}(f(x_i) \ne y_i)p(x)dx   $$

# Accuracy
Defined as the number of **correctly** classified samples divide the number of total samples.
$$ acc(f;D) = 1 - E(f;D) = \frac{1}{m}\sum_{i=1}^m \mathbb{I}(f(x_i) = y_i)        $$
Similarly, the continuous form:
$$acc(f;D) = \int_{x \sim D} \mathbb{I}(f(x_i) = y_i)p(x)dx   $$

# Recall and Precision Rate
When the distribution of different classes are **NOT balanced**, we may be interested in how many samples of interest (positive samples) is found (**Recall Rate**) and  how many of the filter samples of interest are correct (**Precision Rate**). 

We use **TP / FP / TN / FN** to denote the frequency of **True Positive / False Positive / True Negative / False Negative**.

## Precision Rate
$$ P = \frac{TP}{TP + FP}  $$ (TP + FP stands for all the samples classified as **positive**)

## Recall Rate
$$ R = \frac{TP}{TP + FN} $$ (TP + FN stands for all the samples whose labels are **positive**)

## Tradeoff
- Pursuing Recall Rate and Precision Rate at the same time is often **contradictory**. 
- This is because a high Precision means that the model would be **cautious** as possible so that many positive samples with **lower confidence** would be classified as negative.

# PR Curve
In order to **unify** the Precision and Recall rate and compare the performance of different model, **PR Curve** is proposed.
1. The model is required to sort all the samples by the **confidence** (of **being positive** sample). 
2. Normally, for the first sample, the **Precision** would be 1 while the **Recall** would be the **minima** (close to 0).
3. Predict the current sample to be **positive**, **one-by-one**, in the sorted order and keep calculating the corresponding Precison and Recall Rate.
4. When all the samples are predicted to be positive, we have a **Recall** of 1 and the **Precision** reaches the **minima**.

## Break-Event Point of PR Curve
In order to compare the performance of two models, we can use the **area** under the PR curve as the metric. However, this value can be hard to calculate. 

Thus, we use the **Break-Event Point** to reach a balance between the Recall and Precision.
It is calculated by the **x-coordinate of the intersection point** of the **PR Curve** and function $y=x$.
Ideally, we want both the Precision and Recall to be **as high as possible**.
{% asset_img pr.jpg PR Curve showing the tradeoff between Precision and Recall rates %}


# F1-Score
**F1-Score** is a more commonly used metric to reach a balance between Precision and Recall, it is defined as the **Harmonic Mean** of these two:
$$ \frac{1}{F1} = \frac{1}{2} \times (\frac{1}{P} + \frac{1}{R}) $$

## Macro scope (Macro-F1)
1. For **N-class** classification problem, first calculates $N$ F1-Scores on $N$ **Confusion Matrix**.
2. Find the **arithmetic mean** of the $N$ F1-Scores.

## Micro scope (Micro-F1)
1. Find $N$ groups of $TP$, $FP$, $TN$, $FN$ and find the **arithmetic mean** for each of the four.
2. Calculate **F1-Score** with the **mean** $TP$, $FP$, $TN$, $FN$.

## Generalization
With the method describe above, you can similarly define **micro-P**, **macro-P**, **micro-R**, **macro-R**.

# Receiver Operating Characteristic (ROC) Curve
1. Similar to PR Curve, **sort** all the samples by the **confidence of predicting as positive**.
2. Find $$ TPR = \frac{TP}{TP + FN} $$, $$ FPR = \frac{FP}{TN + FP} $$.
These two values stand for the ratio of **correctly classified positive samples** and **incorrectly classified negative samples**.
3. For a **0-1 Classification** task, a model based on **random guess**'s ROC Curve should correspond to $y=x$ and an accuracy of $0.5$.

## Area Under ROC Curve (AUC)
- With **finite samples**, you can draw the coordinate $(TPR, FPR)$ for each point and find the **area** under the ROC Curve. 
- This is a common metric in **evaluating** models.

## Find a confidence threshold for ROC Curve
1. Set the threshold to $\inf$ which exceeds the confidence (score) of all the positive samples and they are all predicted as negative.
2. In this case, both the **TPR** and **FPR** equal $0$.
3. With the threshold goes down, these two would gradually raise to $1$.

## Define Sorting Loss based on AUC
- For each pair of positive-negative samples, if the positive sample achieves a score **lower than** the negative sample, add $1$ to the Loss. If equals, add $0.5$. 
- This corresponds to the area **above the ROC Curve** and thus should be **minimized**.
- $AUC = 1- L_{rank}$
- Similarly, we can assign **different weights** to different types of mistakes a classifer made and draw the **cost curve**. We can find the weighted sum and for each point, draw the curve of **expected cost** (line determined by $(0, FPR)$ and $(1, FNR)$. Then we find the lower bound of all such lines, the area under this curve stands for the cost.
{% asset_img cost.png Cost curve showing expected cost with weighted classification error %}