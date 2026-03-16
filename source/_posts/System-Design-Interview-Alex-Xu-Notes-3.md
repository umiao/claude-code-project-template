---
title: System-Design-Interview (Alex Xu) Notes - Chapter 4 - 9
permalink: system-design-interview-alex-xu-notes-3/
date: 2025-05-18 22:29:48
categories:
- [Job Search, Software Engineering]
tags:
- Interview
- Alex Xu
- System Design
description: Part 2 of notes from Alex Xu's System Design Interview book, covering chapters 4-9 on rate limiters, key-value stores, unique ID generation, URL shorteners, and web crawlers.
key_concepts:
  - Rate Limiting
  - Key-Value Store Design
  - Consistent Hashing
  - CAP Theorem
  - Web Crawler Design
series: System Design Interview - Alex Xu
series_index: 2
takeaways:
- Token bucket and sliding window are common rate limiting algorithms with different trade-offs
- CAP theorem forces a choice between consistency and availability when network partitions occur
- Twitter Snowflake approach divides ID bits into timestamp, datacenter, machine, and sequence sections
- Web crawlers must balance politeness, priority, and freshness when scheduling URL downloads
---
Continued notes from Alex Xu's System Design Interview book, covering system design problems from chapters 4-9.
<!-- {% asset_img cover.jpg System Design Interview Notes cover: rate limiters, key-value stores, and web crawlers %} -->
<!-- more -->

# Design a Rate Limiter
In HTTP, a rate limiter limits the number of clients requests allowed. If API request count exceeds, such excess calls are blocked.
Such components prevent resources starvation by **Denial of Service** (DoS) attack. Twitter allows 300 tweets per 3 hours; Google doc can do 300 read requests per user per 60 seconds.
It also reduce cost and prevent servers from being overloaded.

