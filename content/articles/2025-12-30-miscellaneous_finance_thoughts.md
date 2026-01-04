---
Title: ETF Engineering Magic
Date: 2025-12-30 07:00:00 +0200
Tags: 
slug: miscellaneous_investing_thoughts
status: draft
---

### TWR and MWR

How do we measure the return of a portfolio if it has many assets inside and there are multiple deposits or withdrawals from it throughout the period of interest? It's not as simple as looking at the ending value and the beginning value. 

Returns are relative to a benchmark. If the first deposit happened 3 years ago, at $t_0$, we can compare against the return of a broad index like S&P 500, whose return is $\big(P(t) - P(t_0)\big)/P(t_0)$. $P(t)$ is the price of the index. Suppose the return is 60%, obtained during a strong long uptrend. Can we expect the same return from a sufficiently diversified dollar-cost-averaged (DCA) portfolio? Not really, no, because with DCA you're not investing everything all at the beginning. You're spreading all the buy-ins uniformly across time. Thus, with regular investments the DCA return should be around 30%. 

That's a scary big difference the investor will have to confront. It comes from incrementally investing in an uptrend. If you're sure that the price will go up, DCA will only reduce your profits. If you're less sure, then the return reduction from DCA is basically the cost of hedging against a drop in the asset value. In some cases, if it does drop, DCA will have saved you a lot of stress. 

With a benchmark set, how do we compute the return of the portfolio? If there are no withdrawals so far, the return could be calculated simply as
$$
1 + \text{R}(t) = \frac{V(t)}{\sum_{\tau} D[\tau]}.
$$

Here $R(t)$ is the return at time $t$, $V(\cdot)$ is the spot portfolio value, and $D[\tau]$ are the deposits, presumably at discrete times indexed by $\tau$. If we've invested 1000\$ in 3 deposits and the current value is 1200\$, that's a 20% return. But this is a bad metric because if I deposit more now, the denominator will grow and the return will decrease, without the new money having had the opportunity or the time to grow. Hence, this calculation should be avoided.

A better measure is called **time-weighted return** (TWR). It works as follows. We split the performance into intervals at the time of the deposits, $\tau_1, \tau_2, ..., \tau_N$. The first deposit occurs at $\tau_1$ and the first interval is $[\tau_1, \tau_2]$. The last interval is up to now, $[\tau_N, t]$. For the interval $[\tau_1, \tau_2]$ the starting value of the portfolio is $V(\tau_1^+)$ which indicates the value right after the deposit. Likewise, the ending value is $V(\tau_2^-)$, right before the next deposit. The total TWR return is calculated as:

$$
1 + \text{TWR}(t) = \prod_{i = 1}^N \left(1 + \frac{V(\tau_{i + 1}^-) - V(\tau_i^+)}{V(\tau_i^+)}\right).
$$

The value in the parenthesis is just the gross return from each period. Note how there are no deposits or withdrawals in the formula. In fact, it's only the performance (return) that matters here. Whether it's 1\$ or 1000\$ deposited at time $\tau_i$ doesn't matter. Because of this, the returns obtained stem primarily from the selection of the assets in the portfolio, and their proportions relative to each other. Thus, the TWR is particularly suited for comparing portfolios and funds.

