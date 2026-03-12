---
title: DS-Study-Note-9 Gradient Boosting Machine Tree Model(s)
date: 2022-05-25 19:54:23
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
- GBM
- XGBoost
description: "Study notes on Gradient Boosting Machine Tree models including GBM and XGBoost algorithms."
key_concepts:
  - Gradient Boosting
  - Ensemble Methods
series: Data Science
series_index: 9
takeaways:
  - GBM fits each new tree to the negative gradient (residuals) of the loss function from previous iterations
  - XGBoost improves on GBM with second-order Taylor expansion, regularization, and parallel block processing
  - LightGBM uses leaf-wise growth and histogram binning for faster training on large datasets
  - Boosting is more prone to overfitting than bagging but typically achieves higher accuracy when tuned well
---

# Gradient Boosting Machine Tree
**GBMTree** stands for **Gradient Boosting Machine Tree**.
<!-- more -->
The idea is to train multiple serial **weak** learner, while the objective of each learner is to fit the **negative** gradient of the loss function of the previous cumulative model. 
Thus, after this weak learner is attached, the loss of the new cumulative model shall be maximally reduced. Also, each base (weak) learner can be linearly combined with different weights (so that those learners with higher performance would contribute more to the result). A common implementation of the base learner is Tree Model (*e.g.*, Decision Tree).

{% asset_img theory.jpg DS Study Note 9 cover: Gradient Boosting Machine Tree theory %}

# Primary Feature
The primary feature of GBM (Gradient Bossting Machine) is that, it conduct **Gradient Descent** in the space of function, instead of the space of model parameters (e.g., Neural Network calculates the gradient of current loss to the model parameters for update).

In Gradient Boosting, in each iteration, a weak learner is generated via **fitting the negative gradient** of loss function to the cumulative model formed by the learners generated before (this means that the previous model is left **unchanged**). Then, the current weak learner is added to the cumulative model to reduce the loss.

**Differences**:
- Gradient descent of the **parameter space** would: use the gradient to update the parameters
- Gradient descent of the **function space** would: fit a new function with the gradient

# Math Theory
Considering we have $n$ training samples $\\{x_i, y_i\\}$, and the cumulative model in the $k$th round is $F_{k-1}(x)$. Then, the model in the kth round should be:
$$ F_k(x) = F_{k-1}(x) + arg \min_{h \subset H} Loss(y_i, F_{k-1}(x_i) + h(x_i))   $$
where $h(x)$ is the desired weak learner.

In fact, after the $k-1$th round, we can have $\hat y = F_{k-1}(x)$ and the loss $Loss(y, \hat y)$. Thus, in order to minimize the model's loss after introducing the $k$th weak learner, the gradient of this learner $h(x)$ should be negative to the gradient of $F_{k-1}(x)$, so that:
$$ Gradient \\  h(x) = - \frac{\partial Loss(y, \hat y)}{\partial F_{k-1}(x)} $$ 

In the actual implementation of this algorithm, a concrete **loss function** and a **learning rate** $\alpha$ should be appointed. The learning rate would be used when updating the model: $F_k(x) = F_{k-1}(x) + \alpha h(x)$.
We also need to set a boundary condition (number of iteration, minimal improvement / difference, etc) to decide when to terminate this algorithm.

# GBDT (Gradient Boosting Decision Tree) Algorithm
**GBDT** uses **CART (Classifier And Regression Tree)** as the weak learner.
The benefit of such design is that, the Decision Tree itself is unstable, as minor fluctuation of training data can greatly influence the (inference) result (single Decision Tree has **high variance**).

In **Ensemble Learning**, we expect weak classifiers to have **high variance** to achieve **better generalization performance**. Thus, CART is preferred to the more stable weak learners (*e.g.*, linear regression).

# Implementation
- In **regression task**, the loss function would be ${(y - F_{k-1}(x))}^2$, then the negative gradient would be $2(y - F_{k-1}(x))$.
Thus, we can find the negative gradient simply via $y - F_{k-1}(x)$.

