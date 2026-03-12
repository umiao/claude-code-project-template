---
title: 14th_May_Researcher_Paper_Work_Group
date: 2024-05-14 23:43:14
categories:
- [Research, Paper Read]
tags:
- Research
description: "Notes from a research paper discussion group covering robust selection, stream processing, and UCB procedures."
---
Discussion on challenges with stream processing.
{% asset_img cover.png Research Paper Work Group cover: robust selection and UCB procedure discussion %}
<!-- more -->

### Upper-Confidence-Bound Procedure for Robust Selection of the Best
Author: Yuchen Wan

In simulation area, there may lies input uncertainty in the underlying simulation model.
**Robust selection of the best (RSB)**: models this input uncertainty by a discrete **ambiguity set** (containing multiple possible scenarios) and then proposes a two-layer framework under which the best alternative is defined to have the best **worst-case mean performance** over the ambiguity set. 
\* Categorized as **fixed-precision** and **fixed-budget**

This paper claims to invent a new robust **upper-confidence-bound (UCB)** procedure. 

**Ranking and selection (R&S)** seeks to select the best alternative (have the **smallest mean
performance**) from a finite number of alternatives through repeatedly sampling a simulation model.

If the input distribution is not known, we may also want to model the **input uncertainty** (measurement error).
2-layers: 1 layer to identify the distribution of worst case, 1 layer to compare these cases mean performance.


Difference from **MAB (multi-Armed Bandit)**: Do not count in the regret during "exploration" stage, just aims at selecting the best one. This is under a clear explore-and-exploit 2 stages framework, and should it be easier?

>For me it is quite intuitive that higher exploration rate will lead to better simple regret..

**Take Away**: Figure out a well developed field like RL / MAB, and transfer the related techniques / success into new scenarios or (may be simplified) problems. 

**To be improved**: we may expect a stronger theoretical analysis and tighter bound of error / probabilistic guarantee. The guarantee shown in the paper may not look very satisfying.

---




