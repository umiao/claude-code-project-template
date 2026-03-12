---
title: DS-Study-Note-1 Overfitting and Brief Introduction on Decomposition and Regularization
date: 2022-04-22 09:23:14
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
description: "Overfitting is a modeling error in statistics that occurs when a function is too closely aligned to a limited set of data points. ---- Definition ranked 1st ..."
key_concepts:
  - Overfitting
  - Regularization
series: Data Science
series_index: 1
takeaways:
  - Overfitting occurs when a model memorizes training data noise instead of learning general patterns
  - Common solutions include regularization, dropout, early stopping, and reducing model complexity
  - L1 regularization promotes sparsity by driving some weights to zero; L2 shrinks all weights evenly
  - Small datasets and distribution mismatch between train and test sets are primary overfitting causes
---

>Overfitting is a modeling error in statistics that occurs when a function is too closely aligned to a limited set of data points. ---- Definition ranked 1st in Google 
{% asset_img over.jpg DS Study Note 1 cover: Overfitting, Decomposition, and Regularization %}
<!-- more -->

# Definition


> Overfitting stands for making excessive learning steps on the training set, which results in the model extracting noise of the training set as valid pattern to fit the training set's distribution. In this case, the trained model would show low performance on the testing set and new data (real-world data).

# Possible Causes:
1. The volume of the training data is **too small**.
2. The data distribution of the training set data does **NOT** subject to the testing and real business data. This also means that the ***iid*** (identically and independent distributed) assumption is not satisfied.
3. There exists **noise** in the training set.
4. **Too many** iteration times.
5. Fail to learn **correct features** with ability of generalization and representative. 
6. The overfitting **MAY** be phenomenon of **information leakage**, *i.e.*, too complicated model remembers the training which makes the inference equivalent to the table look-up.


# Solutions:
1. **Discard** some features. This can be implemented by **Feature Selection** or simply **randomly discard** a subset.
> This process can be:
> - Conducted manually.
> - Randomly. (Random Forest)
> - Decided by Model Selection Algorithm. E.g., **PCA(Principal component analysis)**.
> - **PCA**: Solve the eigen-vector of the **covariance matrix**. It is obvious that the larger the covariance is, the more useful the corresponding eigen-value is. Find the **largest k** eigen-values and use their corresponding eigen-vectors to form a matrix as the **PCA output**. (You can also use **SVD** for such decomposition.)
> - You can also use dimensional reduction tools like **LR(lower–upper) decomposition**, **SVD(Singular Value Decomposition)**.
2. Introduce **regularization**.
3. Introduce **drop-out** layer when training network.
4. Use **Early-Stop** to achieve the tradeoff the generalization ability and convergence on the training set. (In this case, **evaluation set** is required for observation.)
5. A combination of methods above.
6. Adopt models like **Random Forest**.
7. Any method which is believed to be able to control the model's **complexity**. *E.g.*, control the depth, number of trees.

# Selection Bewteen the L1 and L2 Regularization Term
1. L1 - LASSO (Least Absolute Shrinkage and Selection Operator): cast penalty on the **sum of the absolute value** of the model parameters.
Regularize all the parameters **equally**. Able to transform some parameters into 0. (make the model **sparse**)
$${L1}\_{reg} = \lambda \sum_{j=1}^p |\beta _j|$$
2. L2 - Ridge Regression: cast penalty on the **sum of the square value** of the model parameters.
$${L2}\_{reg} = \lambda \sum_{j=1}^p \beta _j^2$$


In essence, these two regularization method is to conduct L1 / L2 Normalization on the model parameters and add the normalized term to the **Loss Function** for optimization.
***




