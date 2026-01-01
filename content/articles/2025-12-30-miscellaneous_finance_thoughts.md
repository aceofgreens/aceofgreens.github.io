---
Title: Miscellaneous Investing Thoughts
Date: 2025-12-30 07:00:00 +0200
Tags: 
slug: miscellaneous_investing_thoughts
status: hidden
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
-1000 - \frac{1000}{1 + \text{MRW}} + \frac{2500}{(1 + \text{MWR})^{1.5}} = 0 \ \Rightarrow \ \text{MWR} \approx 11.7\%.
$$

The MWR is simply the internal rate of return of an asset with the same cashflows as those of the portfolio. It is money-weighted because it considers the amount deposited/withdrawn in each cashflow. Therefore, it can be used to gauge the performance of an individual investor's strategy, with timing and concrete amounts invested.