---
Title: ETFs Under the Hood
Date: 2025-12-30 07:00:00 +0200
Tags: 
slug: etfs_under_the_hood
status:
---

ETFs are often praised as the ultimate passive investment tool. But why? How do they work? How does a fund swap thousands of stocks without paying taxes? How does it track market indices? In this post, we’ll pry open the lid of this financial machine, exploring its engineering from first principles.

### The Rational Investor

Millions of traders have dedicated their lives to finding hidden statistical regularities that yield risk-free gains. Yet, market prices are dynamic feedback loops: they change based on actions, and actions are driven by future expectations. No one trades unless they believe it is worthwhile. Consequently, these collective expectations create the wild, often unpredictable, price dynamics we observe.

How is a rational investor supposed to act in such an environment? It is all about the mindset. When presented with two assets, you must first form realistic expectations about their future returns and volatilities. Consider Asset $x$ (e.g., a disruptive technology ETF), which offers high expected returns but high volatility, versus Asset $y$ (e.g., consumer staples), which offers lower risk and lower returns. If you have a long time horizon and the nerves to endure the swings, you rationally decide that Asset $x$ is better suited for your goals, and you invest there.

Suppose that at the end of this period, Asset $x$ actually underperforms the safer Asset $y$. This could be due to a recession or simply a bad sequence of returns right when you needed to cash out. Should you despair? The single most important answer is no. You should not base your self-assessment on *realizations*, which are random and uncontrollable. You made the right decision at the right time given the information available. Beyond that, you have no control, and you should not allow yourself to be swayed by emotions.

Rationality is about taking the action you believe to be optimal ex-ante, and then wiring your brain to be at peace with the result ex-post. You only care about what you control. If your investments underperform, it does not necessarily mean you are a bad investor; it often just means you are subject to variance. If your expectations are correct on average, and you invest according to them, then over the long run, you will outperform. However, since our investment horizons are finite, risk aversion remains a necessary survival mechanism.

Therefore, the practical action plan is as follows:

- **Research**:  Form realistic expectations about returns and volatility. Read financial statements, analyze ETFs, study economics, accounting, and human nature. This is the hardest thing in finance. Acknowledge *epistemic humility* and understand that you will default to the broad market expectations more often than not.
- **Allocation**: Construct a mix of assets - typically a broad market-wide ETF (core) supplemented by satellite ETFs or stocks representing your convictions.
- **Sizing**: Select position sizes that align with your risk profile.
- **Detachment**: Periodically rebalance according to your rational expectations, but stay emotionally detached from daily price action. The rational investor is a cold, calculating, impartial machine. Importantly, while staying detached from random realizations, ruthlessly critique whether your process for gathering future information, which is in your control, needs to improve.


### TWR and MWR

Now, how do we accurately measure the performance of a portfolio with multiple deposits and withdrawals? It is not as simple as comparing the ending value to the beginning value.

Returns are relative to a benchmark. Suppose we compare our portfolio against the S&P 500, which has returned 60% over the last three years, $\big(P(t) - P(t_0)\big)/P(t_0)$. If you utilized a Dollar-Cost Averaging (DCA) strategy during this strong uptrend, can you expect your personal return to match that 60%? Generally, no. With DCA, you don't invest everything at the start, at $t_0$. You spread your buy-ins across time, meaning much of your capital enters the market at higher prices later in the trend. Consequently, your personal return on capital might be closer to 30%. This gap is just the cost of hedging. DCA reduces the impact of a market drop, but in a pure uptrend, it dilutes the total percentage return compared to a lump-sum initial investment.

**A first metric**. In terms of metrics, consider an ultra-simple approach. If there are no withdrawals so far, a naive calculation is to simply divide current value by total deposits:

$$
1 + \text{R}_{\text{simple}}(t) = \frac{V(t)}{\sum_{\tau} D[\tau]}
$$


Here $R_\text{simple}(t)$ is the return at time $t$, $V(\cdot)$ is the spot portfolio value, and $D[\tau]$ are the deposits, at discrete times indexed by $\tau$. If you invested \$1000 in 3 deposits and the current value is \$1200, that's a 20% return. But this metric is flawed because if you deposit more now, the denominator grows instantly and the calculated return will decrease, without the new money having had the opportunity or the time to grow. Hence, this calculation should be avoided.


