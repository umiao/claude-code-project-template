---
title: DS-Study-Note-6 Naive Bayesian modeling
date: 2022-05-02 09:39:44
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
- Naive Bayes
description: "Naïve Bayesian Classifier: is a typical learning based method which make hypothesis on the distribution of prediction target."
key_concepts:
  - Naive Bayes
  - Classification
series: Data Science
series_index: 6
takeaways:
  - Naive Bayes assumes feature independence which simplifies computation but rarely holds in practice
  - Laplace smoothing prevents zero probabilities when a feature value is absent from training data
  - Gaussian Naive Bayes handles continuous features by modeling each as a normal distribution
  - EM algorithm iteratively estimates parameters for mixture models when data has latent variables
---

**Naïve Bayesian Classifier**: is a typical learning based method which make hypothesis on the distribution of prediction target.

<!-- {% asset_img 1.jpg DS Study Note 6 cover: Naive Bayesian classifier model %} -->

<!-- more -->

# The discrete case
Let $X$ be the input feature vector and $Y$ be the labels, then our target is to find out the $Y$ which maximizes the conditional probability $P(Y|X)$, with given $X$. 
In the discrete case, we assume the conditional probabilities (of different channels of the input feature vector) are independent from each other, $$P(X^1, ..., X^D|Y) =  \prod_{d=1}^DP(X^d|Y)$$
Then, we can simply use the **total probability formula** to traverse the existing data to find out the desired $Y$ which corresponds to the maximal conditional probability.
$$ P(Y=k|x^1, ..., x^D) = \frac{\prod_{d=1}^DP(x^d|Y=k)P(Y=k)}{\sum_j\prod_{d=1}^DP(x^d|Y=j)P(Y=j)}  $$ 

$$ Y={argmax}\_k \frac{\prod_{d=1}^DP(x^d|Y=k)P(Y=k)}{\sum_j\prod_{d=1}^DP(x^d|Y=j)P(Y=j)} \\\\ ={argmax}\_k \prod_{d=1}^D P(x^d|Y=k)P(Y=k) $$

## Apply to limited dataset
$$ P(X^i=v_j|Y=k)=\frac{samples \quad with \quad X^i=v_j \quad and \quad Y=k}{samples \quad with \quad Y=k}  $$

For some outliers, *i.e.*, for given input $X$, there does not exist such data (Y), you can use **smoothing** method for **Interpolation** (*e.g.*, set a default value which equals the mean).

## Scaling factor 
You can introduce a **scaling factor** $I$ to adjust the weight between the training data and the default mean value:

$$ P(X^i=v_j|Y=k)=\frac{(samples \quad with \quad X^i=v_j \quad and \quad Y=k) + l}{(samples \quad with \quad Y=k) + lM}  $$
$$ P(Y=k)=\frac{(samples \quad with \quad label \quad k) + l}{(data \quad samples) + lK}  $$
Here $M$ stands for the number of unique values of $X$ (input) and $K$ stands for the number of unique values of $Y$ (output). 
## The continuous case
When processing continuous functions, we need to assume the distribution of the target function, and **Normal Distribution** is most commonly used. Normal Distribution can be described with two parameters, the **expectation** (mean) $\mu$ and the **variance** $\sigma$. These two can be estimated with statistics, so we select Normal Distribution to describe the conditional probability.
Of course, we use assumption not only about **distribution** but also about **independence**. We assume $P(Y|x_1, x_2)=P(x_1|Y) \times P(x_2|Y)$.

$$ \mu_j^i = E[X^i|Y=j] \\\\ \sigma_j^{2^i} = E[(X^i - \mu_j^i)^2|Y=j]$$

Generally, the essence is to determine a distribution relying on the **statistics** and then use the determined distribution to **fit the real distribution**.

# Pros and Cons
- Simple and straightforward.
- Provide the probabilistic distribution function
- Explainable / interpretable
- Require **domain knowledge**.
- Require dataset for learning
- Performs well even the i.i.d assumption is not satisfied
- Using the normal distribution for modeling provides some good properties, but may be contrary to the facts

