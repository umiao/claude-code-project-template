---
title: DS-Study-Note-5 Support Vector Machine (SVM)
date: 2022-04-26 23:51:47
categories:
- [Data Science, General Knowledge]
tags:
- Data Science
- Machine Learning
- SVM
description: "SVM is a machine learning model which aims at finding a Decision Boundary with a subset of the training set. The SVM is a non-probabilistic binary classifier."
---
SVM is a machine learning model which aims at finding a Decision Boundary with a subset of the training set. The SVM is a non-probabilistic binary classifier.
{% asset_img svm.png ML_note %}
<!-- more -->

# Linear Separable
**Linear Separable** stands for an attribute that two class of points can be **completely divided** by a **hyperplane** (more specifically, a line in the 2-D space). 
A **hyperplance** can be determined with normal vector $W$ and intercept $b$, *i.e.*, $$ X^TW + b=0 $$. For the two separable groups, they would satisfies $X^TW + b>0$ and $X^TW + b<0$, respectively. 
- In order to enhance the **robustness**, we additionally require the best-fit hyperplane to separate these two classes with maximum margin  / interval, which is called **Maximum Margin Hyperplane**.

# SVM (Support Vector Machine)
In the training set, the points which are nearest to the hyperplane are named Support Vector. After generalized to $n$ dimensional space, a point $x = (x_1, ..., x_n)$'s *distance* to the hyperplane $w^Tx+b=0$ is $\frac{|w^Tx+b|}{||w||}$ (the denominator corresponds to 2-norm). We are interested with these support vectors and optimize the hyperplane in order to maximize the margin between the support vectors which belong to different classes.

If the maximized distance equals $d$, for all the support vectors, we further unfold the absolute value expression to have: 
$$ \frac{w^Tx+b}{||w||} \ge d, y= 1; \quad \frac{w^Tx+b}{||w||} \le -d, y= -1$$
while $y$ marks different classes. 
Ignore the constant factor, we can have $$ w^Tx+b \ge 1 (y=1); \quad w^Tx+b \le -1 (y=-1)$$
which equals $$ y(w^Tx+b) \ge 1 $$, so that we use hyperplanes $w^Tx+b= \pm 1$ to seperate the two classes. Replace the numerator of the distance expression with the two hyperplanes to have our optimization target:
$$ \max_{w, b} margin \Leftrightarrow \max(\frac{2}{||w||}) \Leftrightarrow \max(\frac{2}{||w||})^2 \Leftrightarrow \min({||w||}^2), \quad y(w^Tx+b) \ge 1 $$	
We can add a constant factor of $\frac{1}{2}$ to absorb the constant factor after get derivative of $w^2$.

## Support Vectors
Now we can tell that support vectors are all the vectors on the lines of $wx^T +b = \pm 1$. Only the support vectors would contribute to the classification.

# Primal-Dual Transformation
In order to solve the primal problem of $\frac{1}{2} {||w||}^2$, we can use **Method of Lagrange Multiplier** to **solve its Dual Problem**. Solving the corresponding dual problem has the advantages of:
- Easier to solve with simpler constraints and only need to optimize one variable $\alpha$
- Able to introduce kernel function to generalize to non-linear cases

