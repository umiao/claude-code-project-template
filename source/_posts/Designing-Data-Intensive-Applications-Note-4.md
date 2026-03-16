---
title: Designing Data-Intensive-Applications-Note-4
date: 2024-02-23 16:38:51
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on data model and query language."
key_concepts:
  - Data Models
  - MapReduce
  - Database Indexes
takeaways:
  - Choose relational models for many-to-many relationships and document models for self-contained records
  - Prefer declarative query languages over imperative code for data access
  - Use graph models when relationships between entities are as important as the entities themselves
  - Store IDs instead of plain text to enable consistent updates and localization
series: DDIA
series_index: 4
---
Discussion on data model and query language.
<!-- {% asset_img cover.png DDIA Chapter 4 cover: Data Models and Query Languages %} -->
<!-- more -->


### Concept of Data Model / Query Language:
We have the questions to answer: 
-	We want to build **abstraction**, one data model layer on top of another, but we need to know how one layer is represented by below layer.
-	**Data modeling** / **API assignment**. How to model the data, **JSON** / **XML**? **Table** in DB? **Graph Model**?

---

### Relational Model v.s. Document Model:
- **Relational**: Data organized into **relations** (called tables in SQL) and each relation is an **unordered collection of tuples** (rows in SQL). Hide details behind cleaner interface.
- **Document**: NoSQL, retrieve document by **name**, each stores information of one **object** and any of its related metadata. 
Examples: **JSON**, **BSON**, **XML**. 
A **collection** is a group of documents.  

Driving Forces behind NoSQL (Maybe **not only SQL** is more accurate):
-	Greater **scalability**, like very large dataset or very high write throughput
-	Preference for **free** and **open source** software over commercial database products
-	**Specialized** query operations not well supported by relational DB
-	Frustration with the restrictiveness of **relational schemas**, and a desire for a more dynamic and expressive data model

**Shortcomings** of document model: In document model, you cannot directly refer to some **nested** items (because it is not stored independently). Thus we should not use it when document structure is too complex / nesting is too deep. Also it has poor support for **Join**.

---

### Object-Relational Mismatch:
Usually, an awkward ***translation layer*** is required between the objects in the Relational Model (tables) Versus Document Model (sometimes named as **impedance mismatch**)

**Object-Relational Mapping** (ORM) like **ActiveRecord** and **Hibernate** can reduce the amount of boilerplate code, but the difference still exists (such mismatch)

**ID** can out-perform pure string in **Many-to-One** / **Many-to-Many** mappings.
Store fields as IDs and retrieve their values can help:
1.	Consistent **styling** 
2. **Avoid ambiguity** 
3. Ease of **updating** 
4. **Localization** support 
5. Better **search matching**

Both stroing by ID / storing by string has some sort of **redundancy**. 
- The previous is for **human**, meaningful info is stored in just one place and everything refers to it use an meaningless ID. 
- For string storage, you are **copying** the same values (might consume more storage).    
However, the benefit using ID is that you do not have to update ID, and can better enforce consistency when update is needed.

- In document model DB, such unifying can be hard as you may need to query DB for multiple times (Good at one-many, not good at many-one, many-many).

--- 
### Conference on Data Systems Languages (CODASYL) and the network model:

> Disclaimer: This may be something old and just material for fun

- Allowing an item to have **multiple parents** to model many-one / one-many
- The link is more like **pointers** (static pointers stored on the disk), follow a path to **traverse** (start from root record)  
- [This may be problematic in **many-many** cases, you need to maintain complex paths of data to update]


**Relational Model**:
- Relation (table) is simply a collection of tuples (rows), you can read any of the rows and select those matching your condition. 
- You can insert new row into table without thinking of foreign key issues (this is done in **query time** not in insert time)
**Key insight**: For relational DB, you only need to build a query optimizer **once**, and then all applications that use the database can benefit from it. 
If you don’t have a query optimizer, it’s easier to hand-code the access paths (a.k.a the **network model**) for a particular query than to write a general-purpose optimizer—but the general-purpose solution wins **in the long run**.

**Document model**: 
- Different from network model, as it uses unique identifier (**foreign key** in relational, **document reference** in documental) to link.

It is possible to use **denormalization** (add **redundant copies**, **grouping** data, etc) to reduce need of join (in relational DB), but it takes extra work to enforce **consistency**.