**Example**:
1. User can do <=2 posts per second, create <= 10 accounts per day from same IP. Can claim rewards no more than 5 times per week from same device.
2. Get clarification on the scale of system / focus / whether distributed / should be implemented as a separate service, and other requirements.
3. For example of rate-limiter, it can be put on client (Note that client may not be trustworthy due to malicious actor) or server side (inside the API). Or we can design a separate middle-ware rate limiter.
4. Cloud microservices have become widely popular, and rate limiting is usually implemented within a component called **API gateway** (fully managed, supports rate limiting, SSL termination, authentication, IP whitelisting, servicing static content..).
5. Tradeoffs of implementing the limiter on server side - against - at gateway. Consider programming language / business needs / can take benefits from reusing microservice arch / time or budget to determine.
6. **Algorithms** for rate limiting:
	- **Token bucket**: Refiller keeps adding tokens to a bucket (with pre-defined capacity) every second, and every request consumes a token. If there is not enough token, block the requests.  Usually we have different buckets for different API endpoints / user / IP.
	Easy to implement, memory efficient, allows a burst of traffic in short periods.
	Needs params: *bucket capacity*, *refill rate*.
	- **Leaking Bucket**: When a request arrives, check if queue is full, if not full, it can be added to the **First-In-First-Out** (FIFO) queue, otherwise it will be dropped. Requests are pulled from the queue and processed at regular intervals.
	Needs params: *bucket capacity*, *outflow rate*.
	\* The queue may be filled by old requests caused by burst of traffic.
	- **Fixed Window Counter**: divides timeline into fix-sized time windows, assign a counter for each. Each request increments the counter by one, once the counter reaches the threshold, drop new request until a new timewindow starts.
		*Cons*: Will allow more requests than allowed quota to go through (if there is a burst of traffic around round minute or second).
	- **Sliding window log**: Keep track of the request timestamps, keep in a cache like **Redis**. Remove all outdated (older than current time window) timestamps when a new request comes in, add new request's timestamp to the log. If the log size $\le$ allowed count, a request is accepted, otherwise it is rejected.
		*Pros*: Accurate measuring, ensure request won't exceed the rate limit.
		*Cons*: Consumes a lot of memory; rejected request may still have timestamp stored in memory.
	- **Sliding window log with counter algo**: Combines the fixed window counter and sliding window log. It estimates the number of request in the rolling window with the following formula:
	> Requests in current window + requests in the previous window * overlap percentage of the rolling window and previous window
	Given that right now we are at 30\% of the current miniute, we can estimate the request count in the rolling window (using 30\% of full previous minute's data).
	It smooths out spikes in traffic using average rate of previous window and is memory efficient; however it only works for not-so-strict look back window since it is based on estimation (but not too bad). Therefore it is a "soft" algo allowing more requests than designed to pass through.


## High level architecture
We need a counter implemented with fast in-memory cache (supporting time-based expiration strategy). It should offers commands: `INCR` (add stored counter by 1) and `EXPIRE` (delete the counter after the timeout).

Such system contains: client -> Rate limiter middleware -> (API server / Redis). Limiter fecthes counter from Redis, and check if the request is allowed (and send to APi servers).

Rules should be written into configuration files and svaed on disk.
API can return a HTTP code 429 (too many requests) in case of exceeding the rate limit. We can also enqueue the rate-limited requests to be processed later (if it is due to system overload).

**Rate Limit headers**: We can return information about whether a client is throttled / and remaining requests in current window.
We can use: `X-Ratelimit-Remaining`, `X-Ratelimit-Limit`, `X-Ratelimit-Retry-After` to express.

Full Design:


{% asset_img rate_limiter.png Rate_Limiter_design %}
- Rules stored on disk; workers frequently pull rules and store in cache. A rqeust will be sent to rate limiter first, which will fetch rules from the cache, and counters / last request timestamp from *Redis* cache.

## Rate Limiter in Distributed Environment
Major challenges include:
**Race Condition**: Two request may concurrently read counter value before either of them write the value back, causing $+1$ instead of $+2$.
	**Lock** should fix such race condition, but will slow down the system. **Lua script** and **sorted sets** data structure in Redis are commonly used to solve such problem.
	Lua script will be executed **atomically**, so we may use `ZINCRBY` to increase / `ZREVRANK` to get the rank. Other ops will be paused.

**Synchronization Issue**:
Single rate limiter may not be able to handle the traffic, so for large system, Synchronization is required.
We may use **sticky sessions** to allow a client to send traffic to the same rate limiter (sending traffic to the same rate limiter). However, it is not **scalable** / **flexible**.


1. **Performance Optimization**: Multi-data center setup is crucial as latency will be high for users located far away. Most clooud service providers build many edge servers across the world.
2. **Monitoring**: to make sure rate limiting algorithm / rules are effective. It should not let pass too many suspicious / too few valid requests.
3. Rate limiting can work on other levels other than **application** level. E.g., limiting by IP addresses using **Iptables**.
	Full layers of Open Systems Interconnection (OSI) model: Physical / Data link / Network / Transport / Session / Presentation / Application
4. Design client with best practices:
	a. Client cache to avoid making frequent API calls
	b. Understand and enforce the limit
	c. Enforce code to catch exceptions or errors
	d. Add sufficient back off time to retry logic.

## Consistent Hash
First construct a hash ring; Using hash function f, also map the servers to the ring evenly (usually the range $\in [0, 2^{160} - 1]$). For a request to find a server, find clockwise until one is found.
In case of add / change a server, only a fraction of keys need to be moved.
To better implement such algo, **Virtual Nodes** are introduced. With large number of virtual nodes and mapping them back to the real nodes, we no need to worry about the issue of non-uniform distribution and frequent change of key mapping.
\* It should be noted that the nodes / virtual nodes are also mapped to the hash ring using hash function, rather than spliting the hash space evenly. This ensures that no matter we add / remove virtual nodes, the distribution will always be random and we do not have to assign keys to different nodes globally (when adding or removing a node).
\*\* My understanding is that this is also about robustness. If we manually evenly divide the nodes, then removal / adding a single node will make the existing nodes become **sub-optimal**.

# Design a Key-Value Store
A **non-relational** database stroing each **unique** identifier as a key with the associated value (can be strings / lists / objects ...). It is usually treated as an **opque** object in key-value store.

Should implement the `put` and `get` operator.
Usually there are tradeoffs about read / write and memory usage.
Design **characteristics**: the size of k-v pair should be less than 10KB; Able to store big data; having high availability, scalability and automatic scaling; have tunable consistenty and low latency.

**Single server store**: Should be easy, keep everything in hash table in memory.
**Potential optimizations**: Data **Compression** and Store only **frequently** used data in memory and the rest on disk. Even with that, a signle server can reach its capacity very quickly.

---

**Distributed Key-value Store**: Distributes key-value pairs accross many servers;

**CAP** (Consistency, Availability, Partition Tolerance) Theorem: It is **impossible** for distributed system to simultaneously provide more than 2 of the 3 guarantees.

**Consistency**: consistency means all clients see the same data at the same time no matter which node they connect to.
**Availability**: availability means any client which requests data gets a response even if some of the nodes are down.
**Partition Tolerance**: a partition indicates a communication break between two nodes. Partition tolerance means the system continues to operate despite network partitions.

It means that we can only have the following 3 combos:
CP, AP and CA. However, due to the inevitable of network partition, we can only tradeoff between consistency and availability.

When network partition happens, and a node is dropped: if data is written to that node, other nodes will have stale data; Otherwise, the dropped node will be inconsistent.
1. Choose **Availability**: system keeps accepting reads, though stale data may be returned.
2. Choose **Consistency**: system block write operations to avoid inconsistency (bank systems);

Discuss with interviewer with such tradeoffs.

## Data Partition
We cannot fit complete dataset in a single server. To split into smaller partitions and store in multiple servers, we should consider the challenges of **evenly distribution** and **minimal data movement** when nodes are added or removed.

Consistent hash will be a good solution.

Advantages:
1. **Automatic scaling**: can automatically add / remove servers
2. **Heterogeneity**: number of virtual nodes be proportional to the server capacity.

## Data Replication
To achieve high availability and reliability, data must be replicated asynchronously over N servers, where N is configurable param.
For implementation, after a key is mapped to a position on hash ring, walk **clockwise** from that position to choose the first N servers to store data copies.
\* For virtual nodes, we may find $<N$ servers for N virtual nodes, we can continue until N distinct servers are found.
For better reliability, we can place replicas in distinct data centers.

## Consistency
**Quorum Consensus** can guarantee consistency for both read and write.
We can define $N$ replicas in total, and $W$ is the write quorum and $R$ to be the read quorum.
A write / read must be successfully applied to $W$ / $R$ different replicas to go through.
Strong consistency is guranteed if $W + R \gt N$.

**Examples**: $R=1$ enables fast read / $W=1$ enables fast write; We can tune the values of W/R/N to achieve desired consistency.

### Consistency Models
- **Strong consistency**: client never sees out-dated value. Not suitable for high availability demand, may block new Ops.
- **Weak Consistency**: may see stale value
- **Eventual Consistency**: specific type of weak consistency; given enough time, all updates will be propagated and replicas are consistent.  (Adopted by **Dynamo** / **Cassandra**, also the recommended solution in this case)

### Versioning as Inconsistency Solution
Treating each data modification as a new immutable version of data. Therefore we can use version to detect and reconcile conflicts.

**Vector clock**: [Server ($s_i$), Version ($v_i$)] pair associated with a data item. When data Item D is written to server $S_i$, the system will increment $v_i$ such vector exists; otherwise create new entry [$S_i$, 1]

We can detect conflict if such vector contains more than one element, example: $D_4([S_x, 2], [S_z, 1])$. We can get to know that the value is now $D_4$ and has the ancestor of server x's version 2 and z's version 1. By comparing the version number, we can determine if a conflict needs to be recorded.

**Downsides**:
1. Adds complexity to the client.
2. The [server:version] pairs could grow rapidly. We can set a threshold of length to remove the old pairs. \* Amazon did not encounter this issue so far.

## Failure Detection
Usually we need at least 2 independent sources of info to mark a server down. **All-to-all** multicasting is inefficient.

**Decentralized** failure detection: **gossip protocal**
1. Each node maintains node membershiplist, containing memberIDs and heartbeat counters, and such count increments periodically.
2. Each node periodically sends heartbeats to a set of random nodes, and the receiver updates the membership list.
3. If the heartbeat has not increased for a predefined periods, that member is considered as offline (such info can be included in the sent heartbeats).

Handling temporary failures: **"sloppy quorum"**
Choose  the first $W$ healthy servers for writes and first $R$ servers for reads, ignore the offline servers.
If a server is temporarily unavailable, another server will process requests and push back changes to achieve data consistency later. (called **hinted handoff**)

For cases that a replica is permanently unavailable, we can implement an **anti-entropy** protocal to compare each piece of data on replicas and update each replica to the newest version.
A **Merkle tree**[1] can be used for inconsistency detection and minimizing the amount of data transferred.
[1] Defined as a tree in which every non-leaf node is labeled iwth the hash of the labels or values (leave node) of its child nodes. Therefore allows efficient and secure verification of the contents of large data structures.

### Steps of Building a Merkle Tree
1. Divide key space into buckets (e.g. number of 4), each bucket is used at the root level node to maintain limited depth of tree.
2. After the buckets are created, hash each bucket using uniform hashing method, create a hash node per bucket.
3. Build the tree upwards till root by calculating hashes of children, then we can quickly identify inconsistency (inconsistent only if high level nodes' hashes disagree).
\* In real world, each bucket contains ~1K keys which is quite a lot.

## System Architecture Diagram
1. Clients communicate with key-value store through API of `get` and `put`
2. Coordinator acts as sa proxy between the client and key-value store
3. Nodes are distributed on a ring using consistent hash, system is completely decentralized so adding and removing nodes are automatic.
4. Data replicated at multiple nodes, no single point of failure.

Each node can be designed to have: client API / Failure detection / Conflict resolution / Failure repair / Replication / Storage engine...

**Write path**:
1. Write request is persisted to a commit log (write ahead log) on disk.
2. Data is saved in memory cache.
3. When the memory cache is full or reaches predefined threshold, flush data to SSTable (sorted-string table)

**Read path**:
1. First read the memory cache, if there is a miss, use bloom filter to determine which SSTable contains the key then read the data from the disk.

---

# Design Unique ID Generation in Distributed Systems
We aim to create a distributed unique ID generation system, which cannot be handled by the `auto_increment` in traditional database.

Collect demands (example): ID should be unique and sortable / not necessarily only increments by 1 / contains ~64-bit numeric values, be able to generate 10K IDs per second.

**Multi-master Replication**: we can let k servers incrementing their IDs respecitvely, with an interval of k.
**Drawbacks**: this approach cannot scale with multiple data centers; IDs do not go up with time across multiple servers; does not scale well when a server is added or removed

**UUID**: 128-bit number, hard to get duplicate generated due to the sparsity. Simple and no coordination needed, easy to scale.
**Drawback**: longer than our 64-bit design; do not go up with time; could be non-numeric

**Ticket Server**: We can use a centralized `auto_increment` feature in a single database server. We can have numeric IDs, easy to implement but only works for small-mediam scale and prone to single point failure.

### Twitter - Snowflake approach
Instead of generating an ID directly, we can **divide** an ID into different sections. E.g., 1 bit for sign; 41 bit for timestamp; 5 bit for data center ID ($2^5=32$ centers); 5 bit for machine ID ($2^5=32$ machines per center) and 12 bits for sequence number (set to 0 every ms).

For the timestamp, we can store $2^{41}-1 \approx 69$ years.
For sequence number, we can have $2^{12}=4096$ IDs per ms.

**Potential extra topics**: Clock synchronization; Section length tuning (how many sequence numbers to reserve); high reliability.

---

# Design a URL Shortener (tiny url)

Understand the problem: Map the original url with params into an alias. With a back of envelope estimation of about 100M urls generated per day; write operation per second $\approx 1160$, estimated read operations to be 10 times of the write operation; Expect the service to run 10 years and accumulate 365B records; average URL estimated to be 100 and storage requirement to be $365B \times 100 bytes \times 10 years = 365 TB$

The API is expected to be REST-style, the client should send a POST request to encode the original URL, should looks like `api/v1/data/shorten` with the original long URL.
Similarly, should have a GET endpoint to retrieve the long url back. Then we should use the Status Code of `301`: **Redirect** and points you to the full new Url.
\**Detailed difference*: 301 means permanent site moving and browser will cache such response and direct to the long URL server in the future; for 302 it is temporarily, so we will still request the URL shortening service in the future.
Both has pros and cons, and 302 can help track hte click rate / source of click, ...
It is also intuitive to just implement with **hash table**.

---

**Data Model**:
Since the data will likely not fit in the memeory, it is better to use a relational database. An ID as primary key and having the shortURL / LongURL as data fields.

**Hash Function Space**:
The potential hashValue should $\in [0-9, a-z, A-Z]$ containing 62 potential characters, then we want to find n such that: $\min 62^n \ge 365B$
Then 7 should be enough.

### Details of Hash Function Selection
1. **Hash + collision** resolution: We can just reuse popular hash function like "CRC32", "MD5" or "SHA-1" and just collect the first 7 chars. However, we may need to resolve hash collision by appending predefined string until no collision is discovered in our DB.
	\*It is expensive to query DB to check if a short url exists. We can use bloom filter to improve performance.
2. **Base 62 conversion**: By using our 62 possible characters, we can convert a binary number into our representitive. Then the short URL length is not fixed and we will then need a Unique ID generator. However, we have security concerns as next URL is predicatable.

Potential **follow-up topics**:
Rate limiter (malicious user may send overwhelming / invalid URLs); Web server scaling (adding more servers providing such service); Database scaling (replication and sharding); analytics (answer related data analytic questions like how many people clicked on link / what do they do..) and again the Availability / Consistent and Reliability topics.

---

# Design a Web Crawler
Crawler (robot / spider) is widely used to discover new / updated content on the web. We can start by collecting a few web pages and then follows link on those pages to collect new content.

Some use cases: search engine indexing; web archiving; web mining (for knowledge and oppurtunities) and monitoring (copyright and trademark infringments)

**Understanding and scoping** the question:
Example: After clarifing about the main purpose, web pages amount per month, content type, whether should consider newly added pages and retention (time to store) and policy regarding duplicative contents. We can get some similar back-of-envelop estimation like 1B / month = 400 pages / sec.
We can then estimate the QPS to be 400 pages per sec, and peak QPS to be twice: 800. Assume the average web page size to be 500k then per month we will have 500 TB storage. For 5 years of content there is going to be 30 PB of data.

Extensive **discussion topic**: *Scalability* (efficient with parallelization) / *Roubustness* (against bad page / crashes / malicious links..) / *Politeness* (compliance and prevent DOS) / *Extensibility* (support new content types)

High Level Design:
{% asset_img crawler_1.png crawler_design %}

**Seed URLs**: We need seeds to start with, e.g. university webpage's domain name. We can also try to divide entire URL spaces into smaller ones to see if they are accessible. Also we can pick seed URLs based on topics. (open-ended question)

**URL Frontier**: Many modern crawlers spit the crawl state into: to-be downloaded and already downloaded. The prior part is called URL *Frontier*, view as a First-in-First-out queue.

**Downloader**: provided by the Frontier.
**DNS Resolver**: get corresponding IP by parsing the URL.
**Content Parser**: Parse and validate web pages. Also we need to check if content / URL is already seen to avoid saving duplicative results (by comparing hash). Also consider implement blacklisted sites there.
**Content Storage**: Mostly disk based, and keep popular contents in memory to reduce latency. Consider data type, size, access frequency, life span, etc.
**URL Extractor**: Parses and extracts links from HTML pages. Also need to convert relative paths to absolute URLs.

### DFS v.s. BFS
In most cases DFS may not be a good choice since the depth can be really deep, so BFS is more commonly used (implemented by FIFO queue).

**BFS Concerns**: most links from the same web page are linked to the same host, causing the crawler tries to download web pages in parallel from the same host and therefore "impolite".
Also, we need to prioritize pages according to their page ranks / web traffic / update frequency, etc.

### URL Frontier
- **Politeness**: Avoid sending too many requests to the same hosting server within a short period. Can download one page at a time from the same host, and a delay can be added between 2 download tasks. Can maintain a mapping from website hostnames to download (worker) threads, make sure that one host crawled at a time.
	**Queue router** ensures that each queue only contains URL form the same host, and mapping table maps worker to a queue.
- **Priority**: We should prioritize URLs based on usefulness (page rank / traffic / update frequency, etc). For multiple queues with priority, we can use a selector to randomly choose a queue with a bias towards queues with higher priority.
- For URL Frontier, the front queues manage **prioritization** and the back queues manage **politeness**.

**Freshness**: Web pages are constantly updated, so recrawl periodically is needed. We can recrawl by web pages' update history or prioritize important pages first and more frequently to optimize such process.

---

As there may be hundreds of millions of URLs in URL Frontier, we can use a disk - memory hybrid approach for storage. We can maintain buffers in memory for enqueue / dequeue operations and data in buffer can be periodically written to the disk.

### HTML Downloader
Robots.txt, called Robots Exclusion Protocol is a standard used by websites to communicate with crawlers. It specifies what pages crawlers are allowed to download, and we should comply wiht that.
It also helps with performance optimization.

Crawl jobs are distributed into multiple servers for performance reasons. The URL space can be partitioned and distribute to workers.

### Cache DNS Resolver
DNS resolver can be bottleneck for crawlers because DNS requests might take time due to synchronous nature of DNS interfaces (takes 10-200 ms). Once a request to DNS is carried out, others are blocked until the first request completed.
By maintaining cache, we can avoid calling DNS frequently.

Also, we can consider optimize by distributing crawl servers geographically (to ensure **locality**, closer to the hosts)
This applies to most of the system components.

We should also set a **short timeout** to avoid waiting for a page for too long.

---

**Robustness**:
Aside from performance optimization, we can also use: **consistent hashing** to distribute loads among downloaders; save **crawl states and data** for failure recovery; we also need **exception handling** and **data validation**.

**Extensibility**:
We can further plugin media resources download module / add Web Monitor module to prevent copyright and trademark infringements.

Avoid **Problematic Content**:
1. **Redundant** content (using hashes and checksums to dedupe)
2. **Spider trap**: inifinite loop / infinite depth directory certain webpages may have. We can set a maximal length for URLs, and user can manually verifiy and identify a spider trap.
3. **Data noise**: Ads, code snippets, spam URLs which have no value.
