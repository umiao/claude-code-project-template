---
title: "Data Science & ML Cheat Sheet"
date: 2026-03-12
type: "page"
comments: false
---

# Data Science & Machine Learning Quick Reference

A condensed reference of all 9 DS study notes. Covers core ML concepts, algorithms, and ensemble methods.

---

## 1. Overfitting (Note 1)

**Definition**: Model memorizes training noise instead of learning general patterns.

### Causes and Solutions

| Cause | Solution |
|-------|----------|
| Small training data | Collect more data, data augmentation |
| Train/test distribution mismatch | Ensure iid sampling |
| Noise in data | Feature selection, data cleaning |
| Too many iterations | Early stopping |
| Excessive model complexity | Reduce parameters, simpler model |
| Information leakage | Strict train/test separation |

### Regularization Quick Reference

| Technique | What It Does |
|-----------|-------------|
| L1 (LASSO) | Adds sum of absolute weights to loss; drives weights to zero (sparse) |
| L2 (Ridge) | Adds sum of squared weights to loss; shrinks all weights (smooth) |
| Dropout | Randomly deactivates neurons during training |
| Early stopping | Stop training when validation error increases |
| PCA / SVD | Reduce dimensions, remove redundant features |

---

## 2. Bias-Variance Tradeoff (Note 2)

**Total Error = Bias^2 + Variance + Irreducible Error**

| | Low Bias | High Bias |
|---|---------|-----------|
| **Low Variance** | Ideal (rare) | Underfitting (simple model) |
| **High Variance** | Overfitting (complex model) | Worst case |

| Term | Definition | Source |
|------|-----------|--------|
| Bias | How far predictions are from truth (systematic error) | Wrong model assumptions |
| Variance | How much predictions change across datasets (instability) | Noise sensitivity |
| Irreducible error | Random noise that no model can capture | Unknown factors |

### Model Complexity Spectrum

```
Simple model (linear)  ------>  Complex model (deep NN)
  High bias                       Low bias
  Low variance                    High variance
  Underfitting                    Overfitting
```

**K-fold Cross-Validation**: Splits data into K folds, trains on K-1, tests on 1. Rotates K times. Reduces variance in evaluation but slightly increases bias (less training data per fold).

---

## 3. Curse of Dimensionality (Note 3)

### Problems in High-Dimensional Space

| Problem | Description | Threshold |
|---------|------------|-----------|
| Distance concentration | Min/max distances converge; similarity metrics break | ~20 dimensions |
| Combinatorial explosion | Data clusters in corners; sample space grows exponentially | Exponential with dims |
| Hubness | Some points become nearest neighbors of disproportionately many others | Increases with dims |

### Solutions

| Approach | Trade-off |
|----------|-----------|
| Remove redundant features | Requires domain knowledge |
| PCA | Loses interpretability |
| Autoencoders / CNN | Learns representations; black box |
| Feature selection | May miss interactions |

---

## 4. Evaluation Metrics (Note 4)

### Confusion Matrix

| | Predicted Positive | Predicted Negative |
|---|-------------------|-------------------|
| **Actual Positive** | TP (True Positive) | FN (False Negative) |
| **Actual Negative** | FP (False Positive) | TN (True Negative) |

### Key Metrics

| Metric | Formula | When to Use |
|--------|---------|-------------|
| Accuracy | (TP+TN) / Total | Balanced classes only |
| Precision | TP / (TP+FP) | Cost of false positive is high (spam filter) |
| Recall (Sensitivity) | TP / (TP+FN) | Cost of false negative is high (disease detection) |
| F1 Score | 2 * P * R / (P + R) | Balance precision and recall |
| Specificity | TN / (TN+FP) | True negative rate |

### Precision-Recall Tradeoff
- Raise threshold: Precision goes up, Recall goes down (more conservative)
- Lower threshold: Recall goes up, Precision goes down (more permissive)

### ROC & AUC

| Component | Description |
|-----------|-------------|
| ROC Curve | TPR (y-axis) vs FPR (x-axis) at all thresholds |
| AUC | Area under ROC; 1.0 = perfect, 0.5 = random |
| PR Curve | Precision (y) vs Recall (x); better for imbalanced data |

### Multi-class Metrics

| Variant | Calculation |
|---------|-------------|
| Macro-F1 | Average F1 across classes (treats all classes equally) |
| Micro-F1 | Pool all TP/FP/FN globally, then compute F1 (weights by frequency) |

