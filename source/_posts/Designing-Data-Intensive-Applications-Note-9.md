---
title: Designing Data-Intensive-Applications-Note-9
date: 2024-02-25 12:49:40
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on Data Flow and Message Passing."
key_concepts:
  - Message Queues
  - Encoding and Schema Evolution
  - Fault Tolerance
takeaways:
  - Prefer REST over RPC for public APIs due to simpler debugging and broader tooling support
  - Use asynchronous message passing for decoupling producers and consumers
  - Design RPC interfaces with idempotent operations to handle network retries safely
  - Apply the actor model for concurrent distributed systems to avoid shared-state complexity
series: DDIA
series_index: 9
---
Discussion on Data Flow and Message Passing.
{% asset_img cover.png DDIA Chapter 9 cover: Data Flow and Message Passing %}
<!-- more -->

### Data Flow in Databases:
- Data usually has longer life cycle, comparing with codes. 
- You need to be aware that if a new version of application wrote the data, it then got read & rewrite by an old ver application, we may face loss of fields / **inconsistency**. 
- The solution can be easy (like keeping the unknown fields, even when you want to transform it into an object then convert back), you just need to be aware of this.
\* For archival storage (like creating database’s **snapshot**), it is better to keep them all stored in **latest** version, rather than following the original mixture of formats.


### Data Flow Through Services: REST and RPC:
- When arranging communication, you usually need to assign roles like **clients** (access API though network) and **servers** (expose API over network).
- Clients use **get** to dowload **HTML**, **CSS**, **JavaScript**, images, etc. 
- Use **POST** requests to submit data to the server. API consissts of a standardized set of protocols and data formats (**HTTP**, **URLs**, **SSL/TLS**, **HTML**, etc.)
- A client-side JavaScript application running inside a web browser can use **XMLHttpRequest** to become an HTTP client (this technique is known as **Ajax**), usually transferring JSON.

### Service Oriented Architecture (SOA) / microservices architecture
- Decompose large application into smaller services by area of **functionality**
- One server itself can be the client of other servers by requesting certain sub-services.  
- This helps application easier to change and maintain by making services **independently** deployable and evolvable. This also means that older version and later version servers and clients must be **compatible** across versions of the service API.
- Service can impose **fine-grained** restrictions on what user can do, but limiting the **input** and **output**.

---

### Web Services:
- Definition: when HTTP is used as the underlying protocol for talking to the service. 
The context of “web” can be: 
1. Personal device usage through public internet.
2. Same organization’s services talk to each other within the data center as part of a service-oriented structure (software supporting this kind of use case is named as **middleware**). 
3. Requests between organizations, usually via internet.

#### REST 
1. Design philosophy that builds upon the principles of **HTTP**
2. Emphasizes **simple** data formats
3. Using **URLs** for identifying resources and using HTTP features for **cache control**, **authentication**, and **content type negotiation**. 
[More famous than SOAP]

\*API designed according to REST principles is called **RESTful**. It prefers less code generation and automated tooling. 

A definition format such as OpenAPI, a.k.a **Swagger**, can be used to describe RESTful APIs and produce documentation.

### SOAP: 

- XML based protocol for making netwrok API requests. 
- Aims to be independent from HTTP and **avoids** using most HTTP features
- Instead with sprawling and complex multitude of related standards (the **web service framework**, known as **WS-\***)

The XML based languaged SOAP API use is called **Web Services Description Language** (WSDL). It is **NOT** human readable and hard to construct mannually, heavily rely on tool support, code generation and IDEs. 
Client access a remote service using **local classes** and **method calls** (encoded to XML messages and decode by the framework). 
[Good for statically typed language]
Also, the implementation can be different across vendors.

--- 

### Remote Procedure Calls:
- The **Remote Procedure Calls** (RPC) model tries to make a request to a remote network service look the same as calling a function or method in your programming language, within the same process 
(this abstraction is called **location transparency**).
#### Problems
- Local func call is **predictable** and either succeeds or fails depend on the paran; 
- A network request is **unpredictable** due to network problem (for both request and response). 
- Network can have completely no result due to a **time-out** (you have no clue what happened). 
- If you retry, then the requests may be executed for multiple times, just the response got lost. 
- This will interfere with the behavior, unless you build mechanism for deduplication (**idempotence**).
- The time for func call is also **unstable**.
- Larger objects are hard to be encoded and send via network. 
We may also encounter type issues when the client and server are not implemented using the same language. Like Java has problem dealing number $> 2^{53}$.