- In **classification task**, we aims at fitting the logarithmic probability $\log \frac{p}{1-p}$ with linear model $Wx+b$. The loss function would be **Cross Entropy Loss**: $Loss = -y \log p - (1-y)log(1-p)$. Then, we can have
$$ F_{k-1}(x) = \log\frac{p_{k-1}}{1-p_{k-1}} \Rightarrow p_{k-1} = \frac{1}{1 + e^{-F_{k-1}}}  $$
$$ Loss = -y\log \frac{1}{1 + e^{-F_{k-1}}} - (1-y)\log \frac{e^{-F_{k-1}}}{1 + e^{-F_{k-1}}} $$

	Simplify the expression, we have $Loss = (1-y)F_{k-1} + \log(1 + e^{-F_{k-1}})$. $-\frac{\partial Loss}{\partial F_{k-1}} = y - p_{k-1}$

# XGBoost
**XGBoost** stands for **eXtreme Gradient Boosting**, which is an algorithm based on **GBDT**. It makes multiple improments, including:
1. Apply **second-order Taylor Formula Expansion** to better approximate various loss functions (and faster convergence).
2. Introduce **regularization term** to prevent overfitting.
3. Use **Block** to store the structure for parallel processing

## Math Theory
The objective function of XGBoost consists of **loss function** and **regularization term**.
The objective function can be written as:
$$ Loss = \sum_{i=1}^n l(y_i, \hat y_i) + \sum_{k=1}^K \Omega(f_k) $$
We have $n$ pairs of training samples and a total of $K$ trees. $\Omega(f_k)$ is the regularization term which measures the model's complexity.

Since XGB is implemented by Boosting, we also have: $\hat y_i^t = \hat y_i^{t-1} + f_t(x_i)$. Here $f_t(x_i)$ is the most recently appended weak learner.

### Taylor Expansion
We already know that $f(x) \approx f(x_0) + f'(x_0)(x - x_0) + \frac{f''(x_0)}{2}(x - x_0)^2$.
Then, let $l(x) = l(y_i, x)$, find the 2nd order Taylor Expansion at $x_0$, we can have $l(y_i, x) \approx l(y_i, x_0) + l'(y_i, x_0)(x - x_0) + \frac{l''(y_i, x_0)}{2}(x - x_0)^2$.
Similarly, we have $l(y_i, x) \approx l(y_i, \hat y_i^{t-1}) + l'(y_i, \hat y_i^{t-1})(x - \hat y_i^{t-1}) + \frac{l''(y_i, \hat y_i^{t-1})}{2}(x - \hat y_i^{t-1})^2$.

Note that we have $x = \hat y_i^{t-1} + f_t(x_i)$, denote $g_i = l'(y_i, \hat y_i^{t-1})$, $h_i = l''(y_i, \hat y_i^{t-1})$, we have:
$$ l(y_i, \hat y_i^{t-1} + f_t(x_i)) \approx  l(y_i, \hat y_i^{t-1}) + g_if_t(x_i) + \frac{h_i}{2}f_t^2(x_i)$$
Here we finish the derivation.

### Unfold regularization term
Note that $l(y_i, \hat y_i^{t-1})$ is a constant, we can simply remove it. Also, we unfold the regularization term $\sum_{k=1}^K \Omega(f_k) = \Omega(f_t) + \sum_{k=1}^{t-1}\Omega(f_k)$. The structure of the previous $t-1$ trees would not change, thus we can view their sum as a constant and remove, to have the polished loss function:
$$ {Loss}^t = \sum_i^n[g_if_t(x_i) + \frac{h_i}{2}f_t^2(x_i)] + \Omega(f_t) $$

### Organize the objective function
1. In order to define a Tree, we need the leave nodes' **weight vector** $\omega \subset R^T$ and the **mapping relationship** $q: R^d \rightarrow 1,2,...,T$, T is the number of the leave nodes. Thus, we can express a tree as $f_t(x) = \omega_{q(x)}$.

2. We then define the complexity, *i.e.*, $\Omega$. We define it by: the number of the leave nodes $T$, and the **L2 Norm** of the weight vectors of the leave nodes. Thus, we define $\Omega(f_t) = \gamma T + \frac{1}{2}\lambda\sum_{j=1}^T\omega_j^2$.

