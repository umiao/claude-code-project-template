---
title: System-Design-Interview (Alex Xu) Notes - Chapter 10 - 12
permalink: system-design-interview-alex-xu-notes-2/
date: 2025-06-23 14:35:37
categories:
- [Job Search, Software Engineering]
tags:
- Interview
- Alex Xu
- System Design
description: Part 3 of notes from Alex Xu's System Design Interview book, covering chapters 10-12 on notification systems, news feed design, and chat systems.
key_concepts:
  - Notification System Design
  - News Feed Architecture
  - Chat System Design
  - Message Queues
series: System Design Interview - Alex Xu
series_index: 3
takeaways:
- Use message queues to decouple system components for independent scaling
- Implement notification logs and retry mechanisms to prevent data loss
- Avoid single points of failure by distributing databases and caches
- Notification templates reduce errors and save development time
- Third-party service extensibility is critical for global deployment
---
Learning note of Alex Xu's system design interview book.
{% asset_img cover.jpg System Design Interview Notes 2 cover: notification systems and distributed architectures %}
<!-- more -->

# Design a Notification System
We may need to have various types of notifications, like mobile push / SMS message / Email.

## Understand the problem and establish design scope
We expect it to be soft real-time, while receiving notifications as soon as possible. We want to support iOS devices / Android deivce / laptop & desktop. Notification should be triggered by client application or can be scheduled from the server side. User should be able to choose to opt-out and estimate the number (e.g. 10M mobile push, 1M SMS messages and 5M emails)


1. **iOS push Provider**: builds and sends notification requests to *Apple Push Notification Service*, given the Device token and a JSON like Payload. Finally, iOS sys can receive the notification.
2. **Android push notification**: Firebase Cloud Messaging is commonly used.
3. **SMS Message**: Consider using third party SMS services like Twilio / Nexmo, etc.
4. **Email**: Companies can homebrew their email services or opt for commercial services like Sendgrid or Mailchimp.
5. **Contact info gathering flow**:  When user installs app or signs first time, API servers collect user contact info and stores in database (request -> load balancer -> API servers -> Database).
		Note that user can have multiple devices, by splitting user - device table, a push notification can be sent to all user devices.

6. **Notification sending / receiving flow**: 
		For the high-level design, we consider multiple services going into the notification system and then distribute to different (internal or external) services for notification serving. 

		**Service 1 to N**: A service can be micro-servce / cron job / distribute system that triggers notification sending events. 

		The **notification system** provides API for service 1-N, and builds notification payloads for third party services.

		**Third-party services**: The **extensibility** is important, making it easy to plugging or unplugging. E.g., if certain service is unavailable in new markets like China, we should find alternative.

7. A **single** notification server means single point of failure, and hard to scale the databases, caches and different notification processing components independently. Also, processing and sending notifications can be resource intensive. It may not be a good design to handle everything in a single system.
		*Improved solution*: Move the database and cache out of the notification server; add more servers and set automatic horizontal scaling; introduce message queues to decouple the system components.  

The **process** of notification sending:
[Service calls API provided by notification servers to send notifications] -> [Server fetches meta data like user info / device token / setting from cache or DB] -> [notification event to be sent to corresponding queue for processing] -> [workers pull event from queue and send to 3rd party services] -> [3rd party serve request and send to user devices]

## Design Deep Dive
### Reliability
1. **Prevention of data loss**: notification can be delayed or reordered, but never lost. We can implement a **notification log** database and have a **retry mechanism**.
2. Recipients may receive notification for **more than** once. Deduplication may be needed due to the nature of distribted system. We can check the eventID when an notification event arrives, if it is seen before, discard it. [This may be unreliable, client end failure may cause stale notification be digested]
3. We can utilize **notification template** to avoid building every notification from scratch. Then we can just customize params / styling / tracking links / etc. Example: `You dreamed of it. We dared it. [ITEM NAME] is back — only until [DATE].`
We can therefore reducing margin error and save time.
		We may need notification setting to check if user is opted-in, before actually sending such notification.
		Also, we may need to **limit** the notification frequency.
4. In case of 3rd party service failure, we need **retry** mechanism. 
5. Also we need to enhance **security** in push notification API, e.g., with the native `appKey`, `appSecret` for **authentication**.
6. We also need to **monitor** key metrics of the notification services, e.g., total number of queued notification. If it is too big, more workers are needed.
7. **Event tracking**: check the open rate / click rate / engagement, etc. We can also track potential errors and unsubscribe behavior. 


# Design a News Feed System
News feed may include updates / photos / videos / links / app activity / likes from people.
**Similar** questions: design Facebook news feed / Instagram feed / Twitter timeline, etc

Align on problem stating and scoping: 
1. Check if it is mobile / web app, or both.
2. Core features should be publishing and seeing posts on news feed page. It should be in certain order like **reverse chronological** order. Feed may contain media files.
3. Clarify on how many friends a user can have (5K), and the traffic volumn (10M DAU).

## High Level Design
1. **Feed publishing**: when user writes a post, write into caches and database. Then populate to all friends' news feed.
2. **Newsfeed building**: Just aggregate all friends' posts in reverse chronological order for simplicity. 

