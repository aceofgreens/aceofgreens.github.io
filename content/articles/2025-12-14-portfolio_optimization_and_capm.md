---
Title: Portfolio Optimization and CAPM
Date: 2025-12-14 07:00:00 +0200
Tags: econ
slug: portfolio_optimization_and_capm
status: draft
---

Investing is important and it seems like almost everyone has an opinion on how to do it. I've decided to look at the problem setting a bit more formally, through the lens of portfolio optimization theory, to better understand its nuances.

**The market**. We model the return of an asset in a given period as a random variable with mean $m$ and variance $\sigma^2$. When there are $N$ such risky assets in the market, their means are a vector $\mathbf{m} \in \mathbb{R}^{N}$ and their covariance is a matrix $\mathbf{\Sigma} \in \mathbb{R}^{N, N}$. A portfolio is a combination of assets such that its return is a linear combination of the returns of the assets held. If the vector $\mathbf{x}$ represents the percentage of each asset, then the portfolio's mean return is $\mathbf{x}^T \mathbf{m}$, and its variance is $\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}$. In all that follows, we assume that $\mathbf{m}$ and $\mathbf{\Sigma}$ are known. This is, of course, far-fetched for the real world, but less so here.

**Utility**. Any investor in the market has a risk-profile representing his tolerance for risk. At the base of this stands, abstractly, a utility function that describes the subjective preference over different wealth levels. We denote it as $u(w)$. It basically says *"If my wealth is $w$, then my utility is $u(w)$".* A common one is called *constant relative risk aversion* (CRRA):
$$
u(w) = \begin{cases}
w^{1 - \gamma} / (1 - \gamma), & \text{ for } \gamma \ne 1 \\
\ln(w), & \text{ for } \gamma = 1.
\end{cases}
$$

It has the following properties. For any $w > 0$, since $u'(w) > 0$, this means that investors prefer more wealth to less, which is reasonable. Since $u''(w) < 0$, there are diminishing returns to having more wealth, which is also reasonable and realistic.

Consider what happens if we take $w$ to be the future wealth and to be uncertain, as coming from a risky asset. The distribution over $w$ induces a distribution over $u(w)$. However, the curvature of $u(\cdot)$, controlled by the parameter $\gamma$, greatly affects the possible values of $u(w)$. Therefore, if an investor cares about *expected utility* over the distribution of $w$, $\mathbb{E}_w [ u(w)]$, this quantity depends on $\gamma$. One can calculate the sensitivity $\partial \mathbb{E}_w[u(w)] / \partial \gamma$ to see the dependence exactly.