**TWR**. A better measure is called **time-weighted return** (TWR). It works as follows. We split the performance into intervals at the time of the deposits, $\tau_1, \tau_2, ..., \tau_N$. The first deposit occurs at $\tau_1$ and the first interval is $[\tau_1, \tau_2]$. The last interval is up to now, $[\tau_N, t]$. For the interval $[\tau_1, \tau_2]$ the starting value of the portfolio is $V(\tau_1^+)$ which indicates the value right after the deposit. Likewise, the ending value is $V(\tau_2^-)$, right before the next deposit. The total TWR return is calculated as:

$$
1 + \text{TWR}(t) = \prod_{i = 1}^N \left(1 + \frac{V(\tau_{i + 1}^-) - V(\tau_i^+)}{V(\tau_i^+)}\right).
$$

The value in the parenthesis is just the gross return from each sub-period. Note how there are no deposits or withdrawals in the formula. In fact, it's only the performance (return) that matters here. Whether it's \$1 or \$1000 deposited at time $\tau_i$ doesn't matter. Hence, the obtained returns stem only from the selection of the assets in the portfolio, and their proportions relative to each other. Thus, the TWR is best suited for comparing portfolios and funds.

A new cash deposit will show up as a new $\tau_i$.  Provided it is invested to maintain the same asset allocation, it will not skew the returns. Each unit of time between cash flows is weighted equally, regardless of how much money is invested during that time. Because returns are compounded by time period (they're multiplied together), not by invested amount, the result is effectively time-weighted. Altogether, TWR measures the performance of an investment independent of cash flows. It removes the impact of investor timing.

**MWR**. To measure the performance of the investor (accounting for timing), we use **Money-Weighted Return** (MWR). The MWR is the rate of return that solves

$$
\sum_{\tau=0}^t \frac{\text{CF}(\tau)}{(1 + \text{MWR})^\tau} = 0.
$$

Here $\text{CF}(\cdot)$ stands for any cashflow, could be deposit or withdrawal.  The cash flow at the current timestep is the value of the portfolio, $\text{CF}(t) = V(t)$, and should have the same sign as any withdrawal. For instance, if we have two deposits of \$1000 at a year apart, and it's 6 months into the next year, and the portfolio is at \$2500, that makes

$$
-1000 - \frac{1000}{1 + \text{MWR}} + \frac{2500}{(1 + \text{MWR})^{1.5}} = 0 \ \Rightarrow \ \text{MWR} \approx 24\%.
$$

The first investment of \$1000 earns 38% in 1.5 years, while the second one earns 11.3% in 0.5 years. The interpretation is straightforward. The MWR is simply the internal rate of return (IRR) of an asset with the same cashflows as those of the portfolio. It is money-weighted because it considers the amount deposited or withdrawn in each cashflow. Therefore, it can be used to gauge the performance of an individual investor's strategy, with timing and concrete amounts invested. It's also sensitive to deposit timings, as a larger deposit in an earlier favorable performance period will dominate the present value.


### Exchange Traded Funds

To understand ETFs, one needs to "derive" them from the ground up. It all starts with an index - a theoretical portfolio representing a specific market segment. Mathematically, it is a weighted sum of asset prices, with prices $P_i$ and weights $w_i$:

$$
I = \sum_{i} w_i P_i.
$$

Which companies are chosen, as well as how the weights are determined depends on the particular methodology of the index itself. The weights could be the proportion of the market cap in a total pool of companies, or any other calculation. In any case, after a company like MSCI designs the index, it can be turned into a product that investors buy and sell. Here's how it works.

The process is called *creation and redemption*. An ETF issuer, a firm like Blackrock or Vanguard, first selects the index to base the ETF off of. Then, they need to obtain the right stocks in the right proportions. With ETFs this is not done by buying them with cash, but instead through a barter system known as *in-kind* creation. If they were bought with cash, whenever people want to leave, the ETF manager would have to sell stocks to get cash to pay them. That sale would trigger capital gains taxes. 

This is where ETFs differ from mutual funds. In a mutual fund, you don’t own the underlying stocks. You own shares of a company (the fund) that owns the stocks. Whenever the fund sells some stocks at a profit, this profit is divided proportionally *across all shareholders* in the fund. Similarly, when one shareholder wants out, this could trigger a sale, suppose at a profit. The capital gains from this sale are also paid by all shareholders that remain in the mutual fund. They pay that tax but also get proportional gain, usually reinvested as more shares, from the sale. The leaving shareholder pays tax on the profit they made from selling their own shares.

ETFs avoid this whole tax situation. The ETF issuer enters into a legal agreement with what's called *Authorized Participants* (APs) - big banks and market makers like Goldman Sachs and JPMorgan. APs are the only entities allowed to create or destroy ETF shares. They bridge the stock market and the ETF issuer’s inventory. The ETF issuer prepares a Portfolio Composition File (PCF). It contains a list of how many shares (an integer number) need to be bought of each company in the index. Further, it includes the "lot size" (e.g. 50K ETF shares) and an initial share price (e.g. \$50). Then, the "creation unit" is worth \$2.5M. Because you cannot buy fractional shares on the open market, the basket of stocks will never perfectly match the target creation value ($2.5M). The PCF therefore also includes a small "balancing cash" component to cover the difference.

Once the APs receive the PCF, they use high-frequency algorithms to buy the shares with their own cash. Then, they perform an *in-kind transfer* with the ETF issuer. It moves the assets directly from the account of the AP to that of the ETF issuer without converting them to cash, avoiding immediate taxes and fees. The issuer in turn gives out a block of "newly minted" ETF shares. The AP then lists those ETF shares on major exchanges where investors can buy them.

On the exchange, the price of ETF shares is determined by supply and demand. Investors bid and ask different prices for shares while order books, along with trading engines, match buyers to sellers, and execute orders. The market price of the ETF could, in principle, deviate from the ETF's *net asset value* (NAV), which is simply the spot price of the underlying stock basket. If the ETF is trading at a discount (spot price below NAV), the AP can intervene. It buys 50K ETF shares from the market and performs an in-kind transfer with the ETF issuer, obtaining the underlying stocks. Then, it sells them, at a profit in the market, thus bringing the ETF price to its NAV. This is called *redemption*.

On the ETF issuer side, once the AP hands over 50K ETF shares, the issuer has to hand over the underlying stocks, but there could be many stocks for each firm, bought at different times, e.g. AAPL stock bought years ago at \$50 and some bought last year at \$150. The issuer purposefully selects the shares with the lowest cost basis (e.g., those bought at $50) to hand back to the AP. By disposing of these low-basis shares via an in-kind swap rather than a sale, the fund *washes* the potential tax liability off its books. The tax bill effectively vanishes. The investors pay capital gains taxes years later when they sell their ETF shares.

Based on all this, we understood that:

- ETFs are created using tax-advantageous in-kind transfers. These do not constitute a cash-based sale and no gain is realized, only a transfer of ownership. Taxation happens on gain realization, not ownership changes.
- Shares are created and destroyed based on demand, unlike regular company stock, whose share count changes only through corporate actions, not continuous arbitrage.
- ETF share prices are not allowed to deviate far from their stock basket's NAV. If they do, the APs arbitrage away the profit opportunities. In reality, transaction fees make some small arbitrage opportunities not worth it.

### Further Details

**Replication**. Mimicking the index by holding the underlying stocks in proportion as close as possible to that of the index is called *physical replication*. It is best for large, liquid indices like the S&P 500 or FTSE 100 where every stock is easy to buy and sell. However, in some cases, e.g. when there are too many stocks in the index, or some of them are illiquid and hard to trade, instead of full physical replication, a statistically representative sample is used.

**Sampling**. With *sampled physical replication*, the ETF issuer calculates a smaller sample of companies that when held, will produce the same returns as the index, up to very small tracking errors. This sample is calculated by optimization programs which take in the structural aspects of the index as constraints, e.g. 15% in small-cap, 25% in the US, etc., and output the optimized weights. Importantly, this kind of replication is only based on historical statistical patterns. There is no guarantee that the representative sample from the past will still behave as the index in the future. For such guarantees, one needs full physical replication.

**Synthetic replication**. Another option for index tracking is *synthetic replication*. It works as follows:

1. The ETF issuer creates the ETF shares and exchanges them with the AP for cash.
2. With the obtained cash, the ETF issuer buys liquid, boring, safe assets, like US Blue Chip stocks. These act as a collateral basket. The AP lists the ETF shares on exchanges.
3. The ETF issuer enters into a *swap* contract with a bank, could be that of the AP, agreeing to pay the return of the collateral basket, while the bank pays the return of the index.
4. The bank, acting as a shock absorber, often buys the underlying index stocks to hedge its own risk, so that if the index goes up and it has to pay more to the ETF issuer, also its own stocks from the index go up.

Overall, synthetic replication provides zero tracking error, because it uses derivatives to track the index return, but is less transparent and involves counterparty risk.

**Rebalancing**. The companies included in the index could change from day to day. In S&P500 those companies that become smaller exit the index, while others enter. The ETF issuer can accommodate this by simply switching the companies in the PCF. However, it still has to do something about the shares of the removed company that it already owns. If it sells them in the market, it will trigger capital gains tax. Instead, something called *heartbeat* trades are performed.

To dump the unneeded stock, the ETF issuer creates a new lot of ETF shares and exchanges them with the AP for cash. This creates an upward spike in the shares outstanding. Then, a day or two later, the AP *purposefully decides to redeem those ETF shares back*. The AP hands over the additional shares, while the ETF issuer hands over the unneeded stock - another in-kind transfer, after which the AP sells them on the market. The end effect is that the unneeded stock have been sold without triggering capital gains taxes.

**Accummulation and distribution**. As the ETF issuer owns the underlying stocks and they pay dividends, the ETF issuer gradually receives cash flows from them. The dividend cash flows collect into a holding account and the ETF issuer can periodically distribute them to the brokerage accounts of the individual investors. When this happens there's a small dip in the ETF price. Alternatively, the ETF manager could reinvest the dividends into the ETF itself, accumulating more stocks. This is basically like buying the dip: whenever a stock releases dividends, its price mechanically falls, and immediately the ETF issuer uses the new cash to buy more of that stock. So the amount of stocks held increases and the net asset value of the ETF rises faster.

**Net asset value**. As explained above, the ETF share price hovers around its NAV. It's calculated as 

$$
\text{NAV} = \frac{\text{Total Assets} - \text{Total Liabilities}}{\text{Shares Outstanding}}
$$

For an ETF issuer, assets include the current value of all stocks owned, the cash, and any receivables. The liabilities include any payables or management fees. The difference, or the *equity* part of the balance sheet, is precisely the NAV available to the ETF shareholders. Note that normal companies value their assets at the [historical cost](https://en.wikipedia.org/wiki/Historical_cost), potentially minus depreciation, but here, ETF issuers use the current market value. This is called [Mark-to-Market accounting](https://en.wikipedia.org/wiki/Mark-to-market_accounting) (MTM). ETFs use MTM because their product is the current market value. If they used historical cost, new investors would be able to buy into the fund at old prices and immediately sell for current, higher prices, robbing the long-term holders. Mark-to-market prevents this theft.

**Timing aspects**. The NAV is calculated once a day, after markets close and the closing prices for every stock can be obtained. This is easier said than done, because for ETFs holding stocks across different countries, at the time of calculating the NAV, in some countries the market could be closed, while in others not yet. To avoid stale pricing, the ETF managers may have to look at proxy instruments, like futures, to get a sense of what the current *fair value* of the stock in the closed market ought to be. They would then adjust the closing price from the closed market, which could be flat from many hours now, to estimate the current fair value. Even though the NAV is calculated once per day, there are *approximations* to it, like the iNAV, which are calculated throughout the day.



<!-- You should be able to identify when an ETF’s underperformance is due to:
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
Avoid common ETF traps that most retail investors fall into -->