# Correction of distribution modeling with Gaussian distribution
Applying the Gaussian / Normal distribution can introduce good properties but may not be reasonable. *E.g.*, the Gaussian distribution has two long tails at the left and right, and it has exactly one peak. 
In order to model the distribution which may have **multiple peaks**, you can use the sum of multiple Gaussian functions for modeling. You can still use the training data to estimate the parameters of these Gaussian distributions.

## EM (Expectation Maximization) Algorithm for parameter estimation
It includes two steps: the **expection-step (E-step)** and **maximization-step (M-step)**. The prior estimate the parameters by observing the data and existing model, and then computes the **expection** of the **likelihood function** with the parameters. The latter find the parameters which **maximizes** the likelihood function.
- The algorithm assures that after each iteration, the value of likelihood function would **increase**, so that the function is bound to converge.

### Instance of EM algorithm
Given two coins with different distribution, we need to estimate their expection of head-up probability after flipping. However, the experiment records do not specify which coin a single record corresponds to. Thus, we need to estimate *the coin an experiment record corresponds to*, and *the expection of getting a head* after flipping **at the same time**.
- We first initialize the expection of the two coins to be **different** values.
- For each experiment record, find out the distribution of the mapping relationship $Z$, to complete a E-Step (*e.g.*, 0.7 belongs to coin A, 0.3 belongs to coin B).
- Use the achieved $Z$ to assign weights to the experiment records. (View each record as a mixture of using coin A and B).
- Update the experiment results to: the estimate experiment result when flipping coin A / B. (times the distribution of $Z$ with the experiment results)
- Base on the priciple of maximize the likelihood, use the updated experiment records to calculate the expectation of the two coins iteratively, as the M-Step

## Apply EM algorithm to solve Gaussian mixture model
Each observation (experimente record) corresponds to the overlap of multiple normal distributions and the parameters are unkown. Then, we can randomly initialize the parameters for the distributions, and find out how each data point can be decomposed into these distributions. Then, we can get the datapoints weighted so that it only includes **one** distribution. Then we can correct the parameters of normal distribution in an **iterative** manner.

>It should be noted that the guarantee of convergence **does not** mean that the EM algorithm can converge at the **global optimal point**, because the given initial parameters decide the upper-bound of performance to a large extent.

# Appendix 
This is about the deduction of EM algorithm's property of convergence guarantee.
## Jensen Inequity
if $f$ is a **Concave function**, $X$ is a random variable, then $E[f(X)] 
\le f(E[x])$. 
Similar conclusion holds, with the unequal sign in the **opposite** direction, when $f$ is a **Convex function**.

Let $P(x,z)$ be the distribution with latent variable $z$ (the weight / contribution of a certain Gaussian distribution made to a datapoint).
$$ \sum_{i=1}^M\sum_{z=1}^NlnP(x,z) =  \sum_{i=1}^Mln\sum_{z=1}^NQ(z) \frac{P(x,z)}{Q(z)}$$
With Jensen inquity (log is a concave function):
$$ \sum_{i=1}^Mln\sum_{z=1}^NQ(z) \frac{P(x,z)}{Q(z)} \ge \sum_{i=1}^M\sum_{z=1}^NQ(z) ln\frac{P(x,z)}{Q(z)} $$

The key step is to adjust $Q(z)$ so that makes the right part equals the left part (reach the $=$). The $=$ can be reached when the input function is a constant function, *i.e.*, $\frac{P(x,z)}{Q(z)}=c$.
Then we have $\sum_z P(x,z) = c\sum_z Q(z) \Rightarrow Q(z) = \frac{P(x,z)}{\sum_zP(x,z)} = \frac{P(x,z)}{P(x)} \Rightarrow P(z|x)$

Then, we solved the issue of how to select $Q(z)$ -- by selecting the posterior probability. This is the essence of E-step which is to build lower-bound for the likelihood function $L(\theta) = \sum_{i=1}^M\sum_{z=1}^NlnP(x,z)$, where $\theta$ is the parameter set of these distributions.
The following M-step aims at adjusting $\theta$ to maximize the lower-bound of $L(\theta)$.
It should be noted that this process is guaranteed to converge, but it may get into local optimal rather than the real parameter values (reach the global optimal). This is determined by the initialization of parameters. 

