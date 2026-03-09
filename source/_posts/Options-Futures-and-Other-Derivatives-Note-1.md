---
title: Options Futures and Other Derivatives - Note - 1
date: 2023-09-09 12:42:55
categories:
- [Investment]
tags:
- options
- futures
- trading
- investment
---
Learning note of "Options Futures and Other Derivatives", 11th Edition.
{% asset_img cover.jpg apple %}
<!-- more -->

# Introduction

- **Derivatives exchange** is a market where individuals trade standardized contracts that have been defined by the exchange.
- **Chicago Mercantile Exchange** (CME)
- *Open outcry system* is being replaced by *electronic trading* -> growth in **algorithmic trading**.

## Over-the-counter Market
- Alternative to exchanges; larger than the exchange-traded market (in total volume of trading)
- Usually between financial institutions;  prepared to quote both a **bid** price (a price at which they are prepared to buy) and an **offer** price (a price at which they are prepared to sell).
-  The terms of a contract do not have to be those specified by an exchange.
- Market size rises to \$600+ trillion in 2022.

## Forward Contracts
- Agreement to buy or sell an asset at a certain future time for a certain price.
- A **spot contract** is an agreement to buy or sell an asset today.
- One of the parties to a forward contract assumes a **long position** and agrees to buy the underlying asset on a certain specified future date for a certain specified price. The other party assumes a **short position** and agrees to sell the asset on the same date for the same price.

### Payoffs from Foward Contracts
Assuming we have forward quotes for the USD/GBP exchange rate, for 6-month forward, the bid price: 1.4416 and offer price: 1.4422, then we can buy 1M GBP for 1.4422M USD.
If the spot exchange rate rose to 1.5000, at the end of the 6 months, the forward contract would be worth \$57,800 (= 1,500,000 - 1,442,200). 

Similarly, if the spot exchange rate fell to 1.3500 at the end of the 6 months, the forward contract would have a negative value to the corporation of \$ 92,200.

We assume the Delivery price=$k$, and price of asset at contract maturity = $S_T$. 
The **payoff** from a **long position** in a forward contract on one unit of an asset is $S_T - K$, and for a **short position**, the payoff is $K - S_T$.

### Forward Prices and Spot Prices
Forward Prices and Spot Prices are tightly related. If a a stock that pays no dividend and is worth 60, and you can borrow or lend money for 1 year at 5%, then the 1-year forward price should be 63. If not, then you can hold long / short forward contracts for profit.

## Future Contracts
Like a forward contract, a futures contract is an agreement between two parties to buy or sell an asset at a certain time in the future for a certain price. 
Unlike forward contracts, futures contracts are normally traded on an exchange. 

## Options
- Options are traded both on exchanges and in the over-the-counter market. 
- A **call option** gives the holder the right to buy the underlying asset by a certain date for a certain price. 
- A **put option** gives the holder the right to sell the underlying asset by a certain date for a certain price. 
- The price in the contract is known as the **exercise price** or **strike price**; 
- The date in the contract is known as the **expiration date** or **maturity**. 
- **American options** (most of the options) can be exercised at any time up to the expiration date.
- European options can be exercised only on the expiration date itself.
- One contract is usually an agreement to buy or sell 100 shares.

It should be emphasized that an option gives the holder the right to do something.
The holder DOES NOT have to exercise this right. This is what distinguishes options from forwards and futures, where the holder is **obligated** to buy or sell the underlying asset.


The price of a call option *decreases* as the strike price *increases* (**negatively correlated**), while the price of a put option *increases* as the strike price *increases* (**positively correlated**). 
Both types of option tend to become more valuable as their time to maturity increases (increased uncertainty, **converged** to the delivery price).

### Example
Suppose an investor instructs a broker to buy one December **call option** contract on Google with a strike price of **\$520**. The broker will relay these instructions to a trader at the CBOE and the deal will be done. 

The (offer) price is \$32.00, this is the price for an option to buy one share. 
In the United States, an option contract is a contract to buy or sell 100 shares. 

Therefore, the investor must arrange for \$3,200 to be remitted to the exchange through the broker. The exchange will then arrange for this amount to be passed on to the party on the other side of the transaction.

The investor got the right to by 100 Google shares for \$ 520 each at the cost of 3200 USD (cost on options).
- If Google reached 600 USD and the option is exercised, the profit would be $(600-520)*100-3200=4800$.
- If Google stayed off 520 USD, the maximal loss is made (the premium) since the holder of the option won't exercise it.
- If a call / put option is sold, the sellar would immidiately receive the premium.

For now, we discussed 4 types of participants in options markets:
1. Buyer of calls
2. Seller of calls
3. Buyer of puts
4. Seller of puts

Buyers hold *long position*, and sellers hold *short position*. Selling an option also known as *writing the option*.






