A cash deposit in the portfolio that doesn't get immediately invested into risky assets will show up as a new $\tau_i$ but, but if it remains cash, or if it doesn't change the overall asset selection, it will not change the returns. In addition, each unit of time between cash flows is weighted equally, regardless of how much money is invested during that time. Because returns are compounded by time period (they're being multiplied together), not by invested amount, the result is effectively time-weighted. Altogether, TWR measures the performance of an investment independent of cash flows. It removes the impact of investor timing.

What *does* account for cash-flow timing is called **money-weighted return** (MWR). The MWR is the rate of return that solves

$$
\sum_{\tau=0}^t \frac{\text{CF}(\tau)}{(1 + \text{MWR})^\tau} = 0.
$$

Here $\text{CF}(\cdot)$ stands for any cashflow, could be deposit or withdrawal.  The cash flow at the current timestep is the value of the portfolio, $\text{CF}(t) = V(t)$, and should have the same sign as any withdrawal. For instance, if we have two deposits of 1000\$ at a year apart, and it's 6 months into the next year, and the portfolio is at 2500\$, that makes

$$
-1000 - \frac{1000}{1 + \text{MRW}} + \frac{2500}{(1 + \text{MWR})^{1.5}} = 0 \ \Rightarrow \ \text{MWR} \approx 24\%.
$$

The first investment of 1000\$ earns 38% in 1.5 years, while the second one earns 11.3% in 0.5 years. The interpretation is straightforward. The MWR is simply the internal rate of return of an asset with the same cashflows as those of the portfolio. It is money-weighted because it considers the amount deposited/withdrawn in each cashflow. Therefore, it can be used to gauge the performance of an individual investor's strategy, with timing and concrete amounts invested. It's also sensitive to deposit timings, as a larger deposit in an earlier favorable performance period will dominate the present value.

### Exchange Traded Funds

To understand ETFs, one needs to "derive" them from the ground up. It all starts with an index - a particular linear combination of risky assets, for example stocks. Prices are $P_i$ and weights $w_i$.

$$
I = \sum_{i} w_i P_i.
$$

Which companies are chosen, as well as how the weights are determined depends on the particular methodology of the index itself. The weights could be the proportion of the market cap in a total pool of companies, or any other calculation. In any case, after a company like MSCI designs the index, it can be turned into a product that investors buy and sell. Here's how it works.

The process is called *creation and redemption*. An ETF issuer, a firm like Blackrock or Vanguard, first selects the index to base the ETF off of. Then, they need to buy the right stocks in the right proportions. With ETFs obtaining the stocks is not done by bying them with cash. If they were bought with cash, whenever people want to leave, the ETF manager would have to sell stocks to get cash to pay them. That sale would trigger capital gains taxes. 

This is where ETFs differ from mutual funds. In a mutual fund, you don’t own the underlying stocks. You own shares of a company (the fund) that owns the stocks. Whenever the fund sells some stocks at a profit, this profit is divided proportionally *across all shareholdes* in the fund. Again, none of them owns the actual stocks that were sold, so none of them can attribute the whole profit. So what happens with mutual funds is, one shareholder wants out and triggers a sale, suppose at a profit. The capital gains for this sale are paid by all shareholders in the mutual fund, those that remain. They pay that tax but also get proportional gain, usually reinvested as more shares, from the sale. The leaving sharehold pays tax on the profit they made from selling their own shares.

ETFs avoid this whole tax situation. The ETF issuer enters into a legal agreement with what's called *Authorized Participants* (APs) - big banks and market makers like Goldman Sachs and JPMorgan. APs are the only entities allowed to create or destroy ETF shares. They bridge the stock market and the ETF issuer’s inventory. The ETF issuer prepares a Portfolio Composition File (PCF). It contains a list of how much shares (an integer number) need to be bought for each company in the index. Since it's mathematically impossible to buy stocks in a ratio that perfectly equals the index's share price down to the penny using only whole shares, the PCF includes a cash component. The PCF also includes the "lot size" (e.g. 50K ETF shares) and an initial share price (e.g. 50\$). Then, the "creation unit" is worth 2.5M\$. The cash component covers the difference between the stock basket value and this target value.

Once the APs receive the PCF, they use high-frequency algorithms to buy the shares with their own cash. Then, they perform an *in-kind transfer* with the ETF issuer. It moves the assets directly from the account of the AP to that of the ETF issuer without converting them to cash, avoiding immediate taxes and fees. The issuer in turn gives out a block of "newly minted" ETF shares. The AP then lists those ETF shares on major exchanges where investors can buy them.

On the exchange, the price of ETF shares are determined by supply and demand. Investors bid and ask different prices for shares while order books, along with trading engines, match buyers, list and execute orders. The market price of the ETF could, in principle, deviate from the ETF's *net asset value* (NAV), which is simply the spot price of the underlying stock basket. If the ETF is trading at a discount (spot price below NAV), the AP can intervene. It buys 50K ETF shares from the market and performs an in-kind transfer with the ETF issuer, obtaining the underlying stocks. Then, it sells them, at a profit in the market, thus bringing the ETF price to its NAV. This is called *redemption*.

On the ETF issuer side, once the AP hands over 50K ETF shares, the issuer has to hand over the underlying stocks, but there could be many stocks for each firm, bought at different times, e.g. AAPL stock bought years ago at 50\$ and some bought last year at 150\$. The issuer chooses to hand over those stocks on which it would owe the largest capital gains tax, those at 50\$. The AP sells them immediately. That's how the issuer avoids paying taxes. The investors pay capital gains taxes years later when they sell their ETF shares.

Based on all this, we understood that:

- ETFs are created using tax-advantageous in-kind transfers. These do not constitute a cash-based sale and no gain is realized, only a transfer of ownership. Taxation happens on gain realization, not ownership changes.
- ETF share prices are not allowed to deviate far from their stock basket's NAV. If they do, the APs arbitrage away the profit opportunities. Shares are created and destroyed based on demand, unlike for example stocks, where the number of shares are fixed and any hyped expectations can increase their price above their fundamentals.

<!-- To cover:
- replication types
- accummulation vs distribution
- NAV
- rebalancing
- intraday aspects -->

<!-- To say you know ETFs very well, you should understand them across structure, mechanics, costs, risks, and use cases. Mastery means you can evaluate any ETF and predict how it will behave in different market conditions.

Below is a complete ETF mastery checklist, grouped by domain. -->
<!-- 
1. Structural Foundations (What an ETF is)

You should clearly understand:
ETF vs mutual fund vs stock
Intraday trading, transparency, tax treatment
Open-ended structure
Shares are created/destroyed based on demand
Index-based design
Most ETFs track an index rather than pick stocks
Legal structure
Investment company (’40 Act in the U.S.) or trust structure
If you understand why an ETF’s price usually stays close to its NAV, you’re solid here. -->

<!-- 2. Creation & Redemption Mechanism (Core ETF “engine”)
This is essential knowledge.
Authorized Participants (APs)
Large institutions that create/redeem ETF shares
Creation units
Large blocks exchanged for baskets of securities
In-kind transfers
Why ETFs are tax-efficient
Arbitrage process
How price deviations from NAV are corrected
You should be able to explain step-by-step what happens when an ETF trades at a premium or discount.

3. Net Asset Value (NAV) & Pricing
Key concepts:
NAV calculation
Based on underlying holdings
Intraday market price vs NAV
Premiums and discounts
iNAV / IOPV
Real-time estimated NAV
You should know when NAV is less reliable (international markets, illiquid assets).

4. Index Construction & Tracking
Knowing the index is knowing the ETF.
Index methodology
Market-cap weighted, equal-weighted, factor-based
Rebalancing schedules
Inclusion/exclusion rules
Corporate actions handling
Tracking difference vs tracking error
You should be able to identify when an ETF’s underperformance is due to:
Fees
Index drag
Sampling
Market friction

5. Costs (Visible and Hidden)
Beyond the expense ratio:
Expense ratio
Bid–ask spread
Tracking difference
Turnover costs
Securities lending impact
Tax drag (dividends, capital gains)
Mastery means knowing why the cheapest ETF is not always the best ETF.

6. Liquidity (Often Misunderstood)
You should understand:
Primary vs secondary market liquidity
ETF liquidity ≠ volume traded
Underlying asset liquidity
Spread behavior in stressed markets
Market maker role
You should be able to explain why a low-volume ETF can still be highly liquid.

7. Taxation (Critical for Investors)

Depends on jurisdiction, but conceptually:
Why ETFs are tax-efficient
Capital gains distributions
Dividend taxation
Withholding taxes (international ETFs)
Tax treatment of bond ETFs
ETFs vs mutual funds in taxable accounts
If you can explain why ETFs usually distribute fewer capital gains than mutual funds, you know this well.

8. Replication Methods
Understand how the ETF holds exposure:
Full physical replication
Sampling
Synthetic replication (swaps)
Counterparty risk
Collateralization
You should know when synthetic ETFs may outperform physical ones—and why.

9. Risk Dimensions (Beyond “Market Risk”)
ETF-specific risks include:
Tracking risk
Liquidity risk
Closure risk
Counterparty risk
Concentration risk
Currency risk
Regulatory risk
You should know which ETF categories amplify these risks (e.g., leveraged, niche thematic, frontier markets).
10. Special ETF Types (Advanced Knowledge)
To claim deep understanding, you should know how these work mechanically:
Bond ETFs
Duration, yield curve exposure, NAV illusion
Commodity ETFs
Futures, contango, backwardation
Leveraged & inverse ETFs
Daily reset, volatility decay
Active ETFs
Transparency differences
Thematic ETFs
Index fragility and turnover
If you understand why a 2× ETF does not deliver 2× returns long-term, you’re advanced.

11. Trading & Execution Best Practices
Practical expertise includes:
Limit vs market orders
Trading at optimal times
Avoiding NAV blind spots
Handling spreads during volatility
Tax-loss harvesting with ETFs
You should know when not to trade an ETF.

12. Due Diligence Framework
You should be able to evaluate any ETF by answering:
What index does it track and how?
How tight is trackingg
What are total ownership costs?
How liquid is the underlying exposure?
What risks are unique to this structure?
Is this the best vehicle for the exposure?

Final Litmus Test
You “know ETFs very well” if you can:
Predict ETF behavior during market stress
Explain price/NAV deviations without guessing
Compare two similar ETFs and justify one choice clearly
Avoid common ETF traps that most retail investors fall into
If you want, I can turn this into:
A self-assessment quiz
A one-page ETF mastery checklist
A real ETF teardown (step-by-step analysis of a specific fund) -->