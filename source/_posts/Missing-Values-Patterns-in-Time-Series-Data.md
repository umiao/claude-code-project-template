---
title: Missing Values Patterns in Time Series Data
date: 2022-05-01 20:36:26
categories:
- [UCLA, Course Study, ECE209 in 2022 spring]
tags: 
- UCLA 
- Data Science
description: "It is meaningful and believed to be possible to discover the pattern of the missing parts of the time series data. Such patterns may vary in different scenar..."
---

It is meaningful and believed to be possible to discover the pattern of the missing parts of the time series data. Such patterns may vary in different scenarios and sources and may be related with physical devices and configurations.
<!-- more -->
# Algorithms for pattern detection 
{% asset_img img.jpg Distribution comparison of imputed values versus known patterns in time series %}
In the above image, we can find out the distribution and comparison between the imputed values VS the known patterns.


A pipeline of missing data pattern detecting is proposed in this paper.[<sup>1</sup>](#1)

> 1. Create base matrices to represent data. 
> 2. An algorithm to quantify and categorize missing values slots. 
> 3. Evaluate the frequencies of time attributes to determinate the most crucial time scenarios to analyze. 
> 4. Use this time attributes to find patterns over classified slots applying **Kernel Density Estimation (KDE)** that is considered as a statistical model to understand the shape and features of data.

## Data missing 
- Around **48%** of studies process dataset with missing values.[<sup>2</sup>](#2)
- You can **discard** the records with missing values, or use **data imputation** methods to recover the missing values. (this can be especially common in time series data)
- It would be helpful if you can find out the **mechanism** of data missing so that you can select a suitable imputation method.
- ***Avoid the missing of values during collection would always be the best solution!***

# Missing value mechanism
1. **Missing At Random (MAR)**: (may work well with statistical based methods)
2. **Missing Completely At Random (MCAR)**: (may work well with Hot-Deck)
3. **Missing Not At Random (MNAR)**: (may works well with learning algorithm, like Random Forest)

# Problem formulation
## Representation
Considering $n$ IOT devices (sensors), each report one attribute and they monitor in a period of $t$ time slots. The, we can denote the data with $x$ and specify a value with $x(t, n)$ (at the $t$th time and collected by the $n$th device). The $t$ is expected to be in the form of a **timestamp** and $x$ can be viewed as a 2D **matrix**.

We can also introduce a binary matrix (as an indicator) to mark if an element of the above matrix is missing (equals null). We can define
$$BM = X(t, n) = \begin{cases} 0,\quad (x(t, n) \quad is \quad null) \\\\ 1 \quad (otherwise)  \end{cases} $$
## Feature selection
A series of papers propose different feature selection strategies based on the matrix $x$ to formulate new feature sequences, including: finding the **cumsum**, finding the **indexes of missing values**, **transpose** of the missing value indexes, record the missing values' **count and span**, etc. The missing value spans can also be pre-categorized into different levels (*e.g.*, minute / hour / day level).



# KDE: Kernel Density Estimation
Select a bandwidth parameter $h$ (may be viewed as the window's length) and a kernel function $K(x;h)$. The function $K$ can be selected from: **gaussian, tophat, epanechnikov, exponential, linear or cosine**.

The 1-D time series case:
$$ \hat f_K(x)=\sum_{i=1}^n K_{h_x}(x-x_i) $$
The 1-D time series case: (the timestamp may have 2 or more channels)
$$ \hat f_K(x,y)=\sum_{i=1}^n K_{h_x}(x-x_i) K_{h_y}(y-y_i)$$
Use the above function to retrieves the points to make a bivariate scatter diagram to visualize
and understand the shape and features of missing data periods.

Here $x$ and $y$ may represent the start and end time of a missing part.

{% asset_img pat.png KDE visualization of missing data patterns with start and end time scatter diagram %}
The mined patterns would be like the visualization results shown above. We can find the common parts shared by the periodical data and view the rest parts as random noise.

# References
<div id='1'></div>

- [1] [Lima, Juan-Fernando, Patricia Ortega-Chasi, and Marcos Orellana Cordero]"A novel approach to detect missing values patterns in time series data." Conference on Information Technologies and Communication of Ecuador. Springer, Cham, 2019.
<div id='2'></div>

- [2] [Dong, Y., Peng, C.Y.J.]Principled missing data methods for researchers. Springer-
Plus 2(1), 222 (2013).



