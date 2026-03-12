---
title: Designing Data-Intensive-Applications-Note-2
date: 2024-02-23 16:01:35
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Topics about scalability, load & press. Definition, metrics and mitigation."
---
Topics about scalability, load & press. Definition, metrics and mitigation.
{% asset_img cover.png DDIA Chapter 2 cover: Scalability, Load and Performance Metrics %}
<!-- more -->

# Scalability 
>Systems can go wrong, with larger load and press.
- **Examples of loads**:
1. ***requests per second*** to a web server
2. ***ratio of reads*** to writes in a database
3. number of ***simultaneously active users*** in a chat room
4. ***Hit rate*** on a cache.

- **Example**: **Twitter** is more frequently read than write, so rather than the first version of: (when a user checking timeline, look up all the people they follow, merge their tweets), we can update everyone’s timeline when a post is created (version 2).
- **Concern**: number of followers is highly biased, and some head users’s posting can cause a lot of writes.
- **Mixed solution**: for celebrities, read their posts when creating timeline, and then merge with the preprocessed family tweets.

--- 

# Describe Performance
Ways to describe a system's performance:
1.	Increase load param, so that system resources **unchanged**.
2.	Increase load param, measure **extra** sys resources needed to keep performance unchanged.
**Scenarios**: In Hadoop, we care more about ***throughput***. In online sys, we care more about ***response time***.

- **Latency**: duration of a request waiting to be handled.
- **Response time**: client’s view, end to end time including network delays and queueing delays.
Simply averaging these metrics is **NOT** good due to existence of outliers. Better checking **percentiles**.
High percentiles (aka **tail latencies**) are important to user’s experience.

--- 
# Service Level Objectives v.s. Service Level Agreements
**Service Level Objectives** (SLO) and **Service Level Agreements** (SLA) are contracts defining the **expected performance** and **availability** of a service. E.g., require median response time < 200ms, P99 latency < 1s (SLO), available for 99.9% of time (SLA).

---
# Random Factors
Random factors which may cause same response taking different time: 
Random additional latency could be introduced by:
1. **Context switch** to a background process.
2. The loss of a network packet and TCP **retransmission**.
3. **Garbage collection** pause.
4. **Page fault** forcing a read from disk.
5. **Mechanical vibrations** in the server rack.

--- 

# Queueing delay
A few **slow requests** can hold up the processing of subsequent requests, known as **head-of-line blocking**.
>In real life, user would send requests **no matter of** whether the previous one is finished (this habit will result in a longer line in queue)

We can have a solution of keeping all request within the time window, sort their response times every minute. We can have approximation algos like:
1. **Forward Decay** (sounds like remove an item from a list with a probability related to its size, retire smaller ones).
2. **T-digest** (some kind of sketching, use clustering to simplify. Use centroids (mean. weight) to replace a group of numbers).
3. **HdrHistogram** (check if it is just histogram with low accuracy fixed-point num) if we cannot count percentiles accurately.

\*User can hardly tell a 200ms latency, and can usually bear a <1s latency. Long latency will impair user experience.


# Solutions to cope with load:
- **Scaling Up** = **Vertical Scaling**: Move to more powerful machine.
- **Scaling Out** = **Horizontal Scaling**: Use more machines and distribute load. (Usually inevitable) 

Some sys can be **elastic** (adding resources automatically or manually).

### Tips / Methodology
1. Distributing stateful data sys to multiple machines can be complex, thus try to keep database on a **single node** (scale up) if possible
2. Scalable architecture depends on the **volume of reads**, **writes**, **data** to store, **data complexity**, requirement of **response time**, **access pattern** or mixture of above.
3. Usually, iterating quickly on product features is more important than scaling to some **hypothetical** future load.



