---
title: DS-Study-Note-2 Bias VS Variance
date: 2022-04-23 00:41:01
categories:
- [Data Science, General Knowledge]
tags:
- DataScience
- Machine Learning
---
The target of Machine Learning is to fit an (unknown) distribution. There lies three possible error: bias, variance and irreducible error. 
<!-- more -->
{% asset_img var.jpg ML_note %}
>The irreducible error **CANNOT be avoided** with any algorithm as it can be viewed as the result of unknown factor, noise, accidents, etc. Thus, we would focus on the bias and variance error.
# Definition
1. **Bias** can be understood as the **accuracy** of the model, *i.e.*, the ability to estimate the output value **accurately**. 
2. **Variance** can be understood as the **stability** of the model, *i.e.*, the ability of resisting the noise and disturbance contained by the input. I also understood this ability as being able to recognize similar inputs and generate **similar** results for them.

# Example
- Applying **K-fold cross validation** can reduce the influence casted by the *outliers* and enhance the generalization ability, which reduces **the variance error**.
- At the same time, part of the data is not used for training, which impairs the model's fitting ability and increase the **bias error**. 
- An intuition is that, a more **complex** model is more **sensitive** to the noise contained by the input, which makes the output less stable (higher variance error). At the same time, a simpler model more easily *ignores* the random noise and difference of distribution between the training set and the testing set.

# Tradeoff and Analysis
The variance of the parameters you are estimating can be reduced, at the cost of increasing bias. If you would like to **generalize** a model trained on a certain training set, then you **CANNOT** minimize the *bias and variance error* at the same time. 

## Bias:
- Bias error comes from the **erroneous assumptions** of the learning algorithm.
- High bias error corresponds to **underfitting**.
- Bias error measures the **closeness** between the distribution you modeled and the **expectation** of the real distribution.
- Introduction of bias term in linear models aims at **simplying** the learning process without introducing way more complicated distribution which makes the model hard to generalize. At the same time, such models would fail to solve the more complicated models which do not meet the **assumption** (that this problem can be approximated by linear model).

## Variance:
- Variance error comes from the **noise / fluctuation / disturbance** of the training set.
- High variance error probably means that you are modeling on the random noise of the training set, which cannot be generalized, and this means **overfitting**.
- Variance error reveals the level of **concentration** of your model.






