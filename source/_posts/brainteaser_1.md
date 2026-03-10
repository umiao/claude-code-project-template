---
title: Collection and Solution of Brainteasers - 1
date: 2022-07-29 00:35:43
categories:
- [Job Search, Financial Firm]
tags:
- IQ
- Brainteasers
- Math
description: "Strange questions you would expected to meet only in interviews of financial / trading firms LOL!"
---
Strange questions you would expected to meet only in interviews of financial / trading firms LOL!

{% asset_img cover.png SQL Note of blur! %}
<!-- more -->

## 1 - Screwy pirates
***Question***: Five pirates looted a chest full of 100 gold coins. Being a bunch of democratic pirates, they agree on the following method to divide the loot:
The most senior pirate will propose a distribution of the coins. All pirates, including the
most senior pirate, will then vote. If at least 50% of the pirates (3 pirates in this case)
accept the proposal, the gold is divided as proposed. If not, the most senior pirate will be
fed to shark and the process starts over with the next most senior pirate ... The process is
repeated until a plan is approved. You can assume that all pirates are **perfectly rational**:
they want to stay alive first and to get as much gold as possible second. Finally, being
blood-thirsty pirates, they want to have **fewer pirates on the boat (kill as many as possible)** if given a choice between otherwise equal outcomes.
How will the gold coins be divided in the end?

***Solution***: Infer from the most trivial case. 
1. **One pirate**: get all $100$ gold. (1 v 0)
2. **Two pirate**: The 2nd pirate would deny the 1st's plan anyway to get all $100$ golds. Thus, 1st pirate's expectation is $0$. (1 v 1)
3. **Three pirate**: Now, the pirate who's the first to move only need to give $1$ gold to the one who is second to move. (2 v 1)
4. **Four pirate**: In the three pirate case, the last pirate's equity is **denied**, so the first to move give him $1$ gold. (2 v 2)

Thus, for any $2n+1$ pirate case ($n < 99$), the first-to-move pirate ($2n+1$) offer the pirate $1$, $3$, ..., $2n-1$ one coin and keep the rest.


## 2 - Tiger and sheep
***Question***: One hundred tigers and one sheep are put on a magic island that only has grass. Tigers can eat grass, but they would rather eat sheep. Assume: **A.** Each time only one tiger can eat one sheep, and that tiger itself will become a sheep after it eats the sheep. **B.** All
tigers are smart and **perfectly rational** and they want to survive. So will the sheep be
eaten?

***Solution***: Trace back from the trivial case, like $1$ tiger ($n=1$) and $1$ sheep. The the tiger would eat the sheep. When $n=2$, no tiger would eat the sheep, otherwise, the case would be transformed to $n=1$ and the tiger who eat the sheep would be eaten. Similarly, we can have that when $n=3$, or $n=2k-1, \forall k \ge 1$, a tiger can eat the sheep.




## 3 - River crossing
***Question***: Four people, A, B, C and D need to get across a river. The only way to cross the river is by an old bridge, which holds at most 2 people at a time. Being dark, they can't cross the bridge without a torch, of which they only have one. So each pair can only walk at the speed of the slower person. They need to get all of them across to the other side as
quickly as possible. A is the slowest and takes $10$ minutes to cross; B takes $5$ minutes; C
takes $2$ minutes; and D takes $1$ minute.
What is the minimum time to get all of them across to the other side?
***Solution***:
The key is to **hide the latency** lol. That is to say, A and B should cross in the same round and never get back. Thus, the plan would be like: ($\rightarrow$, CD), ($\leftarrow$, D), ($\rightarrow$, AB), ($\leftarrow$, C), ($\rightarrow$, CD). The total time consumption would be $17$ mins.

## 4 - Birthday problem
***Question***: You and your colleagues know that your boss A's birthday is one of the following $10$ dates:
**Mar 4, Mar 5, Mar 8
Jun 4, Jun 7
Sep 1, Sep 5
Dec 1, Dec 2, Dec 8**
A told you only the month of his birthday, and told your colleague Conly the day. After
that, you first said: "I don't know A's birthday; C doesn't know it either." After hearing what you said, C replied: "I didn't know A's birthday, but now I know it." You smiled and said: "Now I know it, too." After looking at the 10 dates and hearing your comments,
your administrative assistant wrote down A's birthday without asking any questions. So what did the assistant write?