**API design**: should be HTTP based, allow clients to post / retrieve news feed / add friends, etc
1. Feed publishing: `POST /v1/me/feed`, with params: `content`(text of post) and `auth_token`(to authenticate) 
2. Retrievel: `GET /v1/me/feed`, also has `auth_token` as params.

Such requests should be sent to load balancer from client, then web servers can handle such requests with modules: **Post Service** (write into post cache and database), **Fanout Service** (write into news feed cache) and **Notification Service**.

### News Feeding
A user sends a request to receive news feed, portal should looks like `v1/me/feed`. Through load balancer the traffic is directed to the webserver; then query through Newsfeed service and cache to get the news feed.
For a deep dive, Web servers will further call the **Post Service** (broadcast through post cache and DB) and **Fanout Service** (delivering a post to all friends).

Web server should also enforce authentication and rate-limiting. Only allow users with valid `auth_token` to make post.

**Fanout Service**:
1. We have two modes, fanout on write (**push** mode) or fanout on read (**pull** mode).
2. For Fanout on write, news feed is pre-computed during write time, and a new post is delivered to friends cache immediately after it is published.
	**Pros**: generated in real-time, pushed immediately; fast news feed
	**Cons**: If one has many friends, it will be slow and time consuming. (**hotkey** problem); for inactive users, such strategy causes waste.
3. For Fanout on read: a on-demand model, posts are pulled when user loads home page.
	**Pros**: save resource for inactive usres; no hotkey problem
	**Cons**: Fetching news feed will be slow
4. Recommend a hybrid approach; use push model for majority of users and for celebrities, we use the pull model to make sure it is on-demand. Consisstent hashing is also useful. 
5. **Service design**: The service can get friend ids from graph db (managing friend relationship & recommendation); friends data can be stored (User - DB) (we can later filter on friends using user setting); Then we can go through the message queue - fanout workers - News feed cache (sending the friends list and new post ID (storing the post content may be too large) to the message queue, and use cache for optimizing the news feed). 
\* Uses are more likely to browse latest feeds and scrolling to thousands of news feed's chance is low.

---

***News feed retrieval***
1. **User journey**: User sends request through load balancer and web servers, then servers call the news feed service to fetch news feeds. The service will get a list of Post IDs from the cache to serve the request. A user's news feed should also contains useranme / profile picture / post content, image, etc. We can then fetch and complete post objects from cache, and return in JSON format to the client.

The cache can be further tier into 5 layers:
- Layer 1: News Feed: [News Feed *(storing IDs of News feed)*]
- Layer 2: Content: [Hot Cache *(popular content)*, Normal]
- Layer 3: Social Graph: [follower, following *(user relationship data)*]
- Layer 4: Action: [like, reply, others]
- Layer 5: Counters: [like counter, reply counter, other counters]

**Scaling** methods: Vertical scaling v.s. horizontal; SQL v.s. NoSQL; Master - slave replication; read replicas; consistency models & dataset sharding. 

**Other topics**:
1. Keep web tier stateless.
2. Cache data as much as you can
3. Support multiple data centers
4. Loose couple components with message queues
5. Kry metrics monitoring, like user behavior related performance metrics.

# Design a Chat System
Whatsapp / Facebook messenger / Wechat / Line / Google Hangout and Discord are some popular chat systems. 
It is important to nail down the exact requirement (like solo chat v.s. group chat).

**Example design scope estmatblishment**: 
It should support both 1-1 and group chat (with low latency); use multiple channels, support 50M DAU, allow 100 people in a group;
Aside from that, text length should be $\le$ 100K characters long, check if end-to-end encrption is required. Should store chat history forever.

## High Level Design
Clients should not chat to each other but should connects to a chat service. 
**Related functions**: receive messages from other clients; find right recipents, and if a recipient is not online, hold messages on server until it is back.

For staring a chat, connects the chats service using one or more network **protocols**. For a chat service, the choice of network protocols is important.

It is commmon for clients to use HTTP protocol (a fine option on the sender side) to send messages to each other, informing the service to send message to the receiver. 
\* `Keep-alive` header allows a client to maintain connection with the chat service, and reduces number of TCP handshakes.

\*\* Receiver end may be more complicated. HTTP is client-initiated, and not tirvial to send messages from server. We can simulate server-initiated connects using: **polling** / **long polling** / **webSocket**.

1. **Polling**: Periodically asks the server is there are messages available. Can be costly depending on the frequency. 
2. **Long Polling**: a client holds the connection open until there are actually new messages or a timeout threshold reached. Once the client receives new messages, it immediately sends another request to ther server to restart the process.
	**Drawbacks**: sender and receiver may not connect to the same chat server, such servers are usually stateless. E.g. if use round robin for load balancing, server received message may not have a long-polling connection with the client.
	Also, a server has no good way to tell if a client is disconnected and it is inefficient.
