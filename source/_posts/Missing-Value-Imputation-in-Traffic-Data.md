---
title: Missing Value Imputation in Traffic Data
date: 2022-04-19 14:52:23
categories:
- [UCLA, Course Study, ECE209 in 2022 spring]
tags: 
- UCLA 
- Data Science
description: "Lost of sensor-generated data can be very common. The methods of imputation can be coarsely categorized into: 1. Prediction methods; 2. Interpolation methods..."
key_concepts:
  - Missing Data Imputation
takeaways:
  - Imputation methods fall into three categories: prediction, interpolation, and statistical learning
  - ARIMA-based methods work well for temporally correlated traffic data with seasonal patterns
  - k-NN imputation leverages spatial and temporal neighbors for local pattern-based estimation
  - PPCA and MCMC provide principled probabilistic frameworks for handling missing data uncertainty
---

> Lost of sensor-generated data can be very common. The methods of imputation can be coarsely categorized into: 1. Prediction methods; 2. Interpolation methods; 3. Statistical Learning methods.
<!-- more -->

# Imputation problem & Model Formulation[<sup>1</sup>](#1)

Let $Y_c$ be the traffic dataset persists for $N$ consecutive days,
$$ Y_c = [Y(1), ..., Y(N)] $$
in which the ith $Y(i)$ be noted as 1-D vector
$$ Y(i) = [y_i(1), ..., y_i(D)]^T, i \in [1, N] $$.
Concatenate all the vectors we have together, we would have:
$$ Y_{series} = [y(1), ..., y(D \times N)]^T $$.

Typical traffic data includes the speed and number of vehicles on a certain lane at a time.  These data can form a numerical time sequence. Such data can be collected by sensor installed on the roads or along the roadsides.

# ARIMA-based method[<sup>2</sup>](#2)
**ARIMA** stands for **Autoregressive Integrated Moving Average**.

In ARIMA(p, d, q), p denotes the order of the autoregressive part, d is the degree of differencing and q is the order of moving average part:

$$ (1 - \sum_{i=1}^p \alpha_i L^i) (1 - L)^d y(t) = (1 + \sum_{i=1}^q \beta_i L^i) y(t) \xi(t)  $$

and **L** is the backshift operator, $L_y(t) = y(t- 1)$. $\xi(t)$  is white Gaussian noise.

First train  this model with the known series and impute missing data one by one. The imputed data would be used as known data for next prediction. We use Akaike information criterion to determine $p$ and $q$. $d$ is suggested to be set to $1$.

# BNs-based imputation method[<sup>3</sup>](#3)

**BN** stands for **Bayesian Netowrk**.

Based on the known dataset, learn the distribution model of multivariable variants $Y_{mv}(t) = [y(t-m), ..., y(t)]^T$.
Assume this learning target as **Gaussian mixture model (GMM)**.
Use split and merge expectation maximisation algorithm to determine the model parameters.

With a learnt GMM, missing data of $y(t)$ can be estimated as the expectation foregoing value from the latest $m$ items, as:

$$ \hat y(t) = E[y(t) | y(t-m), ..., y(t-1)] $$

# k-NN based imputation method[<sup>4</sup>](#4)

Weighted k-NN is a non-parametric estimation method.


## Selection S-step (Selection Step):

Use a metric to find $k$ nearest traffic daily flow vectors to the corrupted vector $Y(i)$ in pattern-similar from the dataset $Y_c$. 
Metrics can be **Euclidean distance** and **Pearson correlation**, for examples.

Then, the lost entry / dimension of $Y(i)$ can be imputed with the mean value of the (entries of the) $k$ vectors. 


## Imputation I-step: (Imputation Step)
Because our k-NN algorithm is weighted, then we need to find the weighted average of the k entries (averaged by the correlation coefficent given by the selected metric).  

Grid search and other optimization methods may be applied to determine best $k$.

# LLS-based imputation method[<sup>5</sup>](#5)
## Selection S-step (Selection Step):
Exactly the same as the above k-NN method.

## Imputation I-step: (Imputation Step)
Decompose k selected vectors dataset into matrix $A$ and $B$. The dimension should be corresponding to the missing part of $Y_{mis}(i)$ and observed part $Y_{obs}(i)$ of $Y(i)$.

We would have $$ \hat Y_{mis}(i) = B((A^TA)^{-1}A^T Y_{obs}(i)) $$.

This is just a pseudo-inverse, $A$ should be full-ranked/

{% asset_img matrix.png LLS imputation pseudo-inverse matrix decomposition for missing traffic data %}

# MCMC-based imputation method [<sup>6, 7</sup>](#6)

First assume the entire data sequence $Y$ follows a certain distribution, **e.g.**, Gaussian distribution.
The conditional expectation $E[Y_{mis}|Y_{obs}, \Phi]$ would be approximated by **MCMC(Markov chain Monte Carlo)** with **DA(Data Augmentation)**, since the expectation is hard to be solved precisely due to its high dimension. Here $\Phi$ stands for the parameter of the selected distribution.