---

## 5. Support Vector Machine (Note 5)

### Core Idea
Find the hyperplane that maximizes the margin between classes. Only **support vectors** (nearest points to the hyperplane) determine the boundary.

### Key Formulas

| Concept | Formula |
|---------|---------|
| Decision boundary | w^T x + b = 0 |
| Point-to-hyperplane distance | \|w^T x + b\| / \|\|w\|\| |
| Primal objective | min (1/2)\|\|w\|\|^2 s.t. y_i(w^T x_i + b) >= 1 |
| Soft margin | min (1/2)\|\|w\|\|^2 + C * sum(xi_i) |

### Kernel Functions

| Kernel | Formula | Use Case |
|--------|---------|----------|
| Linear | x_i^T x_j | Linearly separable data |
| Polynomial | (x_i^T x_j + c)^d | Moderate non-linearity |
| RBF (Gaussian) | exp(-\|\|x_i - x_j\|\|^2 / 2sigma^2) | General non-linear (most common) |
| Sigmoid | tanh(alpha * x_i^T x_j + c) | Neural network analogy |

### Tuning Parameters

| Parameter | Effect |
|-----------|--------|
| C (penalty) | High C = hard margin (less misclassification, risk overfit). Low C = soft margin (more tolerance) |
| gamma (RBF) | High gamma = tight decision boundary (overfit). Low gamma = smooth boundary |
| degree (Poly) | Higher degree = more complex boundary |

### SVM Pros & Cons

| Pros | Cons |
|------|------|
| Strong mathematical foundation | O(n^2) to O(n^3) training time |
| Effective in high dimensions | O(n^2) kernel matrix memory |
| Works with small datasets | Not suitable for millions of samples |
| Handles non-linear via kernels | Hard to interpret (especially kernel) |

---

## 6. Naive Bayes (Note 6)

### Core Formula

**P(Y|X) is proportional to P(X|Y) * P(Y)**

Decision: argmax_k product(P(x_i | Y=k)) * P(Y=k)

### Variants

| Variant | Feature Type | Assumption |
|---------|-------------|------------|
| Multinomial | Discrete counts | Multinomial distribution |
| Gaussian | Continuous | Normal distribution per feature per class |
| Bernoulli | Binary (0/1) | Bernoulli distribution |

### Laplace Smoothing
Prevents zero probability when a feature value is absent from training data:

**P(x_i = v | Y = k) = (count + l) / (total + l * M)**

where l = smoothing factor (usually 1), M = number of possible values.

### EM Algorithm (for Gaussian Mixture Models)

| Step | Action |
|------|--------|
| E-step | Compute expected likelihood using current parameters |
| M-step | Find parameters that maximize the expected likelihood |
| Repeat | Until convergence (monotonically increases likelihood) |

**Warning**: EM finds local optima, not guaranteed global. Sensitive to initialization.

---

## 7. L1 vs L2 Regularization Deep Dive (Note 7)

### Comparison Table

| Property | L1 (LASSO) | L2 (Ridge) |
|----------|-----------|-----------|
| Penalty term | sum(\|w_i\|) | sum(w_i^2) |
| Gradient magnitude | Constant (+/-1) | Proportional to w |
| Sparsity | Yes (drives weights to exactly 0) | No (shrinks toward 0 but never reaches) |
| Feature selection | Built-in (zeroes irrelevant features) | No (keeps all features) |
| Unique solution | Not guaranteed (multiple optima) | Guaranteed (unique minimum) |
| Computation | Harder (non-differentiable at 0) | Easier (smooth everywhere) |

### Gradient Behavior

| | L1 | L2 |
|---|----|----|
| Update rule | w = w - alpha * sign(w) | w = w - alpha * w |
| Near zero | Constant step size (jumps to 0) | Vanishing step (approaches 0 asymptotically) |

**When to use L1**: Feature selection needed, expect many irrelevant features.
**When to use L2**: All features potentially relevant, want stable solution.

---

## 8. Ensemble Methods & Random Forest (Note 8)

### Ensemble Paradigms

| Method | Training | Combination | Key Property |
|--------|----------|-------------|--------------|
| Bagging | Parallel, bootstrap samples | Equal-weight voting/averaging | Reduces variance |
| Boosting | Sequential, adaptive weights | Weighted combination | Reduces bias |
| Stacking | Independent models | Meta-learner (e.g., logistic regression) | Combines strengths |

