---
title: DS-Study-Note-3 Dimension Curse
date: 2022-04-26 15:19:27
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
description: "Dimension curse stands for the troubles you would meet when processing high-dimensional data. E.g., computation of similarity, distance, neighbour or any met..."
key_concepts:
  - Curse of Dimensionality
  - Dimensionality Reduction
series: Data Science
series_index: 3
takeaways:
  - In high-dimensional spaces distances between points converge making similarity metrics unreliable
  - The number of samples needed grows exponentially with dimensions (combinatorial explosion)
  - Hubness causes certain points to become nearest neighbors of disproportionately many others
  - Dimensionality reduction techniques like PCA and CNNs mitigate the curse at the cost of interpretability
---

<!-- {% asset_img over.png DS Study Note 3 cover: Curse of Dimensionality %} -->
# Definition 
**Dimension curse** stands for the troubles you would meet when processing **high-dimensional** data. *E.g.*, computation of **similarity, distance, neighbour or any metric based processing.**
<!-- more -->
The reason is that for **high-dimensional** space, the concept of distance will gradually **fail**, and even make any two points **infinitely inseparable**, even if they look different / correspond to very different categories.

As the dimension (of vector representation) grows, the data becomes more and more **sparse** and may correspond to higher variance and bias error. These phenomena are essentially caused by the same theory. However, the theoretical derivation is omitted here.

>Specifically, **dimension curse** can be categorized into the following more concrete problems: 
> 1. Distance concentration
> 2. Combinational explosion
> 3. Hubness

# Distance concentration
- As the number of dimension raises, for the queried point, the distance to its **closest neighbour** would converge to the distance to the **furthest point**. This also means that the ***difference of distance*** between **arbitrary** two points would be **negligible**.
- The difference of distance may be small enough, for a dimension of **20**.
- The distance may remain **effective**, if there lies **inherent clusters** in the data and these clusters are **distant** from each other. Or, if many of the data's dimensions are **redundant** (the data can be embedded into a space with much smaller dimension).
- In high-dimensional space, small change of the **neighbourhood radius** determines the difference of selecting only **ONE** point or selecting **ALL** the datapoints. 
- This is because the **volume ratio** of a **fixed radius** hypersphere to a unit radius hypersphere will be close to **1**.
- Increase of **relevant features** would be **beneficial** to the model. 
- Increase of **irrelevant features** would **impair** the model's performance.
- Distance under *different dimension and space* **CANNOT** be compared with each other.

# Combinational explosion
{% asset_img dif.jpg Combinational explosion: search space growing exponentially with dimension %}
- As the dimensionality increases, a larger percentage of the training data resides in the **corners** of the feature space. 
- It is also much more difficult to traverse the increasing search space as the size of the search space **grows exponentially**, as shown in the above image.
- A complex search space may correspond to the same configuration (object / training / testing sample) in the low-dimensional case, resulting in **overfitting**.
- Training samples with **larger scale** are required to suppress **overfitting** (on data with **high dimensions**). 
- Algorithms like **Random Forest** can restrict the number of features used (in one tree).

# Hubness
- With the increase of dimension, a handful of points are **significantly more frequent** to become the **nearest neighbour** of other points. This is also called **Hubness**.
- If we record the frequency of each point becoming the **nearest neighbour** of another point, we can find that is frequency follows Zipf's Law and is **right-skewed** heavily.
- Generally, points close to the **mean value** of the entire dataset become hubs more easily.
- When **cluster** exists, data points close to the **mean value** of the cluster are more likely to become hubs as well.

# Outlier / Anti-hubs
- These points are most **distant** from the majority of other points.
- Anti-intuitive things may happen, i.e., hubs exist in the **low-density region** of the high-dimensional space, but the hubs are **close** to the other points. 
- At the same time, anti-hubs may exist in the **high-density region** of the high-dimensional space, but the anti-hubs are **distant** to the other points (which makes them outliers).
- This can be viewed as a mismatch between the **probabilistic density** and **distance distribution**. 

# Solution (to dimension curse)
1. For the cases of **Multicollinearity** and **Duplication of Components**(redundancy) happen, we can simply **remove** the redundant variables after evaluation.
2. In the case when each dimension (feature) contributes **equally** to the model's result, methods like **Dimensional Reduction** (including **CNN**, **Convolutional Neural Network**) can be applied.
3. Dimensional Reduction's **Disadvantages**: 
	- Converted data points **DO NOT** represent **original features**.
	- **Less interpretable, hard to visualize, weaker theoretical support**.


***