3. **WebSocket**: bi-directional and persisent, initiated by the client. Starts as HTTP connection and "upgraded" via well-defined handshake. 
	\*It can even work when firewall is in place, using port 80 or 332 which are used by HTTP/HTTPS connections. 

It should be noted that Websocket is implemented by serialized dataframes, with `opcode`, `payload length` and `payload data` defined. Also, client-server data must be masked while server-client data must **NOT** be masked. If not satisfying, send close frame to close connection.
For the payload length, if equals 126 then the actual length is the 2 byte (16bits) int; otherwise if it s 127 then it is 8 bytes (64bits) 


---

Then we can move to the design stage, and have 
Note that sign up / loging / user profile, etc can just use traditional request / response. We can further break down the chat system into three major cateogories: stateless service, stateful service, third-party integration. 

{% asset_img chat_app.png chat_design %}

1. **Stateless Service**: Manage the login / signup / user profile, etc. Sits behind *load balancer*, can be monolithic or individual microservices.
	**Service discovery**: give the client a list of DNS host names of chat servers which client could connect to
2. **Stateful Service**: Chat service, which require a persistent network connection to the chat server. Since the connection usually do not switch, we need service discovery to avoid server overloading.
3. **Third party integration**: *Push notification* is the most important third-party integration.
4. **Scalability**: The number of concurrent connections that a server can handle will most likely be the limiting factor. For 1M concurrent users, each needs 10K memory on server (depending on language choice), only needs 10GB of memory. 
	However, such design is usually deal breaker mainly due to **single point of failure** concern.

Client should maintain a persistent *WebSocket* connection to chat server for real-time messaging. 
Chat servers facilitate message sending / receiving, presence servers manage online / offline status. API services handle login / signup / profile and notification sends push. **KV storage** is used to store chat history, so when offline user comes online she can check history.

**Storage**:
1. **Data types**: **generic data** (user profile / setting / friend list..) and **chat history** (big amount, only recent chats are accessed frequently; need random access of data for search, mentions or jump to specific messages).
2. Use data type and read - write patterns to support the data access layer. Read - write ratio should be ~1:1 for 1-1 chat apps.
3. We recommend **KV store** because:
	Enables easy horizontal scaling; low latency; handle long tail data well and random access; adopted by existing chat applications, like `HBase` and `Cassandra`

---

### Data Models
1. For 1-1 message, should contain `message_id` (bigint), `message_from`, `message_to`, `content` (text) and `created_at` (timestamp)
2. For group chat, we should instead have `channel_id` aside from the message id.
3. `message_id` should be **unique** and **increase** by time.
4. For simplicity, we can run a local sequence generator, becuase we only need *local* IDs when maintaining 1-1 channel or group channel.

## Design Deep Dive
### Service Discovery
Recommend the best chat server for a client, based on geographical location, server capacity, etc.

**Apache Zookeeper** is popular open-source solution for service discovery. It registers and picks best chat server for predefined critieria. 
First time login will go thorugh load balancer and API servers, then Zookeeper will pick the best server which will build **WebSocket** connection with the client.

### Message Flows

For **1-1** Chat case:
	User A sends a message, and the server will obtain a message ID from generator, then sends to message sync queue (across chat servers). Message will also be stored in key-value store. If user B is online, message will be forwared to server where B locates; otherwise a push notification is sent to **Push Notification** (PN) server.

Multiple Device Message **Synchronization**:
	Each device will build a WebSocket connection with the same chat server. Each device maintains a variable named `cur_max_message_id` and use that to track the latest messageID on the device. When message arrives and recipient ID is equal to currently logged-in user and the message ID is greater than ``cur_max_message_id`, forwarding will happen.

**Group Chat**:
	Message from sender will be copied to each group member's message sync queues. 
	\* This design only works for small group chat (to store a copy in each recipient's inbox). **Wechat** therefore limits group to be 500 members.

	On recipient side, a recipient can receive messages from multiple useres, and has an inbox storing messages from different senders.

**Online Presence Indicator**:
	Show a green dot next to a user's profile picture or username. After a WebSocket connection is built, user's online status and `last_active_at` timestamp can be stored into KV store. Presence Indicator shows the user is online. 
	When user logs out, the API servers will notify the presence servers and change to offline in KV store.

**User disconnection**:
	When user disconnects, it may not be a good idea to immediately marks him as offline (e.g., when going through a tunnel). Therefore, we should avoid changing presence indicator too often. 
	We can introduce a **heartbeat** mechanism to solve this. Online client can send a heartbeat periodically to presence servers, and use that to determine online status.
	**Online status fanout**: With a **publish-subscribe** model, each friend maintains a channel. When a friend's status changes, events will be published to channels which are subscribed by friends. 
	For very big group, we can fetch online status only when a user enters a group or manually refreshes the friend list.

### Extensive Discussion TOpics
1. Support for media files. Can discuss compression / cloud storage / thumbnails for large files.
2. End-end encryption.
3. Caching messages on the client-side is effective to reduce the data transfer.
4. Improve load time. Slack built a geographically distributed network to cache user's data, channels for better loading time.
5. Error handling: including chat server error and message resent mechanism (retrying & queueing)

