---
title: Designing Data-Intensive-Applications-Note-5
date: 2024-02-24 00:38:40
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on Storage structures."
key_concepts:
  - LSM-Tree
  - B-Tree
  - Database Indexes
takeaways:
  - Use LSM-trees for write-heavy workloads and B-trees for read-heavy workloads
  - Understand write amplification tradeoffs when choosing storage engines
  - Apply log segmentation and compaction to manage append-only storage growth
  - Use write-ahead logs to ensure crash recovery for both LSM-trees and B-trees
series: DDIA
series_index: 5
---
Discussion on Storage structures.
<!-- {% asset_img cover.png DDIA Chapter 5 cover: Storage Structures and Retrieval %} -->
<!-- more -->


### Storage and Retrieval:
Real life DB may need **concurrency control**, **reclaiming** disk space so that log does not grow forever, handling **errors** and **partially** written records.
- **Log**: an append-only sequence of records.
- **Index**: additional structure that is derived from the primary data (faster read, slower write)
- **Hash Indexes**: basic implementation is to use in memory hash map to store byte offset (then you can generalize memory hash map into disk hash).


### Log run out of space: 
To cope with such risk, we can: 
- Break log into **segments** of a certain size, 
- Closing a segment file when it reaches certain size
- Make subsequent writes to new segment file. 
We can do **compaction** on segments to keep only the **most recent** data (this may even allow us to compress **multiple** segments into one).

---

### Good Practice in storage: 
1. Store file as **binary** format, first encode length of a string in bytes, followed by the raw string 
2. Consider **tombstone** (special delete record) to avoid really deleting records ("delete" execute on read time). 
3. **Crash recovery**: in memory cache will lost, we can consider storing a **snapshot** of each segment’s hash map on **disk**, which can be loaded into memory more quickly. 
4. **Partially written result**: we can keep **checksums** to detect corrupted parts. 
5. **Concurrency control**: we need the log to be strictly **ordered**, so better have **one** writer thread only. 
6. **Reason of Append Only Design**: Appending and segment merging are sequential write operations, which are generally much faster than random writes, especially on **magnetic spinning-disk hard drivesor** even **flash-based solid state drives** (SSDs). 
Crash recovery will also be easier as values will not be partially overwritten. 
Also we can avoid **fragmented** data file.

***Shortcomings of hash table index***: 
- It relies on memory, and performs poor on range queries. 
- You have to go through **all** keys. 

---

### SSTables and LSM-Trees:
- If we further require writes of segment files to be **sequential** (sorted by key), then it is a **Sorted String Table** (SSTable).
- **Advantages over hash indexes**: Easier to merge segments as they are ordered (applicable to **merge sort**). 
- **Tiebreak**: if multiple keys exist, we only keep the latest record. (similar as the idea of using timestamp / ItemID as additional rank keyword)
- **Sparse Index**: Now that we do not need to keep all keys’ indexes, as we can use similar idea of **interpolation**. As the storage is now ordered, we only need to find out the **interval** where a key might exist. Maybe we can keep an index every few KBs (like paging). Also it is possible to compress multiple keys into a **compressed block**. To save disk space / IO cost.
- **Maintenance**: it is possible to maintain SSTables in disk (using **B-Trees**) but it is easier using memory (called **memtable**) with **red-black trees** / **AVL trees**.


{% asset_img 1.png Diagram of SSTable and LSM-Tree structure with memtable %}

--- 

### Memtable 

- When memtable gets bigger than threshold (a few MBs), write it to disk as an **SSTable** file, and the new SSTable file becomes the most recent segment of database. 
- While writing to disk, writes can continue to a **new memtable instance**.   
- When serving reads, try to find key in the memtable, then in **reversed order** to check on-disk segments (check the latest ones first)   
- Run **merging** and **compaction** process from time to time to merge segment files, and remove out-dated values. 
**Recovery of memtable**: memory is not persistent, so keep a separate **log** on disk to record every write to restore crashed memtable (**discard** records after such restoration).

--- 
### LSM-Tree: details and optimization: 
1. MemTable resides in memory, is **NOT** persistent, and ordered by key. Can enhance reliability by **Write-Ahead Logging** (WAL).
2. Memtable turn into **Immutable** Memtable after reaching certain size, and no longer writable. New memtable will handle write request, and Immutable Memtable is **pending transit to SSTable**.
3. SSTable is LSM-Tree’s data structure in disk. Can be optimized using **bloom-filter** and **indexes** on key. Note that the updating of disk is journal / log like, and the write is also in order. The write performance is improved, however there lies **redundancy** due to out-dated data (that is why we need compact).  Also query needs to be in **reverse order** as that is the latest.

### Compact Strategy:  
Because we have **amplified** read / write / space, that is to say, we are reading (two level read of MemTable / SSTable) / writing (Compact may be triggered so we are writing more) / storing (due to redundancy) **more** data than actually needed.

