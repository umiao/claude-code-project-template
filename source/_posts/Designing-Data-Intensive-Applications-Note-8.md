---
title: Designing Data-Intensive-Applications-Note-8
date: 2024-02-25 10:58:40
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on Encoding and Schema."
---
Discussion on Encoding and Schema.
{% asset_img cover.png DDIA Chapter 8 cover: Encoding, Schema Evolution and Compatibility %}
<!-- more -->

### Encoding and Evaluation:
- System require **evolvability**, e.g., capture new field or record types.
- In relational database, we usually assume that all data in database follow only **one** valid pattern. However, in **schema-on-read** / **schemaless** databases, it is possible that you can read a mixture of old / newer data formats written at different times.
- In larger application, you may need **rolling upgrade** / **staged rollout**. It deploys the new version into a few nodes at a time, checking whether the new version is running smoothly, gradually working your way through all nodes. This can enable update without **service downtime**, encourage more frequent releases.
- User may **not** update client-side applications in time. 
Thus we need： **backward compatibility** (newer code can read data that was written by older code) and **forward compatibility** (old code can read data written by new code). 
The prior is easier but the latter is harder and needs old ver of code to **ignore** additions made by the new codes.

Programs usually work with data in at least two ways: 
- **In-memory** (**objects**, **structs**, **lists**, **arrays**, **hash tables**, **trees**, can be effciently accessed and manipulated by CPU via pointers)
- **Over network** (**byte sequence** like JSON). By converting between them, we are doing encoding (**serialization**, **marshalling**) and decoding (**deserialization**, **unmarshalling**).
- **Examples**: For encoding in-memory objects, **Java**: `java.io.Serializable` (bad performance, bloated encoding); **Ruby**: `Marshal`; **Python**: `pickle`.           
#### Limitations 
- Reading is restricted to **the same** language
- Hard to switch programming language in the **receive end**
- Prevents **integration** of system. 
- Decoding process needs to be able to instantiate **arbitrary** classes, usually a source of security problems.  
- Thus, use the language built in encoding is a bad idea.

---

### JSON, XML and binary variants:
JSON and XML are well-known standardized encodings. However, XML is often criticized as too **verbose** and complicated, JSON is benefited from its **built-in support** in browsers and **simplicity**. 

- In **XML** / **CSV**, you cannot differ number from strings; 
- In **JSON**, you can not differ int from float and no precision specified (for number larger than $2^{53}$, it may be an issue).
- Also, they do not support **binary strings**. You can use **base64** to get around but the data size increased by 33%.

JSON is still less effective than binary encoding. **MessagePack**, is a binary encoding for JSON which sacrifice human readability to make the encoding result size smaller (for 18.5% less size in the given example, as a tradeoff).
Meanwhile, csv does not have schema at all, and you may need to deal with complex **escaping** rules.

--- 

### Thrift and Protocal Buffers:
- **Apache Thrift** and **Protocol Buffers** (**protobuf**) are binary encoding libraries that are based on the same principle, and a schema is required to define the type, field name and whether is optional.

{% asset_img 1.png Apache Thrift and Protocol Buffers schema definition example %}

- Thrift has 2 binary encoding formats: **BinaryProtocol** and **CompactProtocol**.
{% asset_img 2.png Thrift BinaryProtocol binary encoding layout %}
{% asset_img 3.png Thrift CompactProtocol binary encoding layout %}

- Note that if a field is specified as required, this is only checked in **run-time**.
- **Variable-length integers**: rather than using a full eight bytes to store integer, we can instead encode in 2 bytes (units) and use the **top bit** of each byte to indicate if there are more bytes to come.
Thrift has a dedicated **list** data type.

---

### Protocol Buffer: 

- Is very similar to the Thrift CompactProtocol. 
- However, it does not have a list / array type, just a **repeated** marker for fields. 

**Nice effect**: 
- Can change option into repeated; 
- New code reading old data sees a list with zero or one elements (depending on whether the field was **present**)
- Old code reading new data sees only the **last** element of the list.

**Compatibility**: 
- You can add new fields to the structure, however, just cannot specify it as a **required** field or the runtime check will fail. 
- Old codes can simply **ignore** unrecognized fields and new codes can adapt old schema.   
- Thus, added fields should be **optional** with **default values**.
- In terms of delete, you can only delete **optional** fields and can **never** use the same tag number again.
- Changing data type is possible, but may come with risk of losing precision / get **truncated**. 

--- 

### Avro:
- Based on **Protocol Buffer** and **thrift**.
- 2 schema languages: (**Avro IDL**) intended for human editing, the other based on JSON and easier to be read by machine.

{% asset_img 4.png Avro schema definition and binary encoding example %}

- No tag number / field to identify type. 
- Integers based on **variable length encoding**. This means that the binary data can only be decoded correctly if the code reading the data is using exactly the same schema as the code write the data. 
- Any mismatch in the schema between the reader and the writer would result in incorrectly decoded data.

**Writer’s schema**: the version of schema an application knows about when it writes (encodes) the data   
**Reader’s schema**: when read / decode, the schema it expect to see.   It can cause problem when there is **mismatch** between reader and writer schema.

**Schema evolution**: 
- **Forward compatibility**: have a new version of schema as writer; 
- **Backward compatibility**: have a old version of schema as reader.
You can only add or delete a field that has a default value.
\*In avro, if you want to allow a field to be null, you have to use a **union type** like: {null, long, string} 

- **Enforcing the writer schema**: the schema can be reused (like declaring in the start of file), e.g., usage in hadoop, storing files with millions of records. 
You can specify a file format (**object container** files) to do this.
We may have multiple authors across different times, so specify the **version** at the beginning of each encoded record and use author’s schema.
- For network connection case, processes can negotiate the schema version for the **lifetime of the connection**.
- Version number can be an **incrementing integer** or a **hash** of the schema.
	
This is in fact, a pattern of **dynamically** generated schema. 
It can be flexibly configured during every run. 
Label / type can be changed though **name** stay unchanged as the identifier.
For statically typed languages like **Java**, **C++** or **C#**, **Thrift** and **Protocol Buffers** are more friendly, allowing **type checking** and **auto-completion**. 
For dynamically typed programming languages like **Javascript**, **Ruby** or **Python**, there is not much point in generating code, and can become an obstacle to getting data.

\*Avro can support both.


