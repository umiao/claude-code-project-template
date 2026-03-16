---
title: DS-Study-Note-7 L1 & L2 Regularization
date: 2022-05-02 16:37:57
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
- Regularization
description: "The essence of L1 and L2 regularization (with corresponding L1 / L2 Norm): the projection of a vector to the domain of positive real number. They can both be..."
key_concepts:
  - Regularization
series: Data Science
series_index: 7
takeaways:
  - L1 regularization produces sparse models by driving parameters exactly to zero with constant gradient
  - L2 regularization shrinks parameters toward zero gradually but never reaches exactly zero
  - L1 may have multiple optimal solutions while L2 guarantees a unique optimum
  - The regularization strength hyperparameter controls the tradeoff between fitting data and model simplicity
---
The essence of L1 and L2 regularization (with corresponding L1 / L2 Norm): the **projection** of a vector to the domain of **positive** real number. They can both be viewed as metrics of distance.

{% asset_img reg.jpg DS Study Note 7 cover: L1 and L2 regularization %}

<!-- more -->
# Summary
1. L1 normalization would make many parameters become **zero** (equivalent of removing these parameters) due to the property of sparsification.
2. L2 normalization is easier to calculate and avoid the issue of discussion on the absolute value function.
3. Only one optimal prediction exists with L2 while multiple optimal solutions may exist with L2 (bacause of the non-linear point at $0$).

# Theory 
Whenever we apply **Gradient Descend** algorithm for parameter optimization, we need to find the gradient (derivative) and use the result for parameter update:
$$ \theta = \theta - \alpha \frac{\partial}{\partial \theta} J(\theta) $$
Here, $\theta$ stands for the model parameters, $\alpha$ stands for the learning rate and $J$ stands for the objective / loss function.
{% asset_img 2.jpg L1 and L2 norm functions and their derivatives for gradient descent %}
The function and derivative of L1 / L2 norm is shown in the above image. We can tell that $$ \frac{dL_1(w)}{dw} = sgn(w)  \\\\ \frac{dL_2(w)}{dw} =w $$

It is easy to find that, whenever the gradient is computed and used for update, the gradient of L1 function (if not equals zero), can only be $1$ or $-1$. Thus, for some parameters, they would head towards $0$ with steady pace (this is the cause of **sparsity**). 
However, for L2 function, the gradient's value would **vanish** when a certain parameter $w$ becomes closer to $0$. This means that with L2 regularization, some parameters may become close to $0$ but would never reach $0$.