**Size-tiered**: Each tier of SSTable has similar size, and **restrict number** (N) of SSTable in each tier. If the number of SSTables reach N, then compact them and pass to next tier. 
(This will result in **huge** SSTable in deeper level) 
(Also for same tier SSTables, each key may has multiple records)

**Leveled**: Each level restricts the **gross size** of SSTables, and in the same level, slice data into SSTables with similar sizes. However, the SSTables are guranteed to be **globally ordered** so only stored once. 
**Strategy**: if a level exceeds the limit on size, then take out 1 SSTable, merge it with next level SSTables which have intersection. (This process can be recursive if still exceeds the size limit)

---

### Make LSM-tree out of SSTables:
- This is used by key-value storage engine like **LevelDB** and **RocksDB**.
- Known as **Log-Structured Merge-Tree** (LSM-tree).

**Instance**: **Lucene** (mapping from term to postings kept in SStable-like sorted files), is an indexing engine for full-text search used by **Elasticsearch** and **Solr**. It uses a similar method for storing its term dictionary.   
The mentioned full-textr search engine actually stores all links related to a keyword as key, with list of resources as the value.

---

### B-Tree

- Standard index implementation in **almost all** relational databases
- Instead of break database into variable-size segments and always write sequentially, B-Tree break into **fixed-size** blocks / pages (traditionally 4KB) and read or write one page at a time. It is more close to hardware, and each page can be identified using an address, stored on disk.
#### Implementation
- Starting from the root, keep going down to narrow the range of indexes and eventually check existence.
- The number of references to child pages in one page of the B-tree is called the **branching factor**, usually a several hundred.
- To update a key, search for leaf page containing that key and write back. 
- To add new key, find the page whose range **encompasses** the new key and add it to the page. If there is not enough space, split the page into 2 **half-full** pages. 
- This ensures that the tree is **balanced**, has a depth of $O(\log n)$. Most database can fit in a depth of 3 – 4. (A four-level tree of 4 KB pages with a branching factor of 500 can store up to 256 TB)

{% asset_img 2.png OLAP data cube / materialized aggregate grid diagram %}

- **Comparing with LSM-Tree**: B-Tree’s rewrite is **in-place** and can be viewed as happening at **hardware level**, rather than on log level.
#### Robustness
 - If you **split** a page because an insertion caused it to be overfull, you need to write the two pages that were split, and also overwrite their **parent page** to update the references to the two child pages. This is a **dangerous** operation, because if the database crashes after only some of the pages have been written, you end up with a corrupted index (e.g., there may be an orphan page that is not a child of any parent).      
 - **Solution**: Include an additional data structure of **Write-Ahead Log** (WAL) (**redo log**), which is append-only file which records every B-tree modification **before** it applied to the pages. This can restore B-Tree to a consistent state.
 - Also,  if multiple threads want to access B-Tree, we will need **lightweight locks** for consistency, which is more complex than log-based structure.

#### Optimizations
1. Can replace WAL with a **copy-on-write** scheme. That is a modified page is written to a different location, and a new version of the parent pages in the tree is created to **point at** the new location. This is also useful for concurency control. 
2. We can save space in pages by **abbreviating** the keys, as we only need enough information to act as **boundaries** between key ranges (e.g., **omit** common prefixs).  Thus we can have higher branching factor and fewer levels. 
3. We can try to layout the tree that leaf pages appear in **sequential** order in disk to save disk seeking time. However, it is difficult. For LSM-trees, such locality is easier as it rewrites large segments during merging.


#### Comparison with LSM-Tree:
- LSM-tree is faster in **write**, and B-Tree is faster in **read**.
- B-tree must do write twice: once to **WAL** (Write-Ahead Log) and once to the tree page itself (need more when split is needed). Need to change a page at **minimum**. Some storage engines even overwrite the same page twice in order to avoid ending up with a partially updated page in the event of a power failure. 
- Log-structured indexes also write data multi-times due to repeated compaction & merging (**write amplification**), impacting SSD; disk bandwidth is also limited and may cause **fragmentation**.
- LSM-tree usually has smaller write amplification as it do not have to overwrite several pages in the tree. Also, **magnetic hard drive**’s sequential writes is much faster than random writes, giving LSM-tree more advantage. 
However, the compaction can impact read-write performance (due to limited **disk bandwidth**), even storage engines try to perform compaction incrementally and without affecting concurrent access. 
Initial write and compaction will share the same bandwidth. As database become larger, the compaction is less effective and may be the **bottleneck** of performance / use up the disk space (write is usually not restricted in SSTable-based storage). 
For high-percentile, LSM-tree can have **high response time** and less predictable.
- Many SSD firmware will use log-structured algo to turn random writes into sequential write.


















