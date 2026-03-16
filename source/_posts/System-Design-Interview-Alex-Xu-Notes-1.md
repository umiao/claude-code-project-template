---
title: System-Design-Interview (Alex Xu) Notes - Chapter 1 - 3
permalink: system-design-interview-alex-xu-notes-1/
date: 2025-05-11 22:29:48
categories:
- [Job Search, Software Engineering]
tags:
- Interview
- Alex Xu
- System Design
description: Part 1 of notes from Alex Xu's System Design Interview book, covering chapters 1-3 on scaling from zero to millions of users, back-of-the-envelope estimation, and the system design framework.
key_concepts:
  - Scalability Patterns
  - Caching Strategies
  - Load Balancing
  - Database Sharding
series: System Design Interview - Alex Xu
series_index: 1
takeaways:
- DNS is typically a paid third-party service, not self-hosted
- NoSQL databases excel for super-low latency, unstructured data, and serialization needs
- Non-relational databases generally don't support join operations
- Separate database from web server as first scaling step
---
Learning note of Alex Xu's system design interview book.
{% asset_img cover.jpg System Design Interview Notes 1 cover: scaling from zero to millions of users %}
<!-- more -->

# SCALE FROM ZERO TO MILLIONS OF USERS 

**Trivial Case**: Web app, database, cache, etc run on a single server.

The **request flow**:

1. Users access websites through domain names, such as api.mysite.com. Usually, the
Domain Name System (**DNS**) is a paid service provided by 3rd parties and not hosted by
our servers.
2. Internet Protocol (**IP**) address is returned to the browser or mobile app. In the example,
IP address 15.125.23.214 is returned.
3. Once the IP address is obtained, Hypertext Transfer Protocol (HTTP) requests are
sent directly to your web server.
4. The web server returns HTML pages or JSON response for rendering.

There are 2 traffic sources:
• **Web application**: it uses a combination of server-side languages (Java, Python, etc.) to handle business logic, storage, etc., and client-side languages (HTML and JavaScript) for presentation.
• **Mobile application**: HTTP protocol is the communication protocol between the mobile app and the web server. JavaScript Object Notation (JSON) is commonly used API response format to transfer data

With growth of user, **database** may be needed. It receives read / write / update request, and returns data.

**Relational Database**: MySQL, Oracle, Postgre ... Query with SQL. 
**Non-Relational Database** (NoSQL): CouchDB, Neo4j, Cassandra, HBase, Amazon DynamoDB, etc. These databases are grouped into
four categories: 
- key-value stores, 
- graph stores, 
- column stores
- document stores. 

Join operations are generally not supported in non-relational databases.

**When to use NoSQL**: 
1. App requires super-low latency
2. Data unstructured, or no relational data.
3. Only needs serialize / deserialize. 
4. Massive data stored.

---

Vertical (Scale Up) v.s. horizontal (Scale Out) scaling: The prior upgrages machine while the latter adds server number.
**Vertical Scale**: Simple and great for low traffic. However it has hard limit, cannot add unlimited CPU and memory to single server; does not have failover and redundancy. Prune to single point failure. 
Therefore horizontal filtering is desirable for large scale applications.

---

## Load Balancer
A load balancer evenly distributes incoming traffic among web servers that are defined in a load-balanced set.
It can make servers unreachable in terms of public IP. Instead, they can use private IP (for machines in the same network) to communicate.

\*Should note that it only resolves web tier but not data tier. Database does not have redundancy yet. 

---

### Database Replication

Can be used in many database management
systems, usually with a master/slave relationship between the original (master) and the copies (slaves).

- Master generally only supports write ops (All insert / delete... goes to it). 
- Slave database gets copies of the data from the master and only supports read. Usually there are higher ratio of reads to writes, so there are usually more slaves than masters. 

Such design incurs better performance, reliability and availability. Down slaves may be replaced by others or master, and if master is down, we can elect a new one. 

---

### Improve the load / response time
We can achieve that by adding **cache** layer (temporary storage which stores the result of expensive responses) and shifting static content (JavaScript/CSS/image/video files) to content delivery network (**CDN**).

A cache tier should be much faster than the database, and we first check if cache has availablel response. If not, we then forward the request. This is called **read-through cache**.

**Consideration when use cache**:
1. Data is read frequently but is written infrequently. 
2. Cache is in volatile memory, not ideal for persisting data (No important data).
3. Should have **expiration** policy. Otherwise data may be stale.
4. Should keep data store and cache in sync for consistency (if data modifying operation on data store / cache are not in a single transaction). 
5. Recommend multiple cache servers across different data centers to avoid **Single Point of Failure** (SPOF). Also we can overprovide required memory for certain percentages to give buffer as the memory usage increases. 
6. When cache is full, we need **eviction policy** to replace data like Least-recently-used (LRU), Least Frequently Used (LFU) or First in First Out (FIFO). 