## Method of Lagrange Multiplier
1. Problem formulation
$$ \min f(x_1, ..., x_n) s.t. h_k(x_1, ..., x_n)= 0, k=1,2,...,l $$
That is to say, we decide to optimize function $f(x_1, ..., x_n) $ with $l$ extra constraints. We can let $$ L(x, \lambda = f(x) + \sum_{k=1}^l \lambda_k h_k(x) $$, where $L(x, \lambda)$ is named **Lagrange Function**, and $\lambda$ is **NOT** required to be non-negative.

When solving the problem, we need to find $\frac{\partial L(x, \lambda)}{\partial x_i}$ for each $i \in \{1, ..., n\}$ and let them be $0$. This is called **necessary condition of equality constraints** (in order to get extremum).

## Strong Duality
We want to transform $$ \min_w \max_\lambda L(w, \lambda)  \Rightarrow \max_\lambda \min_w  L(w, \lambda), \quad (\lambda_i \ge 0)$$
For function $f$, if we have $\min \max f \ge \max \min f$, that is, the minimum of the possible maximums is still greate than the maximal possible minimums, we say there exists **weak duality**. If $f$ is **convex optimization problem**, we have **strong duality**. 
In order to handle the SVM problem, we require the **Karush-Kuhn-Tucker (KTT)** condition as the **necessary and sufficient condition** of strong duality.

## Karush-Kuhn-Tucker (KTT) condition
We need to transform the optimization of inequality into optimization of equality:
$$ \min f(w)=\min \frac{1}{2} {||w||}^2, g_i(w) = 1 - y_i(w^Tx_i+b)\le 0 $$
into
$$ L(w, \lambda, a) = f(w) + \sum_{i=1}^n \lambda_i h_i(w) = f(w) + \sum_{i=1}^n \lambda_i [g_i(w) + \alpha_i^2], \lambda_i \ge 0$$
$g_i(w)$ is guaranteed to be $\le 0$ for $\forall i$, we can solve a series of non-zero values (a_i^2) to make every term of constraints $0$. Then we require $L$'s' partial derivative to $w$, $\lambda$ and $a$ equals $0$ to derive the KKT condtion:
$$\min L(w, \lambda, a) \Rightarrow \min L(w, \lambda) = f(w) + \sum_{i=1}^n \lambda_i g_i (w)$$
The achieved minima must be greater than $0$, we have $\sum_{i=1}^n\lambda_i g_i(w)\le 0 $, $L(w, \lambda) \le p$ as a natural upper bound. So that our objective can be changed to $\max_\lambda L(w, \lambda)$.
The dual optimization problem after transformation: $$\min_w  \max_\lambda L(w, \lambda) , \lambda_i \ge 0$$ 

# Procedure of solving SVM problem
1. Construct Lagrange Function $\min_{w,b}\max_{\lambda}L(w,b,\lambda)= \frac{1}{2} {||w||}^2 + \sum_{i=1}^n \lambda_i [1 - y_i(w^Tx_i+b)] $
2. Transform to dual problem $\max_\lambda \min_{w,b}L(w,b,\lambda)$ 
Find derivatives: $\frac{\partial L}{\partial w}=w - \sum_{i=1}^n \lambda_i x_iy_i=0$,
$\frac{\partial L}{\partial b}=\sum_{i=1}^n \lambda_i y_i=0$ to get $\sum_{i=1}^n \lambda_i x_iy_i=w$, $\sum_{i=1}^n \lambda_i y_i=0$.
Substitue into function:
{% asset_img f1.png ML_note %}, that is, 
$$ \min_{w,b}L(w,b,\lambda)=\sum_{j=1}^n\lambda_i - \frac{1}{2} \sum_{i=1}^n\sum_{j=1}^n \lambda_i\lambda_jy_iy_j(x_i \cdot x_j) $$
3. We can tell that the above question is a quadratic programming problem and its scale is proportional to the number of training samples. It can be solved with **Sequential Minial Optimization (SMO)** algorithm. It optimizes one parameter a time and fixed the others.
	- We just mentioned that SMO algorithm optimize **only one** parameter a time. However, we have a constraint $\sum_{i=1}^n \lambda_i y_i=0$ which must be satisfied. Thus, we update **two** parameters a time to solve this issue. With two selected parameters $\lambda_i$ and $\lambda_j$, we fix the other parameters and we have $$\lambda_i y_i + \lambda_j y_j = c, \lambda_i \ge 0, \lambda_j \ge 0, c= -\sum_{k \ne i,j}\lambda_ky_k $$ Then we can have $\lambda_j = \frac{c-\lambda_iy_i}{y_j}$ so that we can replace $\lambda_j$ with expression of $\lambda_i$, find the partial derivative for $\lambda_i$ and update the two paramteres, keep iterating until converge.
4. By find partial derivative, we can have $w=\sum_{i=1}^m \lambda_i y_i x_i$. All the points corresponding to a $\lambda_i > 0$ are **support vectors** (non-support vectors correspond to $\lambda_i=0$), and we can find an arbitary support vector $x_s$ and substitute x to have $y_s(wx_s+b)=1 \Rightarrow y_s^2(wx_s+b)=y_s$ to find $b$. $y_s^2=1$, thus $b=y_s - wx_s$. We can also find b via the mean value of the support vectors: $$b=\frac{1}{|S|}\sum_{s\in S}(y_s - wx_s) $$
5. With $w$ and $b$ found, we can construct the hyperplane $w^Tx+b=0$ and use $f(x)=sign(w^Tx+b)$ to decide the classification result.

# Parameters to be searched (tuned) in SVM
- **C**: decide the level of regularization. In fact, $C=\frac{1}{\lambda}$ and $\lambda$ is the regularization coefficient. (Is a squared l2-penalty)
- **kernel**: The kernel function adopted by SVM model.
- **degree**: The highest degree, when adapting Polynomial kernel function.
- **gamma**: Coefficent of the kernel function.
Beside, you can decide whether to use **heuristic shrinking**, **tolerance** (the desired accuracy at convergence), size allocated to **kernel cache**, **iteration times**. You can also appoint **random state** for reproducing results.

# Soft Margin
The original SVM require the problem to be solved is **linear separable**. When this prerequisite is not satisfied, we can use **soft margin** to solve this problem. Originally, we require the two classes correspond to different signs, in a hyperplane expression. Now, we can allow SVM to misclassify on a handful of vectors. 
$$ y_i(w^Tx_i+b) - \xi_i  \ge 1$$ which means that for such $i$, they do not meet the constraint and need the help of **relax coefficient** $\xi_i$.

In order to minimize the number of misclassified vectors, we would fix our objective (loss) (by appending a regularization term for the relax coefficients):
$$ \min_w \frac{1}{2}{||w||}^2 + C \sum_{i=1}^m \xi_i, \quad g_i(w,b)=1-y_i(w^Tx_i+b)-\xi_i \le 0, \xi_i \ge 0 $$
Here, $C > 0$ and can be understood as the penalty to the misclassified samples. If $C \rightarrow \infty$, then $\xi_i \rightarrow 0$ and the SVM (with soft margin) becomes linear separable SVM.

# Kernel Function
The essence of kernel function $K$ is to map vectors from low-dim Hilbert Space to high-dim. By this mean, we expect the samples which are not linear separable become separable, in the high-dim space.
$$K(x,z)=\phi(x) \cdot \phi(z)$$
Prerequisite: The Gram matrix formed by the set of all the points of the function is **semi-positive definite**. (a.k.a. complete inner product space)

{% asset_img ker.jpg ML_note %}

The introduction of kernel function is to solve the case of linear unseparable. It is costly to map samples to high-dimensional space before calculating dot product, thus kernel function can realize effectively calculating the dot product result of high-dimensional space, in low-dimensional space.
## Types of kernel functions
- Linear kernel: $x_i^Tx_j$
- Polynomial Kernel: $(x_i^Tx_j+c)^d$
- Radial basis function kernel: $exp(-\frac{||x_i-x_j||_2^2}{2\sigma ^2})$
- Hyperbolic tangent kernel: $tanh(Kx_i^Tx_j+c), \quad K>0, c<0$
It is clear that only the latter three needs parameter tuning.

# Pros and Cons
## Advantages:
1. Supported by math theory, highly **interpretable**
2. Do not rely on statistical method, simplify the regular classification and regression problem (solely rely on the support vectors, which are deterministic and crucial samples)
3. Applying of kernel function can handle the **unlinear tasks**
4. Computational complexity relies on the number of support vectors(rather than the dimensional of the sample space), avoid the curse of dimension
## Disadvantages:
1. Long training time (every time select a pair of parameters for optimization to maintain the sum unchanged). The complexity would be $\mathcal{O}(n^2)$ where $N$ equals the number of training samples.
2. If applied kernel function and need to store the matrix, extra space of  $\mathcal{O}(n^2)$ is required.
3. The prediction rate is **inversely proportional** to the number of support vectors, leading to high complexity. 
4. Not suitable for scenarios which have millions, or even hundreds of millison of samples.



