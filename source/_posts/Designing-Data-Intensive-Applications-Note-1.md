---
title: Designing Data-Intensive-Applications-Note-1
date: 2024-02-23 15:44:41
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Introduction to designing data intensive applications, a.k.a data systems, providing high-level ideas about what it is and why it is needed."
key_concepts:
  - Fault Tolerance
  - Scalability
  - Replication
takeaways:
  - Distinguish between faults and failures when designing resilient systems
  - Use redundancy at every level (hardware, software, process) to tolerate faults
  - Minimize opportunities for human error through good abstractions and sandbox environments
  - Design systems around three pillars: reliability, scalability, and maintainability
series: DDIA
series_index: 1
---
Introduction to designing data intensive applications, a.k.a data systems, providing high-level ideas about what it is and why it is needed.
{% asset_img cover.png DDIA Chapter 1 cover: Reliable, Scalable, and Maintainable Applications %}
<!-- more -->

# Key Concepts
1. **Reliability**: tolerating hardware & software faults; as well as human error
2. **Scalability**: Measuring load & performance; latency, percentiles and throughput
3. **Maintainability**: operability, simplicity & evolvability

**Motivation**: More applications are **data intensive** than compute-intensive. The amount of data, complexity and how fast it changes is the issue.

## Commonly used components:
- Store data so that they, or another application, can find it again later (**databases**)
- Remember the result of an expensive operation, to speed up reads (**caches**)
- Allow users to search data by keyword or filter it in various ways (**search indexes**)
- Send a message to another process, to be handled asynchronously (**stream processing**)
- Periodically crunch a large amount of accumulated data (**batch processing**)

## Meaningfulness of having the data system concept:
1. The boundaries between categories got blurred:  datastores that are also used as message queues (**Redis**), and there are message queues with database-like durability guarantees (**Apache Kafka**)
2. Single tool is harder to handle multiple use cases and needs. So we can break down into tasks which can efficiently run on single tool.
3. Selection of components and getting them to work make you also a data system designer

---

## Fault and Failure
**Fault tolerant / resilient**: System anticipate faults (certain types of faults) and can cope with them. 
Fault $\ne$ failure, as fault is one component of the system deviating from its spec, whereas a *failure* is when the system as a whole stops providing the required service to the user. We should try stop fault turn into failure.

Intentionally triggering faults may help prevent failure (like release resources).
This book focuses more on **curable** faults.


### Hardwares 
>We assume hardware related errors to be random and independent.

Hard disks are reported as having a **mean time to failure** (MTTF) of about 10 to 50
years. Thus, on a storage cluster with 10,000 disks, we should expect on average one disk to die per day.  

**Solution**: 
Add Disk **redundancy**, like **RAID** configuration.
**Servers**: dual power supplies and hot-swappable CPUs
**Power**: batteries and diesel generators


### Software

For AWS, it is fairly common for virtual machine instances to become unavailable without warning, as the platforms are designed to prioritize **flexibility** and **elasticity** over single-machine **reliability**.


Software / systematic error can be harder to anticipate, and can occur a lot more than hardware failures as they are correlated. Like software bug, or deplete of resources (CPU time, memory, disk, etc). The failures can also be cascading, one trigger another.

--- 

### Mitigation Methods

Some methods to help mitigate system failures:
1. Carefully thinking about **assumptions** and **interactions** in the system. 
2. Thorough **testing**.
3. Process **isolation**.
4. Allowing processes to **crash** and **restart**. 
5. **Measuring** (do some validation / verification), **monitoring**, and **analyzing** system behavior in production

**Human** can be very unreliable, causing ~75% failures by false operation rather than 10-25% of hardware outages.

**Methods**: 
1.	Well-designed **abstractions**, APIs, and admin interfaces make it easy to do “the
right thing” and discourage “the wrong thing.” (should reach a balance, not become too complex)
2.	**Decoupling** testing sandbox from prod.
3.	Thorough, full-grained **test**.
4.	Fast **recovery** / **rollback**, gradual **roll out**, logs and data **recomputation**.
5.	**Monitoring** on metrics (telemetry).
6.	Good **managing** and **training**.