---

A CDN is a network of **geographically dispersed** servers used to deliver static content. 
The **closet** CDN server will respond the request.
If we got a miss, we will just query the server.
CDN servers cache static content like images, videos, CSS, JavaScript files, etc.

The result will be cached for Time-To-Live (**TTL**).

**Dynamic content caching** enables the caching of HTML pages that are based on request path, query strings, cookies, and request headers. 
\* Dynamic contents may vary by user behavior / location. To cache such content, we need to cache by request, and then cache the generated response as a **static** file.
\*\* Major difference is that, dynamic contents are generated from server rather being ready to deliver.

**Consideration when use CDN**:
1. Run by 3rd party providers, need to pay for data transfer (in and out). Infrequently used assets should be moved out of CDN.
2. Set proper expiry (TTL).
3. CDN **Fallback**: should be able to detect problem and request resource from origin.
4. **Invalidate** resources: either using CDN provider's API or use **object versioning**.

---

## Stateless Web Tier
A good practice is to store session data in the **persistent shared storage** such as relational database or NoSQL, allowing us to move state (for instance user session data) out of the web tier. 

Each web server in the cluster can access state data from databases. This is called **stateless** web tier (simpler, more robust, scalable).

\* If we design web tier to be stateful, then user's subsequent request must be sent (**routed**) to the previous same server.
(This can be supported by load balancer's **sticky session**)

We prefers the data storage to be NoSQL so that it is easy to scale. 
We can also apply **auto-scaling** (adding or removing servers based on traffic loads)

---

## Data Centers
It will be needed when certain application will server international traffic.
**geoDNS**: DNS service that allows domain names to be resolved to IP addresses based on the location of a user. Therefore it can geo-route the traffic.

### Challenges:
1. **Traffic redirection**: Effective tools are needed to direct traffic to the correct data center. GeoDNS can be used to direct traffic to the nearest data center depending on where a user
is located.
2. **Data synchronization**: Users from different regions could use different local databases or
caches. In failover cases, traffic might be routed to a data center where data is unavailable.
A common strategy is to replicate data across multiple data centers. 
3. **Test and deployment**: With multi-data center setup, it is important to test your
website/application at different locations. Automated deployment tools are vital to keep
services consistent through all the data centers.

To further scale our system, we need to decouple different components of the system so they can be scaled independently. 
**Messaging queue** is a key strategy employed by many real-world distributed systems to solve this problem.

---

## Message Queue

Durable component, stored in memory, that supports asynchronous communication.

It serves as a buffer and distributes asynchronous requests. 
- Input services, called producers/publishers, create messages, and publish them to a message queue. 
- Other services or servers, called consumers/subscribers, connect to the queue, and perform actions defined by the messages.

Allowing producer and the consumer to be scaled **independently**

---

## Logging, metrics, automation
- Logging: Monitor err logs, identify errs and problems. 
**Host level metrics**: CPU / Memory / disk IO
**Aggregate level metrics**: performance of entire database tier, cache tier.
**Key business metrics**: daily active users, retention, revenue

**Automation**: When system gets big and complex, need to build and leverage automation tools to improve productivity.
**Continuous integration**: each code check-in is verified through automation, allowing teams to detect problems early. Build / test / deploy process can also be automated.

---

**Vertical Scaling**: aka scaling up, adding more power to an existing machine (CPU / RAM / Disk / ...)
*Drawbacks*: hardware has upper limit; single point of failures; high cost.

**Horizontal Scaling**: sharding / scaling out. Add more servers. The separated smaller / easily managed parts are called **shards**, sharing the same (data) schema.
- *Consideration*: the sharding key, enabling efficient data retrieval and modification. Should be able to evenly distribute data.
- **Resharding** will be needed if: a single shard cannot hold more data; experience faster exhaustion than other shards. **Consistent hashing** is commonly used to solve this problem.
- **Celebrity / hotspot key** problem: Excessive access to a specific shard. We can allocate a shard for each celebrity (might even require further partition).
- **Join / De-normalization**: It will be harder to join, if a database is sharded across multiple servers. We can de-normalize the database so that query can be performed in a single table. 

---

## Scaling to Millions of Users
1. Keep web tier **stateless**.
2. Build **redundancy** at every tier.
3. Cache data as much as possible
4. Multiple data centers
5. Host static assets in CDN
6. Sharding
7. Split tiers into individual services
8. Monitor the system and use automation tools

# Back-Of-The Envelope Estimation
> “back-of-the-envelope calculations are estimates you create using a combination of thought experiments and common performance numbers to get a good feel for which designs will meet your requirements”

**Power of two**:
\*Unit in bytes. 
$2^{10} \approx$ Kilobyte = KB	
$2^{20} \approx$ Megabyte = MB	
$2^{30} \approx$ Gigabyte = GB	
$2^{40} \approx$ Terabyte = TB	
$2^{50} \approx$ Petabyte = PB	

**Common latency numbers**:
| Operation Name    | Time |
| -------- | ------- |
| L1 cache reference  | 0.5 ns    |
| branch mispredict | 5ns     |
| L2 Cache reference    | 7ns    |
|   Mutex lock / unlock  | 100ns    |
|   main memory reference  |   100ns  |
|   compress 1KB with Zippy  |  10μs   |
|   send 2KB via 1Gbps network  |  20 μs  |
|   Read 1MB sequentially from memory  |   250 μs  |
|    Round trip iwthin the same datacenter |   500 μs  |
|   Disk seek  |   10 ms  |
|   Read 1MB sequentially from network  |  10 ms   |
|   Read 1MB sequentially from disk  |   30 ms  |
|  Send packet CA -> Netherlands -> CA   |   150 ms  |

\* Avoid disk seeks if possible; Simple compression algos are fast; Compress data before send via internet; Data centers usually in different regions and therefore slow to send data between them. 

## Availability Numbers
**Service level Agreement** (SLA): defines the uptime delivered by service provider to customers. Cloud providers usually set it to 99.9% or above, measured in nines.
| Availability % | Downtime per day   | Downtime per year |
| -------- | ------- | ------- |
| 99% | 14.4 mins | 3.65 days |
| 99.9% | 14.4 mins | 8.77 hrs |
| 99.99% | 8.64 s | 52.6 mins |
| 99.999% | 864 ms | 5.26 mins |
| 99.9999% | 86.4 ms | 31.56 s |

### Estimate Example of Twitter
With 300M monthly active user, 50% use Twitter daily. User posts 2 tweets daily on average, 10% tweets contain media, data stored for 5 yrs.

Query per Second: 300M * 0.5 * 2 tweets / 24 hrs / 3600 seconds ~ 3500
Then Peek QPS ~ 2* QPS = ~7000 (This may not be a good estimation now)

Media storage: 150 M * 2 * 10\% * 1MB = 30TB per day, ~55 PB in 5 years

# System Design Framework
1. Do NOI jump right into a solution. Think deeply and ask questions to **clarify** requirements and assumptions. This may includes:
	- What specific features to build / Channels (web / mobile)?
	- How many users / how fast the company anticipate to scale up
	- Tech stack / existing services
2. Propose high-level design and get buy-in
	- Initial blueprint for design. Ask for feedback, treat interviewer as teammate and work together.
	- Draw **box diagrams** with key components (like clients / APIs / web servers / data stores / cache / CDN / Message Queue..)
	- Do back-of-envelope calculations to evaluate your blueprint fits the scale constriants; think out aloud. 
	- It depends on the cases, when it comes to whether designing API endpoints and database schema.
	**Examples**: For message publishing, traffic goes to certain API with `auth_token` from DNS, then into load balancer and sent to separate Post / Fanout / Notification service, and the prior 2 can have their own cache / DB. 
	For News feeding, we can just access the News Feed Service / Cache via similar path.
3.  Design Deep Dive
	After figuring out the prioritization (high / low level design, e.g. -) Avoid getting into the details which do not demonstrate your ability! 
4. Wrap up: a few follow-up questions or give the freedom to discuss other aditional points. 
	- Identify the system bottlenecks; discuss potential **improvements**. Critical thinking.
	- Talk about **error cases**, **operation** issues by monitoring metrics and err logs. How to **roll out** the system?
	-  Handle the **next scale curve**, how to support 10x users?

**Dos**: Ask for clarification; understand the requirement; No right or best answer (startup and grown companies have different demands); Share your thinking, give multiple approaches if possible; Go into the most critical component's details first; Try to work with interviewer as a teammate, never give up.

**Don'ts**: Don't be unprepared, jump into a solution without clarifying, or go into too much detail. Do high level design first, ask for hints when stuck. Ask feedback early and often (like follow-ups)

---

Time allocation: 
1. 3 - 10 mins understanding the problem, come up with design scope.
2. 10 - 15 mins Propose high-level design and get buy-in.
3. Design deep dive: 10 - 25 mins
4. Wrap: 3 - 5 mins.







