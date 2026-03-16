---
title: Designing Data-Intensive-Applications-Note-3
date: 2024-02-23 16:28:51
categories:
- [Data Science, Data System]
tags:
- Data Science
- Data System
- Designing Data-Intensive-Applications
description: "Discussion on maintainability, evolvability and operability."
key_concepts:
  - Scalability
  - Fault Tolerance
takeaways:
  - Reduce complexity through good abstractions rather than patching symptoms
  - Design for evolvability by anticipating requirement changes from the start
  - Invest in operability through monitoring, automation, and self-healing mechanisms
  - Repay technical debt systematically to maintain long-term system health
series: DDIA
series_index: 3
---
Discussion on maintainability, evolvability and operability.
<!-- {% asset_img cover.png DDIA Chapter 3 cover: Maintainability, Evolvability and Operability %} -->
<!-- more -->

# Maintainability
1. Fixing **bugs**
2. Keeping its systems **operational**
3. **Investigating** failures
4. **Adapting** it to new platforms
5. Modifying it for new **use cases**
6. Repaying **technical debt**
7. Adding **new features**


Try to focus on the following 3 design principles:

---

### Operability
Make it easy for operations teams to keep the system running smoothly. 

**Duties** of operations teams include: 
- **Monitor** health
- **Track** issue & cause
- **Update** software and platform
- Track how systems **interfere** each other
- Manage **deployment** and **configuration**
- Anticipate and resolve **future problems**
- Perform **complex maintenance**
- System **security**
- **Define** process
- Preserve **org-level knowledge** about sys


Examples of **improving maintainability**:
- Provide visibility into runtime behavior and internal of system
- **Automation** and **integration**
- Avoid dependency on **individual** machines
- Docs and operational models
- Good **default** behavior
- **Self-healing** of sys
- Exhibit **predictable** behavior.

---

### Simplicity
Make it easy for new engineers to understand the system, by removing as much
complexity as possible from the system. 

Examples of **complexity**:
- Explosion of the **state space**, 
- **Tight coupling** of modules, 
- **Tangled** dependencies, 
- Inconsistent **naming and terminology**,
- **Hacks** aimed at solving performance problems, 
- **Special-casing** to work around issues

**Best Resolving practice**: 
1. Introduce **abstraction** to hide details. 
2. Extract data system into well-defined, reusable **components**.

>Note this is not the same as simplicity of the user interface.


---

### Evolvability
Make it easy for engineers to make changes to the system in the future, adapting it for **unanticipated** use cases as requirements change. 
Also known as **extensibility**, **modifiability**, or **plasticity**.

Examples of **Evolvability** needs:
-	You learn **new facts**, 
-	Previously **unanticipated** use cases emerge, 
-	**Business priorities** change, 
-	Users request **new features**, 
-	New **platforms** replace old platforms, 
-	**Legal** or regulatory requirements
-	Change, growth of the system forces **architectural changes**







