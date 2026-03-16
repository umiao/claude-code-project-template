---
title: Object Oriented Design -- Principles and Practices
date: 2022-09-05 00:09:14
categories:
- [Job Search]
tags:
- OOD
- Object Oriented Design
- Software Engineering
description: "Important principles as well as solution to concrete interview questions."
key_concepts:
  - SOLID Principles
  - Object-Oriented Design
takeaways:
  - SOLID principles (SRP, OCP, LSP, ISP, DIP) provide guidelines for maintainable class design
  - Design patterns like Observer, Singleton, and State solve recurring structural problems
  - Start OOD interviews by identifying core objects, their relationships, and responsibilities
  - Favor composition over inheritance and program to interfaces for flexible, testable designs
---

Important principles as well as solution to concrete interview questions.

<!-- {% asset_img ood.jpg Object-Oriented Design cover: SOLID principles and design patterns %} -->
<!-- more -->

# SOLID Principles

**SOLID** stands for:
- **S (SRP)**: The **S**ingle **R**esponsibility **P**rinciple
There should **NEVER** be more than one reason for a class to change.
(A class should be changed and seperated, if it needs to undertake multiple type of responsibilities)
{% asset_img 1.jpg Single Responsibility Principle: a class should have only one reason to change %}
- **O (OCP)**: The **O**pen **C**losed **P**rinciple
The software should be expandable instead of immutable. That is to say, being **open** to **extension** and **close** to **mutation**.
{% asset_img 2.jpg Open Closed Principle: open for extension, closed for modification %}
- **L (LSP)**: The **L**iskov **S**ubstitution **P**rinciple
Only when an instance of a child class is able to **replace any instance** of its super class, we can say there is an is-A relationship between the two classes.
{% asset_img 3.jpg Liskov Substitution Principle: subclass instances replace superclass instances %}
- **I (ISP)**: The **I**nterface **S**egregation **P**rinciple
We should not force people to be dependent on the interfaces which they do not use.
Using multiple **specialized** interfaces is better than a single **universal** interface.
{% asset_img 5.jpg Interface Segregation Principle: prefer specialized interfaces over a universal one %}
- **D (DIP)**: The **D**ependency **I**nversion **P**rinciple
High level modules should not be dependent on low level modules. Both should be dependent on abstraction. Abstraction should not be dependent on details, details shoulde be dependent on abstraction.
{% asset_img 4.jpg Dependency Inversion Principle: high-level modules depend on abstractions %}

# Design Patterns
1. **Observer Design Pattern**: A subject corresponds to multiple observers, and notifies them of any state changes. Usually used for implementing event handling systems in "event driven" software. The observers are physically separated and have no control over the emitted events and their sources. Most implementations use background threads listening. 
	- The sole responsibility of a subject is to maintain a list of observers and to notify them of state changes by calling their **update()** operation. 
	- The responsibility of observers is to **register (and unregister)** themselves on a subject (to get notified of state changes) and to update their state (synchronize their state with the subject's state) when they are notified.

2. **Composite Design Pattern**: 
	- A **part-whole hierarchy** should be represented so that clients can treat part and whole objects **uniformly**. (Define a unified Component interface for different parts)
    - A **part-whole** hierarchy should be represented as **tree structure**. (Requests can be forwarded to their child components)
    - Try not to differentiate the leaf nodes and branch, have all the objects showing **similar behavior**.

3. **State Design Pattern**:  Allows an object to **alter** its behavior when its **internal state changes**. This can be a cleaner way for an object to change its behavior **at runtime** without resorting to conditional statements and thus improve maintainability. Aim to solve the tasks of:
	- An object should change its behavior when its internal state changes.
	-  State-specific behavior should be defined independently. That is, adding new states should not affect the behavior of existing states.
	- **Essence**: State should be defined as an object. A class delegate state-specific behavior to the state object, rather than implement it itself.

4. **Singleton Design Pattern**: Only allow one "single" instance of a class to be initialized. The only instance can be stored as class static variable and use **hidden & private** constructor.

# OOD Interview Topics
## Design an elevator
**Requirement**: an elevator would finally stopped at the required floor. It would head towards **the same direction**, until all the requests (to that direction) have been solved.

We can try to **abstract** the following objects / classes from the real-life elevator: 
- elevator (define its state, properties and restrictions, etc)
- panel (serve as container of buttons)
- button 
- request (signal triggered by button)
- controller (schedule & control the elevator).

Also, the **following facts** should be noted: 
1. Normally, the **status** of an elevator can only be: up, down and idle. There may be more states like under repair & inspection.
2. You should not abstract passengers into a class, because the elevator can be **agnostic of** certain passenger / items. It only check the total weight of them to decide if they can fit into one single ride.

## Design a parking lot
We can try to **abstract** the following objects / classes from the real-life parking lot: 
- Parking spot
- Entrance
- Cashier / Management System
- Timing System
- Ticket Printer


## Design a playlist
This is mainly about system design I believe. Comprehensively consider the data structure and pipeline to be applied to optimize the performance.

Work on the requirement to decide which part would need random access ability and find suitable data structure.