To see this in another light, consider that if $u(\cdot)$ is concave, then due to [Jensen's inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality), $u(\mathbb{E}_w[w]) \ge \mathbb{E}_w [u(w)]$. This means that if the risky asset is very risky, then $w$ can take on many different values. The more concave $u(\cdot)$ is, the more the investor prefers the mean wealth, which gives $u(\mathbb{E}_w[w])$, over a random one, which gives on average $\mathbb{E}_w [u(w)]$.   

Thus, the utility function carries with it an implicit risk-attitude. For CRRA, it is one where the investor is always risk-averse but his degree of risk-aversion stays constant at different levels of wealth. This is measured using the [Arrow–Pratt relative risk aversion formula](https://en.wikipedia.org/wiki/Risk_aversion#Relative_risk_aversion). If we calculate $-w u''(w) / u'(w)$, we get exactly $\gamma$, independent of $w$. It means that a 10% risk is evaluated the same whether you are poor or rich. А 1% increase in wealth reduces marginal utility always by $\gamma$%, irrespective of the wealth level.

**Mean-variance preferences**. Now we'll derive a simpler utility function based on the return's moments. The return is $r$, a small random number around 0. First, write the future utility $u\big(w(1 + r)\big)$ as a second-order Taylor approximation around the initial wealth $w$:

$$
u\big(w(1 + r)\big) \approx u(w) + u'(w)rw + \frac{1}{2}u''(w)(rw)^2.
$$

Now, since $r$ is stochastic and we assume the investor cares about expected utility,

$$
\begin{aligned}
\mathbb{E}_w \left[u\big(w(1+r)\big)\right] & \approx u(w) + u'(w_0)\mathbb{E}_w[rw] + \frac{1}{2}u''(w)\mathbb{E}_w\left[(rw) ^2\right] \\
& = u(w) + u'(w)\mathbb{E}_w[rw] + \frac{1}{2}u''(w) \big( \text{Var}(rw) + (\mathbb{E}_w[rw])^2 \big). \\
\end{aligned}
$$

This already shows utility in terms of mean and variance of the underlying asset, at least around the current $w$. For more concreteness, assume utility is CRRA and $r \sim N(\mu, \sigma^2)$. We get:

$$
\begin{aligned}
\mathbb{E}_w \left[u\big(w(1+r)\big)\right] & \approx w^{1 - \gamma} \left(\frac{1}{1 - \gamma} + \mu - \frac{\gamma}{2} (\sigma^2 + \mu^2) \right) \\
& \propto \text{const} + \mu - \frac{\gamma}{2}(\sigma^2 + \mu^2).
\end{aligned}
$$

Now, this is an approximation and it holds when $r \approx 0$. In that case, $\mu^2 \rightarrow 0$ and we get that expected utility depends positively on the mean return of the asset and negatively on the variance, of course assuming that $\gamma > 0$, which corresponds to risk-aversity. This is an important result: whatever utility or return distribution, expected utility can be locally approximated as a quadratic. It is not a too bad of an assumption to say most investors have utilities shaped in this way.

**Optimization**. Now, consider the choice between a risk-free asset paying $r_f$ and a single risky asset with mean return $\mu$ and variance $\sigma^2$. The investor chooses the percentage of wealth allocated to the risky asset, call it $x$, that maximizes expected utility:

$$
\max_x \ J(x) = (1 - x)r_f + x \mu - \frac{\gamma}{2} x^2 \sigma^2.
$$

Here $(1 - x)r_f + x \mu$ is the expected return of the portfolio and $x^2 \sigma^2$ is the variance. Taking the derivative wrt $x$ and setting it to zero immediately gives the solution

$$
x^\ast = \frac{1}{\gamma} \cdot \frac{\mu - r_f}{\sigma^2}.
$$

The quantity $(\mu - r_f)/\sigma^2$ is the excess mean return over the risk-free rate, per unit of variance. The optimal share in the risky asset $x^\ast$ is inversely proportional to this quantity. A higher $\gamma$ means holding less of the risky asset. Note that risk vs no-risk is not a binary choice. Unless you suffer from infinite risk-aversion ($\gamma = \infty$), it's always optimal to hold at least some amount of the risky asset.

**Many risky assets**. Now, let's solve the optimal investment problem with one risk-free and $N$ risky assets. The vector $\mathbf{x}$ contains the shares of the risky assets. The share of the risk-free asset is $1 - \mathbf{x}^T \mathbf{1}$, where $\mathbf{1}$ is a vector of $N$ ones. The problem becomes

$$
\max_\mathbf{x} \ J(\mathbf{x}) = \mathbf{x}^T\mathbf{m} + (1 - \mathbf{x}^T \mathbf{1}) r_f - \frac{\gamma}{2} \mathbf{x}^T \mathbf{\Sigma} \mathbf{x}.
$$

From the first-order condition $\mathbf{m} - r_f \mathbf{1} = \gamma \mathbf{\Sigma}\mathbf{x}$ we get $\mathbf{x}^\ast = \frac{1}{\gamma} \mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1})$. This is similar to before, the optimal allocation in the risky assets is a multiple of the mean excess return per unit of risk. If $\gamma$ is high, the share allocated in any of the risky assets could be minimal. The weights $\mathbf{x^ast}$ are unconstrained. If an element is negative, it represents shorting the asset, if it's greater than $1$, it represents borrowing and buying more.