The MCMC with DA is a special case of Gibbs sampler described as follows:
## Imputation I-step: (Imputation Step)
Given a current estimated model parameter $\Phi ^k$, this step uses the conditional probability $Y_{mis}^{k+1}=p(Y_{mis}|Y_{obs}, \Phi)$ to simulate missing values for each observation independently.
## Posterior P-step:
Use $p(\Phi |   Y_{obs}, Y_{mis}^{k+1})$ to update model parameter $\Phi$. In this manner, a Markov chain of $(Y_{mis}^{1},\Phi ^{1} )$, ..., $(Y_{mis}^{N},\Phi ^{N} )$ should be constructed.

The missing data is estimated as 
$$ \hat Y_{mis} = \frac{1}{N_{sample} - N_{burn-in}} \sum_{t = N_{burn-in + 1}}^{N_{sample}} Y_{mis}^t   $$.

The first $N_{burn-in}$ samples would be discarded. One feasible parameter setting is $N_{sample}=1500$ and $N_{burn-in}=500$. I believe the introduction of burn-in is to allow the model sometime to converge.


# PPCA-based imputation method[<sup>8</sup>](#6)
PPCA stands for **Probabilistic Principal Component Analysis**. It assumes that the observed data depends on latent varaiables $$ Y = Wx + \mu + \epsilon $$ where $Y$ is a D-dimensional vector of observed data, $x$ is a q-dimensional latent varaible defined Gaussian distribution and $\epsilon$ is isotropic noise. $x \sim N(0,1)$, $\epsilon \sim N(0, \sigma ^2 I)$ and $\mu$ stands for a base mean value. 

Use Expectation Maximisation (EM) method to find a set of imputed data which best fit the above distribution. Concrete steps of EM method:
## Expectation E-step: 
Find out the expectation of completed log-likelihood function with previous estimated parameters $\Phi ^k$ and observed data part $Y_{obs}$: 
$$ Q(\Phi | \Phi ^k) = E_{X, Y_{mis} | Y_{obs}, \Phi ^k}[log p_c (Y_c, X|\Phi ^k)]  $$
We can use this to update our guess of the missing data part $Y_{mis}^k$ and latent data $X^k$.

## Maximisation M-step: 
Computiong parameter space $\Phi$ by maximising the expectation of log-likelihood in E-step:
$$ \Phi ^{k+1} = \arg \max_{\Phi} Q(\Phi | \Phi ^k)  $$

Conditional expectation $E[Y_{mis} | Y_{obs}, \Phi]$ can be difficult to calculate and can approximate with MCMC with DA.

# Dataset Intended to Use: 
{% asset_img dataset.png Traffic sensor dataset used for missing value imputation evaluation %}

# Comparison

Prediction and interpolation methods mentioned cannot capture stochastic variations in daily traffic flow. On the contrary, statistical learning methods could achieve traffic flow information by emphasising the statistical characteristics of traffic flow.

**Shorting coming of such methods**: Cannot handle the situations in which neighbour (data points) DO NOT even exist.


# References
<div id='1'></div>

- [1] [Li, Yuebiao, Zhiheng Li, and Li Li]"Missing traffic data: comparison of imputation methods." IET Intelligent Transport Systems 8.1 (2014): 51-57.

<div id='2'></div>

- [2] [Ahmed, Mohammed S., and Allen R. Cook]Analysis of freeway traffic time-series data by using Box-Jenkins techniques. No. 722. 1979.

<div id='3'></div>

- [3] [Ueda, Naonori, et al.] "Split and merge EM algorithm for improving Gaussian mixture density estimates." Journal of VLSI signal processing systems for signal, image and video technology 26.1 (2000): 133-140.

<div id='4'></div>

- [4] [Troyanskaya, Olga, et al.] "Missing value estimation methods for DNA microarrays." Bioinformatics 17.6 (2001): 520-525.

<div id='5'></div>

- [5] [Kim, Hyunsoo, Gene H. Golub, and Haesun Park.] "Missing value estimation for DNA microarray gene expression data: local least squares imputation." Bioinformatics 21.2 (2005): 187-198.

<div id='6'></div>

- [6] [Ni, D., Leonard II, J.D.] "Markov chain Monte Carlo multiple imputation using Bayesian networks for incomplete intelligent transportation systems data", Transp. Res. Rec., 2005, 1935, (1), pp. 57–67

<div id='7'></div>

- [7] [Gilks, W.R., Richardson, S., Spiegelhalter, D.J.]"Markov chain Monte Carlo in practice" (Chapman & Hall, London, 1996)

<div id='8'></div>

- [8] [Tipping, M.E., Bishop, C.M.]"Mixtures of probabilistic principal
component analyzers", Neural Comput., 1999, 11, (2), pp. 443–482