**Enterprise JavaBeans** (EJB) and Java’s **Remote Method Invocation** (RMI) are limited to **Java**. 
The **Distributed Component Object Model** (DCOM) is limited to **Microsoft** platforms. 
The **Common Object Request Broker Architecture** (CORBA) is excessively complex, and does not provide backward or forward compatibility

Due to the shorcomings mentioned above, RPC is mainly used in request between services owned by the same organizaiton, typically in the same **data center**.

- **Rest**: will not try to hide the fact this is a network protocol, but you can still build RPC libraries on top of that. 

**RESTful** APIs are：
1. good for experimentation and debugging (easily make request using browser / tool curl)
2. Supported by **all** mainstream programming languages and platforms
3. Has a vast **ecosystem** of tools (servers, caches, load balancers, proxies, firewalls, monitoring, debugging tools, testing tools, etc.).

#### Evolvability: 
- For RPC, we can do the simplifying assumption that **all** servers will be first updated, then come the clients. 
Then, we only have **backward compatibility** on **requests**, and **forward compatibility** on **responses**.
If RPC is used for service providing, upgrading can be **hard** on clients. 
Then compatibility may need to be maintained to long time, maybe forever. 
- Service providers often end up maintaining **multiple versions** of the service API side by side.  
This can be done via specifying the version in **HTTP header** / **URL** / or use **API Keys**.

\* New generation of RPC frameworks is more explicit about the fact that remote request is different from a local function call. E.g., use **futures** (**promises**) to encapsulate **async** actions that may fail.
\*\*Some frameworks also provide **service discovery**, allowing a client to find out at which IP address and port number it can find a particular service.

--- 

### Asynchronous Message-passing Systems:
- It is between **RPC** and **databases**. 
A request (message) is delivered to another process with low latency, but got converyed by an intermediate called **message broker** (**message queue** / **message-oriented middleware**). 
- Usually no data model is enforced, the message is just a **sequence of bytes** with some metadata. 
- For consumer, if it wants to republish the message, it should keep all the **unknown fields**.
- Difference with RPC is that the message-passing is usually **one-way**. 
Sender does not expect replies, just send and move forward.
- **Open source implementations**: **RabbitMQ**, **ActiveMQ**, **HornetQ**, **NATS**, **Apache KAFKA**

#### Advantages: 
- Act as a **buffer** to improve system reliability; 
- Redeliver messages to a **crashed** process, avoid it from being lost; 
- Avoids the sender needing to know the **IP address** and **port number** of the recipent (useful in a cloud deployment where virtual
machines often come and go); 
- One message to be send to **serveral** recipents; 
- Logically **decoupes** the sender from the recipent (sender does not care who is the message consumer).

---

### Distributed actor frameworks:
- The actor model is a programming model for **concurrency** in a single process. 
- Rather than dealing directly with threads (and the associated problems of **race conditions**, **locking**, and **deadlock**), logic is encapsulated in **actors**. 
- Each can represent one **client** / **entity**, may have some not shared local states. 
Process one message at a time, can be scheduled **independently** by framework. 
- Communicating with each other by sending – receiving **asynchronous** messages. Delivery is not guranteed.


In distributed actor framework, this programming model is used to scale an application across multiple **nodes**. Same message-passing mechanism is used regardless of sender & recipents in the same node or not. 
If not, message will be encoded into byte sequence, send over network and decode on the other side.

It essentially **integrate** message broker and the actor programming model into single framework. 
But still need to take care of **forward** & **backward** compatibility.

- **Location Transparency**: ability to access objects without the knowledge of their location. In actor model, location transparency works better than model in RPC. 
The message is already assumed to be possibly **lost**, and we have less of a fundamental mismatch between local and remote communication.

#### Examples: 
1. **Akka** uses Java’s built-in serialization by default, which does not provide forward
or backward compatibility. However, you can replace it with something like **Protocol Buffers**, and thus gain the ability to do rolling upgrades.
2. **Orleans** by default uses a custom data encoding format that does not support **rolling upgrade** deployments; 
To deploy a new version of your application, you need to set up a new cluster, move traffic from the old cluster to the new one, and shut down the old one. 
Like with Akka, custom **serialization** plug-ins can be used.
3. In **Erlang** OTP it is surprisingly hard to make changes to record schemas (despite the system having many features designed for high availability); 
Rolling upgrades are possible but need to be planned carefully. 
An experimental new maps datatype (a JSON-like structure, introduced in Erlang R17 in 2014) may make this easier in the future.