**Best Sharpe ratio**. Consider another question: if we can invest only in risky assets, what portfolio has the highest excess mean return per unit of risk? This quantity, $(m_i - r_f)/\sigma_i$, is called the [Sharpe ratio](https://en.wikipedia.org/wiki/Sharpe_ratio#). Hence, we're seeking the portfolio with the highest Sharpe ratio:

$$
\max_\mathbf{x} \ J(\mathbf{x}) = \frac{\mathbf{x}^T\mathbf{m} - r_f \mathbf{1}}{\sqrt{\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}}} \ \text{ s. t. } \mathbf{x}^T \mathbf{1} = 1
$$

To solve this more easily, we square the objective function and maximize that instead. This is valid, because we assume that $\mathbf{m} > r_f$, so the numerator is positive, as is the denominator. For simplicity, denote the excess mean return $\mathbf{m} - r_f \mathbf{1}$ as $\mathbf{m}_+$. We solve the unnormalized setting first, where we pretend the constraint $\mathbf{x}^T \mathbf{m}$ does not exist. The FOC gives

$$
(\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}) \mathbf{m_+} = (\mathbf{x}^T \mathbf{m_+}) \mathbf{\Sigma}\mathbf{x} 
 \ \Rightarrow \ \mathbf{x}^\ast = \left[\frac{\mathbf{x}^T \mathbf{\Sigma}\mathbf{x}}{\mathbf{x}^T \mathbf{m_+}}\right] \mathbf{\Sigma}^{-1} \mathbf{m}_+.
$$

The term in the bracket is just a scalar constant. The point is that again we get $\mathbf{x}^\ast \propto \mathbf{\Sigma}^{-1} (\mathbf{m} - r_f \mathbf{1})$. To find the exact answer we substitute into the constraint that $\mathbf{x}$ has to sum up to 1 and obtain the final answer, the so-called tangency portfolio:

$$
\mathbf{x}_T = \frac{\mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1})}{\mathbf{1}^T \mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1})} \in \mathbb{R}^N
$$

This is the risky portfolio with the highest Sharpe ratio. It offers the highest excess mean return per unit of risk. The same vector $\mathbf{z} = \mathbf{\Sigma}^{-1} ( \mathbf{m} - r_f \mathbf{1})$ as in the expected utility problem, shows up also here! There it was scaled by the risk aversion, whereas here it's normalized. This proves that every single rational, mean-variance investor, regardless of their risk aversion $\gamma$, will choose to hold the same proportional mix of risky assets - the tangency portfolio $\mathbf{x}_T$.

There's also big theoretical result here. The [The Two-Fund Separation Theorem](https://en.wikipedia.org/wiki/Mutual_fund_separation_theorem) states that the investment decision can be separated into two independent tasks:

1. The investment decision (universal): determine the composition of the optimal risky portfolio, $\mathbf{x}_T$, by maximizing the Sharpe Ratio. This decision is purely technical and market-driven.
2. The financing decision (individual): determine the proportion of total wealth to invest in the tangency portfolio, $\mathbf{x}^{*T} \mathbf{1}$, and the proportion to invest in the risk-free asset, $1-\mathbf{x}^{*T} \mathbf{1}$. This is determined by the investor's individual risk tolerance $\gamma$.

Thus, if you're very risk-averse, hold less of the tangent portfolio and more of the risk-free asset. If you tolerate risk easily, hold more of the tangent portfolio and less of the risk-free asset. The point is that the tangency portfolio should be always held, with more or less wealth allocated to it.

**Capital allocation line**. We've identified that any investor first finds the tangency portfolio as the risky portfolio to invest in, and then scales the share allocated to it by their risk profile. If $y = \mathbf{x}^T \mathbf{1}$ is the total share in the tangency portfolio, then $1 - y$ is that of the risk-free asset. The return of the tangency portfolio is $r_T$, while that of the investor's portfolio is $r_S$, with $S$ standing for *scaled*. The statistics of $r_S$ are:

$$
\begin{aligned}
& \mathbb{E}[r^\ast] = y \mathbb{E}[r_T] + (1 - y)r_f = r_f + y (\mathbb{E}[r_T] - r_f) \\
& \sigma^2_S = y^2 \sigma_T^2 \ \Rightarrow \ \sigma_S = y \sigma_T
\end{aligned}
$$

From that last line we express $y = \sigma_S/\sigma_T$ and plug it into the mean return equation to obtain the Capital Allocation Line (CAL). It is a line in $(r_S, \sigma_S)$ space describing the linear risk-return relationship of the portfolio of *any* rational mean-variance investor. 

$$
\mathbb{E}[r_S] = r_f + \underbrace{\left[ \frac{\mathbb{E}[r_T] - r_f}{\sigma_T} \right]}_{\text{Sharpe ratio}} \sigma_S
$$

The investor should set the risk of his portfolio, $\sigma_S$, according to his risk-profile. Then, the mean return he can expect is given by the CAL. The slope of the CAL is the Sharpe ratio of the tangency portfolio, which has the highest Sharpe ratio of any portfolio in the market.

**Market equilibrium**. There are many investors in the market, each holding the same composition of risky assets. Let's assume they all share the same information for $\mathbf{m}$ and $\mathbf{\Sigma}$. Suppose also markets are perfect with no taxes, transaction costs, and all assets are infinitely divisible.

The *market portfolio* $M$ is the portfolio of all risky assets in the investment universe, weighted by their total market capitalization (price times the number of shares outstanding). It represents the supply of all risky assets. Likewise, since investors demand different multiples of the same tangency portfolio, their aggregate demand also has the same risky asset proportions in it as the tancency portfolio. At equilibrium, supply of risky assets must equal the demand for such. This means that at equilibrium the market portfolio is equal to the tangency portfolio.

That is the central and most powerful assertion of the [Capital Asset Pricing Model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model) (CAPM). The identity between the tangency and market portfolios is the crucial bridge that allows the theory of individual optimal choice ([modern portfolio theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)) to become a theory of market prices (CAPM). The former serves as microfoundations to the latter.

Now, we know that the market portfolio has the highest Sharpe ratio. Any other small deviation from it will reduce the Sharpe ratio. Hence, if we have a new portfolio, where we allocate a share $w$ to some asset $i$ and share $1 - w$ to the market portfolio, then the derivative of the Sharpe ratio of that combined new portfolio, evaluated at $w=0$, should be zero. Let's write it out. We denote the combined portfolio with $C$.

$$
\begin{aligned}
& \mathbb{E}[r_C] = w \mathbb{E}[r_i] + (1 - w) \mathbb{E}[r_M] \\
& \sigma^2_C = w^2 \sigma^2_i + (1 - w)^2 \sigma^2_M + 2 w(1 - w) \text{Cov}(i, M) \\
& \left[ \frac{\partial}{\partial w} \frac{\mathbb{E}[r_C] - r_f}{\sigma_C} \right]_{w = 0} = 0
\end{aligned}
$$

Now, the calculations are long and tedious, so we'll skip them. After computing the derivatives, substituting and simplifying one gets the so-called [Security Market Line](https://en.wikipedia.org/wiki/Security_market_line):

$$
\mathbb{E}[r_i] = r_f + \underbrace{\frac{\text{Cov}(r_i, r_M)}{\text{Var}(r_M)}}_{\beta_i} (\mathbb{E}[r_M] - r_f).
$$

It's a linear relationship between the mean return of asset $i$ and its covariance with the market portfolio. The slope is called the "beta" of asset $i$. If $\beta = 1$, the asset moves with the market. If $\beta > 1$, it's more volatile than the market. If $\beta < 0$, it moves opposite to the market. In general, $\beta$ measures what's called *systematic risk*. That's the unavoidable risk of participating in the market as a whole. It cannot be removed by diversification (holding different assets of varying correlations). And that's why CAPM compensates investors for it. Any risk that is endemic to an individual firm (e.g. a particular lawsuit, deal, event) could be diversified away by holding a bundle of assets, but not this kind of market-wide risk. 
