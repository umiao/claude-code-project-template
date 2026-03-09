---
title: Designing Data-Intensive-Applications-Note-7
date: 2024-02-24 10:07:04
categories:
- [Data Science, Data System]
tags:
- DataScience
- Data System
- Designing Data-Intensive-Applications
---
Discussion on techniques related to data warehouse / OLAP.
{% asset_img cover.png ML_note %}
<!-- more -->

### Transaction:
- A bunch of operations, not necessarily having **ACID** (**atomicity**, **consistency**, **isolation**, and **durability**). 
In fact, it just allows low-latency read / write comparing with batch processing jobs (this is more widely used by **analytic** purpose, rather than serving customers).
#### Online Transaction Processing Systems (OLTP System) 
- Small number of records read per query
- Fetch by key
- Random access and low-latency write based on user input
- Serve end-users via web application
- Based on latest state of data, usually have dataset from GB-TB


#### Online Transaction Analytic Systems (OLAP System) 
- Aggregate read on records
- Bulk or event stream write
- Used by internal analyst for decision support
- Data based on history of events; dataset from PB – TB as it is history data

---

### Data Warehouse
- Company has the trend to stop analyzing on **OLTP** database, instead on separate database (running analytic queries on **OLTP** can be **expensive**, and harm the **performance**, as they should be low-latency and has high-availability).
- Thus we expect data warehouse to be separate from OLTP, read-only, get stream of updates and transform them into an anlysis-friendly schema, clean and load to data warehouse. This is called **Extract-Transform–Load** (ETL). 
The information source can be from multiple databases.  
\* Indexing optimization discussed above may work well for OLTP, but **NOT** for analytic queries.
- Data warehouses are common to be **relational**, as SQL is generally a good fit for analytic queries. 

There are many graphical data analysis tools that generate SQL queries, visualize the results and explore data like:
- **drill-down** (navigate from high-level summary to more detailed level, break down aggregated data into more granular levels) 
- **slicing** (select a subset of data based on specific criteria or dimensions)  
- **dicing** (like slicing, bat invloves selecting and analyzing data based on multiple criteria / dim). 

---

### Stars and Snowflakes: schema for analytics:
- Raw data tables are linked to **Fact Table**. Certain row in that table indicates certain events, e.g., when and where an item is sold at which price. Some columns in that table are attributes, and some are foreign key references (called **dimension table**, indicating event’s who, what, where, when, how, and why).
- **Star Schema** (dimensional modeling): the fact table is the center and connection to other tables are like the rays of the star. 
[**Easier** to use]
- **Snowflake Schema**: dimensions are further broken into **sub-dimensions**. In some table like product table, each row can reference foreign keys to represent brand & types, rather than stroing them as string. 
[More **normalized**]

---


### Column oriented storage:
- Fact tables can be very **large** (trillions of rows) but dimension a tables are usually much smaller (millions of rows). 
Fact table can have a lot of columns, but we usually only access **a few** of them at a time. 
Based on the above facts, unlike most OLTP databases (including document databases) whose stroage is laid out on **row-oriented** fashion, we can instead all values from each column together.    
- This helps reducing the overhead by **NOT** loading the not requested columns. 
Note that the column-oriented storage layout relies on each column file containing the rows in **the same order**.
- **Parquest** is a **columnar storage** format that applies to non-relational data as well, supporting a document data model.
- **Column compression**: The value sequences in many columns are quite **repeatitive**, indicating that compression can be used. An effective technique is **bitmap encoding**. Follows a graph about how bit map works:

In the following example, we have 18 rows and 6 possible column values, so we can use 1 bit to store the **occurrence** of a certain value. It is possible to be further reduced by **run-length encoding**.   It is especially efficent when we want to do **boolean computation** on a few values.

{% asset_img 1.png ML_note %}

- **Sort Order**: In column storage, the order may not matter, but we can force certain (meaningful) column to be ordered and use it as **indexing mechanism**.   
This can also help **compressing** the column, as we can use **run_length** encoding for sorted column.    
It needs to be noted that such compression has the best performance on the **first** sorted key, e.g., secondary key will be group by the first key so we will not have so many duplicate values.

- It may be a good idea to store multiple copies of data, sorted in **different** way. In that way we are adding **redundancy** and being able to further **optimize** queries.  
- The idea is like secondary indexing, but the different is that index is usually stored in **one place**, and only pointer / offset is stored, but in this way, the **values** got duplicated as well.  

[Note that such optimization makes **write** harder, compression is even impossible for **in-place** methods like B-Tree]  
This can be optimized by **LSM tree**, which accumulate enough writes (first add to memory and added to sort structure), then to be updated to disk in **batch**.

---

### Memory bandwidth and vectorized processing
Potential concerns include: 
1. Memory bandwidth
2. The bandwidth from main memory into the CPU cache
3. **Branch mispredictions** and **bubbles** in the CPU instruction processing pipeline
4. Make use of **single-instruction-multi-data** (SIMD) instructions in modern CPUs.


- Column-oriented storage layouts are good for making use of **CPU** cycles, while reducing the volume of data needed to be loaded from **disk**. 
- For example, the query engine can take a **chunk** of compressed column data that fits
comfortably in the CPU’s **L1 cache** and iterate through it in a **tight loop** (that is, with
no function calls). 
- A CPU can execute such a loop much faster than code that
requires a lot of function calls and conditions for each record that is processed. 
- Column compression allows more rows from a column to fit in the same amount of L1 cache. 
Operators, such as the bitwise **AND** and **OR** described previously, can be
designed to operate on such chunks of compressed column data directly. 
This technique is known as **vectorized processing**

---

### Materialized aggregate:
- Rather than handling raw data every time, we can use **materialized view** to cache some counts / sums which are frequently used.
- Difference with **standard (virtual) view** in relational database: materialized view are values of query result written to **disk**, while virtual view is just some stored **queries**.
- When underlying data changes, materialized view needs to be updated as it is a **denormalized copy** of the data. 
This comes with higher **write cost**, making it not often used in OLTP databases. 
They are more valuable in **heavy-read** data warehouses.
- **Data Cube / OLAP Cube**: a grid of aggregates grouped by different dimensions.

{% asset_img 2.png ML_note %}