***Solution***: The key is like looking for a **unique identifier**. Since the days $2$ and $7$ are unique, then $C$ would be able to know the whole date if the day is $2$ or $7$. However, I believe $C$ does not have a chance to know it, thus, the month cannot be Jun or Dec. Then, $C$ learns the month is within Mar and Sep and know the whole date. Then, we can know that $C$'s day is within $\\{1, 4, 8\\}$ because if the day is $5$, $C$ still cannot tell. However, if the day is $4$ or $8$, I cannot figure out the date. Then, the month must be a **unique identifier** and can only be 1st Sep.




## 5 - Card game
***Question***: A casino offers a card game using a normal deck of $52$ cards. The rule is that you turn over two cards each time. For each pair, if both are black, they go to the dealer's pile; if both are red, they go to your pile; if one black and one red, they are discarded. The process is repeated until you two go through all $52$ cards. If you have more cards in your pile, you win $100$ $; otherwise (including ties) you get nothing. The casino allows you to negotiate the price you want to pay for the game. How much would you be willing to pay to play this game? 

***Solution***: $0$ because you will never win. Whenever you take away two red cards, there are two black cards for the dealer. In case of a tie (one black and one red), the difference of black and red cards number would not change (both in the deck and in your piles). Consider the idea of **symmetry**.
 

## 6 - Burning ropes
***Question***: You have two ropes, each of which takes $1$ hour to burn. But either rope has different densities at different points, so there's no guarantee of consistency in the time it takes different sections within the rope to bum. How do you use these two ropes to measure $45$ minutes? 

***Solution***: For a rope that takes $x$ minutes to burn, if you light both ends of the rope simultaneously, it takes $\frac{x}{2}$ minutes to burn. So we should light both ends of the first rope and light one end of the second rope. $30$ minutes later, the first rope will get completely burned, while that second rope now becomes a $30$-min rope. At that moment, we can light the second rope at the other end (with the first end still burning), and when it is burned out, the total time is exactly $45$ minutes.


## 7 - Defective ball
***Question***: You have $12$ identical balls. One of the balls is heavier **OR** lighter than the rest (you don't know which). Using just a balance that can only show you which side of the tray is heavier, how can you determine which ball is the defective one with $3$ measurements? 

***Solution***: Split the $12$ balls into groups of $4$, and measure the first $2$ groups. If it balances, the defective ball is in the rest group. If not, that ball is within the prior $2$ groups...
The detailed strategy is shown in the following image:

{% asset_img ball.png SQL Note of blur! %}

## 8 - Trailing zeros
***Question***: How many trailing zeros are there in $100!$ (factorial of $100$)? 

***Solution***: This is an easy problem. We know that each pair of $2$ and $5$ will give a trailing
zero. If we perform prime number decomposition on all the numbers in $100!$, it is obvious that the frequency of $2$ will far outnumber of the frequency of $5$. So the frequency of $5$ determines the number of trailing zeros. Among numbers $1, 2, ..., 99$, and
$100$, $20$ numbers are divisible by $5$ ( $5, 10, ..., 100$ ). Among these $20$ numbers, $4$ are
divisible by $5^2$ ( $25, 50, 75, 100$ ). So the total frequency of $5$ is $24$ and there are $24$
trailing zeros.

## 9 - Horse race
***Question***: There are $25$ horses, each of which runs at a constant speed that is different from the other horses'. Since the track only has $5$ lanes, each race can have at most $5$ horses. If you need to find the $3$ fastest horses, what is the minimum number of races needed to identify them? 

***Solution***: It is natural for us to index the horses from $1$ to $25$ and split them into $5$ groups of $5$ to take the first race. Then, with the first round $5$ races, you can eliminate the last $2$ of each group. We can assume $1, 6, 11, 16, 21$ are the fastest within each group (and already sorted by their speed, though we do not know the speed now).

We can find that for $16, 21$ cannot be in top $3$; $11$ may be within top $3$ but may not (because other members of top $3$ may be beat by $1$ and $6$). Then, we can race the $6$th time among $1, 6, 11, 16, 21$ to find out the local top $3$. Then, the pool of top $3$ can only be: $1, (2, 3), 6, (7), 11$ and $1$ is the absolute champion. Then we only need to give $7$th ride to $2, 3, 6, 7, 11$.

## 10 - Infinite sequence
***Question***: If x ^ x ^ x ... ^ x=2 and $x\^y=x^y$, find $x$.
***Solution***: Since we can have $x > 1$ and $\lim_{n \rightarrow \inf}$ x ^ x ^ x ... ^ x (a total of n) =2 converges to a constant $2$, then another ^ x would not change the result.  Then we can have x ^ (x ^ x ^ x ... ^ x) = $x^2 = 2$, $x=\sqrt 2$.