3. Merge the terms according to their order: 
	$$ {Loss}^{(t)} = \sum_{j=1}^T[(\sum_{i \in I_j}g_i)w_j + \frac{1}{2}(\sum_{i \in I_j}h_i + \lambda)w_j^2] + \gamma T$$
	We can denote $G_j = (\sum_{i \in I_j}g_i)$ and $H_j = \sum_{i \in I_j}h_i$, these two stands for sum of the 1 / 2 - order partial derivative of the samples contained by leave node $j$. Note that $G_j$, $H_j$ are constants.

### Optimal Solution
We can tell that the objective function $f(w_j) = G_jw_j + \frac{1}{2}(H_j + \lambda) w_j^2$ is a 2nd-order function about $w_j$. Thus, we can tell that the minial ($f(w_j) = -\frac{G_j^2}{2(H_j + \lambda)}$) is reached at $w_j = - \frac{G_j}{H_j + \lambda}$.

# LightGBM

## Motivation
1. Reduce the occupancy of memory. Utilize as much as possible data on single machine, without sacrificing the speed.
2. Reduce the overhead of communication, realize linear acceleration in case of Multiprocessor parallel.

## Difference from XGBoost
1. These two alogrithms both use the negative gradient of the loss function as the approximation of the residual of current decision tree, to fit the new decision tree.
2. LightGBM would grow in the vertical direction, and other algorithms would grow in the horizontal direction.
3. LightGBM would grow in the leave node with maximal error, to reduce loss as possible.

## Histogram Algorithm
**Histogram Algorithm** is proposed to substitute the **pre-sorted algorithm** of **XGBoost**. The pre-sorted algorithm would first sort the samples according to their feature values, then find the optimal split point from all the possible feature values. Thus, for each feature, the number of candidate split points is proportional to the **number of samples**.

At the same time, **Histogram Algorithm** would discretize the continuous feature values into a constant number (*e.g.*, 255) of bins. Thus, the candidate split points would reduce to **(num_bins - 1)** from **(num_unique_values - 1)**.
{% asset_img hist.png LightGBM histogram algorithm discretizing feature values into bins %}

With this manner, instead of storing the feature values with `float_32`, we can now use `uint_8` to store the index of bucket (with hash algorithm). At the same time, there comes the tradeoff of **losing accuracy** to **raise efficiency** 
- (However, single Decision Tree itself is a weak model, it is not that important for the split points to be accurate. Coarse split points may have the **regularization** effect and the result can **stay robust** under Gradient Boosting framework.).
### Acceleration of Histogram via finding difference
The histogram of a leaf can be found by solving the difference of its father node's histogram and its brother's histogram. **LightGBM** can solve the histogram of a leaf node (with small sample number) and quickly find the histogram of its brother.
{% asset_img hist2.jpg LightGBM histogram acceleration via difference of sibling leaf histograms %}

It should be noted that **XGB** and **LightGBM** only consider non-zero values.

### Leaf-wise Algorithm with Depth Limit

Most GBDT algorithms use the **level-wise** grow strategy, *i.e.*, all the leave nodes in the same level would be splitted, under a single traverse (then **post-pruning** would be executed). It is friendly for multi-thread optimization, controlling of model complexity and resist over-fitting. However, for many leaves, the **split gain** is very **low** and result in useless computational overhead. 

LightGBM uses the **leaf-wise** grow strategy. At a time, a leaf with **max split gain** is selected and splitted. Thus, with the same number of splition, we can come up with better accuracy and lower error. However, it also has the advantage of possibility of **overfitting**, as a deep decision tree may be generated. Thus, a `max_depth` is introduced to control the depth of a tree.

## GOSS - Gradient Based One-Side Sampling
**GOSS** aims at omitting most of the samples with **small gradient** and only use the remaining samples to compute the information gain. (We assume that the samples with smaller gradients are already **well-trained**.)

However, simply dropping the data with small gradient would change the overall distribution of dataset. Thus, **GOSS** would sort all the possible values of the feature to be splitted order by the absolute value and select the $k$-largest ones. Then, $m-k$ samples and randomly selected from the remaining ones (and assigned with a constant $fact$ to scale the samples with small gradient).


