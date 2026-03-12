---
title: DS-Study-Note-8 Random Forest
date: 2022-05-03 22:48:16
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
- Random Forest
description: "Random Forest inherits the idea of bagging, which is part of Ensemble Learning paradigm."
---

Random Forest inherits the idea of **bagging**, which is part of **Ensemble Learning** paradigm.
<!-- more -->

{% asset_img rf.png DS Study Note 8 cover: Random Forest and ensemble learning %}
# Introduction to Ensemble Learning
1. It can be simply categorized into **Boosting**, **Bagging** and **Stacking**.
2. **Stacking**: use **Logistics Regression** to integrate multiple prediction results and output one single prediction. It can be viewed as a more complicated form of **voting** (most commonly appeared in classification tasks, take the result with most votes).
3. **Bagging** and **Boosting** both somehow combine existing classification / regression methods to form a stronger classifier (utilize some sort of **group intelligence**). The difference lies in the combining method.

## Bagging
Also known as **Bootstrap aggregating**. 
### Procedure
The idea is to :
	1. sample $n$ data samples with bootstraping method (**sample with replacement**) from the dataset, to form $k$ training sample sets by repeating $k$ times. That is to say, some samples can be contained in multiple training sample sets, while some samples may not be contained by any training sample sets.
	2. We can tell that the $k$ training sets are **independent** with each other.
	3. Execute learning algorithm on the $k$ training sets to achieve $k$ models.
	4. Receive the classification  / regression results by integrating the $k$ outputs of these models (with voting / averaging).

- **Characteristics**: 
	1. Highly Parallelizable.
	2. The generated models are highly independent with each other.
	3. All the models have the same significance (equally important).
- **Representative Work**: *Random Forest*

## Boosting
The idea is to combine multiple 'weak' classifiers to form only **ONE** 'strong' classifier to generate **ONE** prediction, rather generating and processing $k$ individual predictions. 
- This method runs under the **Approximately Correct (PAC)** framework. This theory supports that you are bound to leverage multiple weak classifiers into a stronger one.
### Implementation
1. In each round, the **weight distribution** of the  training data would be altered. The weight of samples which are **falsely** classified would **increase** while the weight of the **correctly** classified samples would be **reduced** to accelerate the iteration / convergence. 
2. **Different ways of combining the weak classifiers**: 
	- Use **additive model** to generate a **linear combination**.
	- **AdaBoost**: Through the **weighted majority voting** method, the weight of classifiers with less error rate would be increased. Weight of classifiers with high error rate would decrease.
	- **Boosting Tree**: The classifers establish series connection and each classifier fits the **residual** of the prior one. Use the **additive sum** of **all** the classifiers as the predicted value.

- **Representative Work**: *GBDT / XGBoost*

## Summary on Bagging and Boosting
- **Bagging**: 
	1. would generate multiple training sets with **replacement**. 
	2. Each sample / classifier has **the same** weight. 
	3. Can be easily **Parallelization**.
- **Boosting**: 
	1. would not modify the training set but the samples' weight. 
	2. The weight of each sample / classifier would be **changed** according to error rate. 
	3. The training of classifiers should be in **sequential** order.

### Model setup / combination
1. Bagging + Decision Tree = **Random Forest**
2. AdaBoost + Decision Tree = **Boosting Tree**
3. Gradient Boosting + Decision Tree = **Gradient Boosted Decision Trees (GBDT)**

# Decision Tree
## How it is built
- General description: 
	1. Randomly sample from the dataset to train decision tree. 
	(First select $N$ samples to train a decision tree which is to be placed at the **root** node)
	2. Randomly select attribute (feature) used for training. 
	(If the data has $M$ attributes, then randomly select a subset with size of $m$)
	3. Decide the attribute used for node splitting. 
	(Use some metirc (**information gain**, **gini impurity**) to select one attribute as the splitting attribute of this node)
	4. Repeat such process untill reach the preset boundary 
	(Unable to split / reach required depth).
	(If the selected splitting attribute is already used by the father node, it also indicates that we have reached the **leaf node** and no further splitting is required)
	5. Build massive Decision Trees to form a forest.

# Pros and Cons
## Advantages
1. Able to process data with high dimensions without **dimensional reduction** and **feature selection**.
2. Indicates the **importance** and **correlation** between features.
3. Resist **overfitting**.
4. High training speed, easy to **parallelize**.
5. Easy to implement.
6. Able to alleviate the **imbalance** in dataset distribution.
7. Able to resist **missing data** partially.
## Disadvantages
1. Overfitting on some regression and classification tasks with high noise volumn.
2. In favor of attributes with more possible ways of splitting (in discrete cases). 
With more **choices of splitting** / more **unique values**, an attribute can cast greater impact on the Random Forest classifier, making the result unreliable.