### Bagging vs Boosting

| | Bagging | Boosting |
|---|--------|---------|
| Sampling | With replacement | Reweight misclassified samples |
| Model weights | Equal | Higher weight for better models |
| Parallelizable | Yes | No (sequential) |
| Overfitting risk | Low | Higher |
| Error reduction | Variance | Bias |

### Random Forest

**= Bagging + Decision Trees + Random Feature Subsets**

Each tree:
1. Bootstrap sample N data points (with replacement)
2. At each split, randomly select m features (m << M total)
3. Choose best split among m features (information gain or Gini)
4. Grow tree fully (no pruning)

Final prediction: majority vote (classification) or average (regression).

**Why random features?** Decorrelates trees. Without it, all trees would split on the same strong features.

| Pros | Cons |
|------|------|
| Handles high dimensions without reduction | Overfits on very noisy data |
| Built-in feature importance | Biased toward high-cardinality features |
| Resistant to overfitting | Less interpretable than single tree |
| Handles missing data partially | |
| Fast, parallelizable | |

---

## 9. Gradient Boosting: GBM, XGBoost, LightGBM (Note 9)

### GBM Core Idea
Each new tree fits the **negative gradient** (residuals) of the loss function:

**F_k(x) = F_{k-1}(x) + alpha * h_k(x)**

where h_k is fitted to the negative gradient of the loss at F_{k-1}.

### GBM vs XGBoost vs LightGBM

| Feature | GBM | XGBoost | LightGBM |
|---------|-----|---------|----------|
| Approximation | First-order gradient | Second-order Taylor expansion | Second-order + histogram |
| Regularization | None built-in | L1 + L2 on leaf weights + count | Same as XGBoost |
| Tree growth | Level-wise | Level-wise | Leaf-wise (best-first) |
| Parallelism | None | Block structure for parallel | Parallel histogram |
| Speed | Slowest | Fast | Fastest |
| Memory | High | Moderate | Low (histogram binning) |

### XGBoost Key Innovations

| Innovation | Benefit |
|-----------|---------|
| Second-order Taylor expansion | Better loss approximation, faster convergence |
| Regularization term Omega | Controls tree complexity (leaf count + weight L2 norm) |
| Block structure | Enables parallel column processing |
| Optimal leaf weight: w_j = -G_j / (H_j + lambda) | Closed-form solution per leaf |

### LightGBM Key Innovations

| Innovation | How It Works |
|-----------|-------------|
| Leaf-wise growth | Splits the leaf with max gain (vs all leaves at same depth) |
| Histogram binning | Discretizes continuous features into bins; reduces split candidates |
| Histogram subtraction | Child histogram = parent - sibling (halves computation) |
| GOSS | Keeps high-gradient samples + random sample of low-gradient ones |
| EFB (Exclusive Feature Bundling) | Bundles non-conflicting sparse features into one |

### Ensemble Method Combinations

| Combination | Result |
|-------------|--------|
| Bagging + Decision Tree | Random Forest |
| AdaBoost + Decision Tree | Boosting Tree |
| Gradient Boosting + Decision Tree | GBDT |
| GBDT + 2nd-order + regularization | XGBoost |
| XGBoost + leaf-wise + histogram | LightGBM |

---

## Quick Decision Guide

**Classification algorithm?**
- Small dataset, clear margin -> SVM (RBF kernel)
- Fast baseline, interpretable -> Naive Bayes
- Tabular data, best accuracy -> XGBoost / LightGBM
- Need probability output -> Naive Bayes or calibrated ensemble

**Regularization?**
- Feature selection needed -> L1
- All features matter -> L2
- Both -> Elastic Net (L1 + L2)

**Ensemble method?**
- Reduce variance (unstable base learner) -> Bagging / Random Forest
- Reduce bias (weak base learner) -> Boosting / XGBoost
- Combine diverse models -> Stacking

**Evaluation metric?**
- Balanced classes -> Accuracy or F1
- Imbalanced classes -> Precision/Recall, AUC-ROC, or AUC-PR
- Ranking quality -> AUC
- Cost-sensitive -> Cost curves

**High dimensions?**
- Try Random Forest first (handles high dims natively)
- Apply PCA if needed for visualization or speed
- Use L1 regularization for feature selection
- Be aware of distance concentration above ~20 dimensions