## EFB - Exclusive Feature Bundling
High-dimensional data is usually **sparse**. Such sparsity inspires us to develop a **lossless** method to reduce the dimension of features. If two features are **exclusive**, it means that their feature would not be non-zero values at the same time. Then, we can simply find the sum of these two (**Bundling**), without losing information. If they are not completely exclusive, we can measure the **conflict ratio** (ratio of having non-zero values at the same time) of a pair of features. If **conflict ratio** is small, we can still bundle them without impair the final accuracy.

**Exclusive Feature Bundling, EFB** points out that if we conduct fusion and bundling on some features, we can reduce the number of features for better performance.

### Decide which features to bundle
Bundling **pair-wise independent** features is a **NP-Hard** problem. The **EFB** algorithm of **LightGBM** reduces this problem into **Graph Coloring Algorithm**. Each feature would be viewed as a **vertex** of the graph, and we draw an **edge** between two features which are **NOT completely independent** and the **weight** of the edge is the **conflict ratio** of these two features. Then our task is to color the vertices to be bundled in the same color.

- The **heuristic** alogrithm is like: **Construct** such a graph, **sort** the vertices by the degree (larger degree means higher degree of conflict). **Traverse** each vertex (feature), allocate it to one of the existing feature bundles or create a new one, to minimize the total conflict.
- When the scale of data is very large, the efficency of graph operation would get too low. **LightGBM** proposes a **non-graph algorithm**, which sort the features by the number of **non-zero values**.

### Implement the bundling
We can distribute values of different features into **different bins** of a bundle (in order to make sure the values of raw features are **recognizable before bundling**, by adding a **shifting constant** to the feature value).




## Summary
It is not recommended to use LightGBM on small dataset as it is **sensitive to overfitting**. (Recommend to use LightGBM on dataset with a size larger than 10K)

### Categorical Feature
It should be noted that, **one-hot encoding** is not recommended for **Decision Tree** (especially when the number of classes is large).
1. The split would be **imbalanced**, which results in **very small splitting gain**. Using one-hot encoding means that on each decision node, we can only use **one vs rest** splitting (*e.g.*, decide a sample is dog or not). It is almost equivalent to not splitting at all.
2. One-hot encoding would cut samples of the same class into many **small subspaces / groups** (statistics on small space may be **inaccurate**). **LightGBM** use **many-to-many** to solve this issue (*e.g.*, a single node is $X = A || X = C$).

**Acceleration method**: Before traverse all the candidate splitting points, first sort the histogram by the mean value of the corresponding labels, then search the optimal splitting point according to the order. This method can easily **overfitting**, so it needs further **constraints** and **regularization**.

### Source Code

When running in parallel, **LightGBM** would store all the training data in each node (server) to save the communication cost (instead of dividing the data vertically and distributing to each node). LightGBM would also use **Reduce Scatter** to distribute the task of merging the histogram. Finally, it applies parallizing based on **voting** (only the **Top K** features of **each node** would be considered and merged). Also, the histogram algorithm **LightGBM** applied is naturally more friendly to **Cache**, because it reduce the **random access** and do not need a data structure to store the mapping of **row indexes to leave indexes**.

Recommended web for source code studying: https://mp.weixin.qq.com/s/XxFHmxV4_iDq8ksFuZM02w


# Summary on Bagging and Boosting
1. **Sample Selection**: 
	**Bagging**: sampling with replacement, different training sets are independent from each other
	**Boosting**: The training set remains unchanged, only the weight of each sample alters (decided by the performance of last round).

2. **Weight of sample**:
	**Bagging**: Each sample has the same weight.
	**Boosting**: Weight decided by the error rate (higher error rate corresponds to higher weight).

3. **Weight of learner**:
	**Bagging**: Each learner has the same weight.
	**Boosting**: Each weak learner has different weight (more accurate one has higher weight).
4. **Parallel computing**:
	**Bagging**: Able to parallel.
	**Boosting**: Each learner should be generated in sequential order.

5. **Essence**:
	**Bagging**: Reduce variance (via voting).
	**Boosting**: Reduce bias.
