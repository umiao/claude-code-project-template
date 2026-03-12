---
title: NLP-1 Roadmap
date: 2022-06-20 10:23:43
categories:
- [AI, NLP]
tags:
- NLP
description: "Have a glance on the NLP tasks and techniques. Will be discussed in a more detailed manner."
---
Have a glance on the NLP tasks and techniques. Will be discussed in a more detailed manner.
{% asset_img rm.png NLP study roadmap cover: overview of NLP tasks and techniques %}
<!-- more -->
# General Roadmap for NLP Study


```mermaid
graph LR;
    1[Preliminary]--> 1.1[Linear Algebra];
    1 --> 1.2[Statistics and Probability];
    1--> 1.3[Metrics];

    2[Traditional model];
    2 --> 2.1[Statistical ML];
    2.1 --- 2.1.1(Linear Classification);
    2.1 --- 2.1.2(SVM);
    2.1 --- 2.1.3(Tree Model);
    2.1 --- 2.1.4("HMM / CRF");


    2 --> 2.2[Neural Network];
    2.2 --- 2.2.1(Word embedding);
    2.2 --- 2.2.2(CNN);
    2.2 --- 2.2.3(RNN/LSTM/GRU/Bidirectional);
    2.2 --- 2.2.4(ELMo);
    2.2 --- 2.2.5(BERT);


    3[Paradigm and trick];
    3 --> 3.1[Document Classification];
    3.1 --- 3.1.1(ReNN);
    3.1 --- 3.1.2(MLP);
    3.1 --- 3.1.3(RNN);
    3.1 --- 3.1.4(CNN);
    3.1 --- 3.1.5(Attention);
    3.1 --- 3.1.6(Transformer);
    3.1 --- 3.1.7(GNN);


    3 --> 3.2[Sentence Matching];
    3.2 --- 3.2.1(Representation based);
    3.2 --- 3.2.2(Interaction based);

    3 --> 3.3[Annotation];
    3.3 --- 3.3.1(Embedding Module);
    3.3 --- 3.3.2(Context Encoder Module);
    3.3 --- 3.3.3(Inference Module);

    3 --> 3.4[Generation];
    3 --> 3.5[Language Model];
    3.5 --- 3.5.1(Word Level);
    3.5 --- 3.5.2(Sentence Level);

    4[Application Scenarios];
    4 --> 4.1[Single Task];
    4.1 --- 4.1.1(Lexical Analysis);
    4.1 --- 4.1.2(Syntax Analysis);
    4.1 --- 4.1.3(Semantic Analysis);
    4.1 --- 4.1.4(Document Generation);



    4 --> 4.2[Complex Task];
    4.2 --- 4.2.1(Search / Recommendation);
    4.2 --- 4.2.2(Conversation);
    4.2 --- 4.2.3(Knowledge Graph);
```

# By the way
Other roadmaps of the ML / Statistical topics would be placed here (from [reddit](https://www.reddit.com/r/MachineLearning/comments/d8jheo/p_natural_language_processing_roadmap_and_keyword/)):
{% asset_img 1.png NLP roadmap from reddit: part 1 of 4 %}
{% asset_img 2.png NLP roadmap from reddit: part 2 of 4 %}
{% asset_img 3.png NLP roadmap from reddit: part 3 of 4 %}
{% asset_img 4.png NLP roadmap from reddit: part 4 of 4 %}