--- 

### Schemaless / Schema flexibility in Document Model

- In **JSON**, usually we do not support **enforcing** of any schema (there may be some schema, but not enforced by the DB). We may see any value / any key.
- **schema-on-read**: the structure of the data is implicit, and only interpreted when the data is read. Just like dynamic type checking rather than static type chekcing.
- This can be tricky for **MySQL**, as it copies the **entire table** when doing `alter table`.

---

### Data Locality of queries
1. May grant performance advantage if you want to access entire document frequently. 
(If in multiple tables, then may need more **disk seek time**)
2. Unless the modification does not change the **encoded size**, we usually need to rewrite **entire** document when making modifications. (thus should try to keep documents small)

This idea is beyond document database, also applicable to relational DB. 
- Google’s **Spanner database**: offers the same locality properties in a relational data model, by allowing the schema to declare that a table’s rows should be interleaved (nested) within a parent table. 
- Oracle: Offers the same using a feature called **multi-table index cluster tables**. 
- The column-family concept in the **Bigtable data model** (used in **Cassandra** and **HBase**) has a similar purpose of managing locality.
- More and more relational DB is adding support to JSON (allowing values to be **nested obj**, rather than only trivial values).

---

### Query Languages for Data:
#### Declarative
- SQL is regarded as **declarative**. 
- Just specify the **pattern** of result data you want, what **conditions** to meet, but not about **how** to receive this result. 
- Usually order is not guaranteed as well, but it is good for parallelization
- Details are hidden, and optimization can be done **without modifying** the query


#### Imperative
- **IMS** / **CODASYL** query are using **imperative** code. 
- Guide device to do certain operations in certain **order**. This can be harder to optimize / rewrite on multiple machines
- **HTML** is declarative as well. 
- **Document Object Model** (DOM) API is imperative instead (a bad rewrite using DOM API can be less interactive as it detect conditions & runs only one time).

#### Map-Reduce
- **Map-Reduce** can be in between of declarative and imperative, consisting of important operations of map (collect) and reduce (fold / inject). 
- Usually map func provides the **partial result**, and reduce func works on **aggregation**.   
- **Restrictions**: they have to be “pure” functions, no additional queries can be done, no side effect should be made (so that they can be executed in any time / any order). 

--- 

### Graph-Like Data Model: 
- Describe data with **Vertices** and **edges**.
- It is good for, e.g., describing **social network** and **hierarchical** relationships.

**Property Graphs**:  
- Each vertex consists a **unique identifier**, a set of outgoing edges, a set of incoming edges, a collection of properties (K-V pairs).
- Each edge consists of a unique identifier, the vertex which the edge starts, a label to describe the kind of relationship between the two vertices, a collection of properties (K-V pairs).

1. Any two vertices can be linked; 
2. You can find the incoming / outgoing edges for a vertex; 
3. You can use labels for different kinds of relationships, store different kind of info in a single graph. This actually allow us to store data in different **granular**.

---

### Cypher Query Language:
Demos an example of **creation** of a property graph:
{% asset_img 1.png Cypher property graph creation example %}
Example of **query**:
{% asset_img 2.png Cypher query example for graph traversal %}

- Such query effectively specify an **endpoint** / **destination vertex**, and we want to find a **path** to get there. 
- We first declare a person should have a “born_in” edge, then we want to keep tracking “within” edge to reach certain country / address vertex.
- **Application** in SQL: This can be difficult as the number of **“join”s** needed is not clear. You can use **RECURSIVE** syntax (used to enlarge the same table / set) for such purpose (but very complex and ineffective).


**Triple-Stores**: 
- Basically the same as property graph model, just using different words of: `(subject, predicate, object)`   
This just like `(in_vertex, directional_edge, out_vertex)`


### SPARQL 
A query language for triple-stores using the RDF (**Resource Description Framework**) data model. 
It looks like:
{% asset_img 3.png SPARQL query example for RDF triple-stores %}


### Datalog
Similar triple-stores languages, write as `predicate(subject, object).`
See example of decalration as well as query below:
{% asset_img 4.png Datalog declaration and recursive query example %}

It can also recursively find a person who born in USA and lives in Europe.
Note that in above example, rule “within_recursive” can derive **itself**. (You can view the first line of row as “tail recursive”)




