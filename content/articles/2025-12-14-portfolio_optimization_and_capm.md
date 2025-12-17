---
Title: Portfolio Optimization and CAPM
Date: 2025-12-14 07:00:00 +0200
Tags: econ
slug: portfolio_optimization_and_capm
status:
---

I've decided to look at the problem of portfolio optimization a bit more formally, to better understand its nuances. The end goal of this post is to explain the beta coefficient, observable in many finance websites. Along the way, we'll see how portfolio optimization serves as the microfoundations on equilibrium theories in the market of risky assets.

**The market**. We model the return of an asset in a given period as a random variable $r$ with mean $m$ and variance $\sigma^2$. When there are $N$ such risky assets in the market, their means are a vector $\mathbf{m} \in \mathbb{R}^{N}$ and their covariance is a matrix $\mathbf{\Sigma} \in \mathbb{R}^{N, N}$. A portfolio, also called a fund, is a combination of assets such that its return is a linear combination of the returns of the assets held. If the vector $\mathbf{x}$ represents the percentage of each asset, then the portfolio's mean return is $\mathbf{x}^T \mathbf{m}$, and its variance is $\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}$. In all that follows, we assume that $\mathbf{m}$ and $\mathbf{\Sigma}$ are known. This is, of course, far-fetched for the real world, but less so here.

**Utility**. Any investor in the market has a risk-profile representing his tolerance for risk. At the base of this stands, abstractly, a utility function that describes the subjective preference over different wealth levels. We denote it as $u(w)$. It basically says *"If my wealth is $w$, then my utility is $u(w)$".* A common one is called *constant relative risk aversion* (CRRA):
$$
u(w) = \begin{cases}
w^{1 - \gamma} / (1 - \gamma), & \text{ for } \gamma \ne 1 \\
\ln(w), & \text{ for } \gamma = 1.
\end{cases}
$$

It has the following properties. For any $w > 0$, since $u'(w) > 0$, this means that investors prefer more wealth to less, which is reasonable. Since $u''(w) < 0$, there are diminishing returns to having more wealth, which is also reasonable and realistic.

Consider what happens if we take $w$ to be the future wealth and to be uncertain, as coming from a risky asset. The distribution over $w$ induces a distribution over $u(w)$. However, the curvature of $u(\cdot)$, controlled by the parameter $\gamma$, greatly affects the possible values of $u(w)$. Therefore, if an investor cares about *expected utility* over the distribution of $w$, $\mathbb{E} [ u(w)]$, this quantity depends on $\gamma$. One can calculate the sensitivity $\partial \mathbb{E}[u(w)] / \partial \gamma$ to see the dependence exactly.

To see this in another light, consider that if $u(\cdot)$ is concave, then due to [Jensen's inequality](https://en.wikipedia.org/wiki/Jensen%27s_inequality), $u(\mathbb{E}[w]) \ge \mathbb{E} [u(w)]$. This means that if the risky asset is very risky, then $w$ can take on many different values. The more concave $u(\cdot)$ is, the more the investor prefers the mean wealth, which gives $u(\mathbb{E}[w])$, over a random one, which gives on average $\mathbb{E} [u(w)]$.   

Thus, the utility function carries with it an implicit risk-attitude. For CRRA, it is one where the investor is always risk-averse but his degree of risk-aversion stays constant at different levels of wealth. This is measured using the [Arrow–Pratt relative risk aversion formula](https://en.wikipedia.org/wiki/Risk_aversion#Relative_risk_aversion). If we calculate $-w u''(w) / u'(w)$, we get exactly $\gamma$, independent of $w$. It means that a 10% risk is evaluated the same whether you are poor or rich. А 1% increase in wealth reduces marginal utility always by $\gamma$%, irrespective of the wealth level.

**Mean-variance preferences**. Now we'll derive a simpler utility function based on the return's moments. The return is $r$, a small random number around 0, with $\mathbb{E} := \mathbb{E}_r$. First, write the future utility $u\big(w(1 + r)\big)$ as a second-order Taylor approximation around the initial wealth $w$:

$$
u\big(w(1 + r)\big) \approx u(w) + u'(w)rw + \frac{1}{2}u''(w)(rw)^2.
$$

Now, since $r$ is stochastic and we assume the investor cares about expected utility,

$$
\begin{aligned}
\mathbb{E} \left[u\big(w(1+r)\big)\right] & \approx u(w) + u'(w)\mathbb{E}[rw] + \frac{1}{2}u''(w)\mathbb{E}\left[(rw) ^2\right] \\
& = u(w) + u'(w)\mathbb{E}[rw] + \frac{1}{2}u''(w) \big( \text{Var}(rw) + (\mathbb{E}[rw])^2 \big). \\
\end{aligned}
$$

This already shows utility in terms of mean and variance of the underlying asset, at least around the current $w$. For more concreteness, assume utility is CRRA and $r \sim N(\mu, \sigma^2)$. We get:

$$
\begin{aligned}
\mathbb{E} \left[u\big(w(1+r)\big)\right] & \approx w^{1 - \gamma} \left(\frac{1}{1 - \gamma} + \mu - \frac{\gamma}{2} (\sigma^2 + \mu^2) \right) \\
& \propto \text{const} + \mu - \frac{\gamma}{2}(\sigma^2 + \mu^2).
\end{aligned}
$$

Now, this is an approximation and it holds when $r \approx 0$. In that case, $\mu^2$ is second-order and negligible relative to $\sigma^2$. Dropping it yields the standard mean–variance form $\mu - \frac{\gamma}{2} \sigma^2$, where expected utility depends positively on the mean return of the asset and negatively on the variance, of course assuming that $\gamma > 0$, which corresponds to risk-aversion. This is an important result: whatever utility or return distribution, expected utility can be locally approximated as a quadratic. It is not an unreasonable assumption to say most investors have utilities shaped in this way.

**Optimization**. Now, consider the choice between a risk-free asset paying $r_f$ and a single risky asset with mean return $\mu$ and variance $\sigma^2$. The investor chooses the percentage of wealth allocated to the risky asset, call it $x$, that maximizes expected mean-variance utility $\mathbb{E}[r] - \frac{\gamma}{2} \text{Var}(r)$:

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

From the first-order condition $\mathbf{m} - r_f \mathbf{1} = \gamma \mathbf{\Sigma}\mathbf{x}$ we get $\mathbf{x}^\ast = \frac{1}{\gamma} \mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1})$. This is similar to before, the optimal allocation in the risky assets is a multiple of the mean excess return divided by the variance. If $\gamma$ is high, the share allocated in any of the risky assets could be minimal. Apart from summing to one, the weights $\mathbf{x}^\ast$ are unconstrained. If an element is negative, it represents shorting the asset, if it's greater than $1$, it represents borrowing and buying more of it.

**Best Sharpe ratio**. Consider another question: if we can invest only in risky assets, what portfolio $P$ has the highest excess mean return per unit of risk? This quantity, $(\mathbb{E}[r_P] - r_f)/\sigma_P$, is called the [Sharpe ratio](https://en.wikipedia.org/wiki/Sharpe_ratio#). Hence, we're seeking the portfolio with the highest Sharpe ratio:

$$
\max_\mathbf{x} \ J(\mathbf{x}) = \frac{\mathbf{x}^T(\mathbf{m} - r_f \mathbf{1})}{\sqrt{\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}}} \ \text{ s. t. } \mathbf{x}^T \mathbf{1} = 1
$$

To solve this more easily, we square the objective function and maximize that instead. This is valid, because we assume the optimal portfolio has positive excess returns, so the numerator is positive, as is the denominator. For simplicity, denote the excess mean return $\mathbf{m} - r_f \mathbf{1}$ as $\mathbf{m}_+$. 

Observe that the Sharpe ratio is homogeneous of order zero, meaning that $J(c \mathbf{x}) = J(\mathbf{x}), c \in \mathbb{R}$. Hence, it's the direction of $\mathbf{x}$ that changes the Sharpe ratio, while the constraint $\mathbf{x}^T \mathbf{1} = 1$ only turns the optimizer into a portfolio by ensuring that all wealth is allocated. Hence, we solve without the constraint first, and then simply normalize it. The FOC gives

$$
(\mathbf{x}^T \mathbf{\Sigma} \mathbf{x}) \mathbf{m_+} = (\mathbf{x}^T \mathbf{m_+}) \mathbf{\Sigma}\mathbf{x} 
 \ \Rightarrow \ \mathbf{x} = \left[\frac{\mathbf{x}^T \mathbf{\Sigma}\mathbf{x}}{\mathbf{x}^T \mathbf{m_+}}\right] \mathbf{\Sigma}^{-1} \mathbf{m}_+.
$$

The term in the brackets is just a scalar constant. The point is that again we get $\mathbf{x} \propto \mathbf{\Sigma}^{-1} (\mathbf{m} - r_f \mathbf{1})$. To find the exact answer we substitute into the constraint that $\mathbf{x}$ has to sum up to 1 and obtain the final answer, the so-called tangency portfolio:

$$
\mathbf{x}_T = \frac{\mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1})}{\mathbf{1}^T \mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1})} \in \mathbb{R}^N
$$

This is the risky portfolio with the highest Sharpe ratio. It offers the highest excess mean return per unit of risk. Observe that the optimizer of the Sharpe ratio is denoted as $\mathbf{x}_T$, while that of the mean-variance utility is $\mathbf{x}^\ast$. The same vector $\mathbf{z} = \mathbf{\Sigma}^{-1} ( \mathbf{m} - r_f \mathbf{1})$ shows up in both solutions! In $\mathbf{x}^\ast$ it was scaled by the risk aversion, whereas in $\mathbf{x}_T$ it's normalized. This proves that every single rational, mean-variance investor, regardless of their risk aversion $\gamma$, will choose to hold the same proportional mix of risky assets - the tangency portfolio $\mathbf{x}_T$.

There's also big theoretical result here. The [The Two-Fund Separation Theorem](https://en.wikipedia.org/wiki/Mutual_fund_separation_theorem) states that the portfolio optimization can be separated into two independent tasks:

1. The investment decision (universal): determine the composition of the optimal risky portfolio, $\mathbf{x}_T$, by maximizing the Sharpe Ratio. This decision is purely technical and market-driven.
2. The financing decision (individual): determine the proportion of total wealth to invest in the tangency portfolio, $\mathbf{x}^{*T} \mathbf{1}$, and the proportion to invest in the risk-free asset, $1-\mathbf{x}^{*T} \mathbf{1}$. This is determined by the investor's individual risk tolerance $\gamma$.

Thus, if you're very risk-averse, hold less of the tangent portfolio and more of the risk-free asset. If you tolerate risk easily, hold more of the tangent portfolio and less of the risk-free asset. The point is that the tangency portfolio should be always held, with more or less wealth allocated to it. The two fund theorem obtains its name from the fact that only two funds, the tangency and the risk-free one, are needed to identify all the configurations that any rational investor would select.

**Capital allocation line**. We've shown that an investor first finds the tangency portfolio as the risky portfolio to invest in, and then scales the share allocated to it by their risk profile. If $y = \mathbf{x}^{\ast T} \mathbf{1}$ is the total share in the tangency portfolio, then $1 - y$ is that of the risk-free asset. The return of the tangency portfolio is $r_T$, while that of the investor's portfolio is $r_S$, with $S$ standing for *scaled*. The statistics of $r_S$ are:

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

The investor finds the tangency portfolio and based on his risk-profile, decides whether to invest more or less in it, which changes the risk $\sigma_S$ of the resulting scaled portfolio. Then, the mean return he can expect is given by the CAL. The slope of the CAL is the Sharpe ratio of the tangency portfolio, which has the highest Sharpe ratio of any portfolio in the market.

**Market equilibrium**. Now suppose there are many investors in the market. Let's assume they all share the same information for $\mathbf{m}$ and $\mathbf{\Sigma}$ but have different risk attitudes. Suppose also markets are perfect with no taxes, transaction costs, and all assets are infinitely divisible.

The *market portfolio* $M$ is the portfolio of all risky assets available in the investment universe, weighted by their total market capitalization (price times the number of shares outstanding). It represents the aggregate supply of all risky assets. Its weights are $\mathbf{x}_M = (P_i Q_i) / \sum_{j} P_j Q_j$.

Since investors demand different multiples of the same tangency portfolio, aggregate demand also has the same risky asset proportions in it as the tangency portfolio. At equilibrium, supply of risky assets must equal the demand for such. This means that at equilibrium the market portfolio is equal to the tangency portfolio, $\mathbf{x}_M = \mathbf{x}_T$.

That is the central and most powerful assertion of the [Capital Asset Pricing Model](https://en.wikipedia.org/wiki/Capital_asset_pricing_model) (CAPM). The identity between the tangency and market portfolios is the crucial bridge that allows the theory of individual optimal choice ([modern portfolio theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)) to become a theory of market prices (CAPM). The former serves as microfoundations to the latter. Pricing here refers to computing the fair expected return of an asset with a certain risk relative to the market.

**Price adjustments**. As defined, $\mathbf{x}_M$ has all of its weights in $[0, 1]$, whereas in $\mathbf{x}_T$ some weights could be greater than one, or even negative. How do we deal with this? CAPM is a static model. It claims that the two portfolios are equal, without much justification. But in reality, to reach equilibrium there are price-adjustment dynamics. As a heuristic, if investors short asset $i$, this brings its current price $P_i$ down. As it does so, the expected mean $m_i = {P_\text{i, future}} / P_i - 1$ increases (holding $P_\text{i, future}$ fixed). In this way, the tangency portfolio adjusts. The bottomline is that portfolio optimization works with expected returns and at equilibrium, because of the price-adjustment dynamics, the tangency portfolio has weights in $[0, 1]$. 

We can ask the question *"What must $\mathbf{m}$ be given that $\mathbf{x}_T = \mathbf{x}_M$?"* To see, we plug in and solve:

$$
\mathbf{x}_T \propto \mathbf{\Sigma}^{-1}(\mathbf{m} - r_f \mathbf{1}) \ \Rightarrow \ \mathbf{m} - r_f\mathbf{1} \propto \mathbf{\Sigma} \mathbf{x}_M
$$

This last equation shows that in order for markets to clear, the expected return over risk-free rate must align perfectly with the covariance term $\mathbf{\Sigma}\mathbf{x}_M$. 

**Security market line**. At equilibrium the market portfolio has the highest Sharpe ratio. Any other small deviation from it will reduce the Sharpe ratio. Hence, if we have a new portfolio, where we allocate a share $w$ to some asset $i$ and share $1 - w$ to the market portfolio, then the derivative of the Sharpe ratio of that combined new portfolio, evaluated at $w=0$, should be zero. Let's write it out. We denote the combined portfolio with $C$.

$$
\begin{aligned}
& \mathbb{E}[r_C] = w \mathbb{E}[r_i] + (1 - w) \mathbb{E}[r_M] \\
& \sigma^2_C = w^2 \sigma^2_i + (1 - w)^2 \sigma^2_M + 2 w(1 - w) \text{Cov}(r_i, r_M) \\
& \left[ \frac{\partial}{\partial w} \frac{\mathbb{E}[r_C] - r_f}{\sigma_C} \right]_{w = 0} = 0
\end{aligned}
$$

The calculations are long and tedious, so we'll skip them. After computing the derivatives, substituting, and simplifying, one gets the so-called [Security Market Line](https://en.wikipedia.org/wiki/Security_market_line):

$$
\mathbb{E}[r_i] = r_f + \underbrace{\frac{\text{Cov}(r_i, r_M)}{\text{Var}(r_M)}}_{\beta_i} (\mathbb{E}[r_M] - r_f).
$$

It's a linear relationship between the mean return of asset $i$ and its covariance with the market portfolio. The slope is called the "beta" of asset $i$. If $\beta > 1$, the asset has higher systematic exposure than the market and amplifies market movements. If $\beta < 0$, it moves opposite to the market. To understand it intuitively, we need to first understand *systematic* and *unsystematic* risk.

**Unsystematic risk**. The return from a risky asset could be high or low because the issuing company has struck a major deal with a partner, or is facing a tough lawsuit. These are individual, idiosyncratic reasons related to the company itself. They are *diversifiable*: when this risky asset is mixed with others, the combined portfolio variance could be lower than that of its individual assets. 

**Systematic risk**. Other risks, such as the risk of the entire market tanking or booming, cannot be avoided. If you participate in the market, you're open to such risk. Hence, it's called systematic. It cannot be diversified away. Common examples are inflation, interest rate risks, business cycles, quantitative easing/tightening, tax changes.

The parameter $\beta$ measures systematic risk. Since this risk is unavoidable, CAPM compensates investors for it. If an asset contributes $\beta$ times as much systematic risk as the market portfolio, then it must offer $\beta$ times the market risk premium. Interestingly, if $\beta < 1$, the asset could still be more volatile than the market if most of its risk is idiosyncratic. CAPM is also a *single-factor* model because there's only one factor that is compensated, systematic risk. In contrast, there exist multiple factor models (e.g. [Fama-French three factor](https://en.wikipedia.org/wiki/Fama%E2%80%93French_three-factor_model)) which model the return as 
$$
r_i - r_f = \alpha_i + \sum_{k=1}^K \beta_{ik} F_k + \epsilon_i.
$$

Here there are $K$ factors, each with coefficient $\beta_{ik}$, along with an abnormal return term $\alpha_i$. CAPM predicts $\alpha_i = 0, \ \forall i$, but in reality some companies and assets could be estimated, for example due to model misspecification or omitted risk factors, to have $\alpha > 0$, i.e. returns above those that pricing models predict.  Hedge funds are meticulously seeking this alpha.

An asset with statistics $(m_i, \sigma_i)$ is efficient, or undominated, if there is no other portfolio that offers the same return for a smaller risk, or that has the same risk but with a higher return. The CAL of portfolio $P$, as we saw above, contains all portfolios which are a combination of the risk-free asset and that particular portfolio $P$. If $P$ is some inefficient asset, its entire CAL will be dominated. The CAL of the tangency portfolio is called the Capital Market Line (CML). The CML is one particular CAL, and the only one which is non-dominated.

The key difference between the SML and the CML is that SML uses systematic risk, instead of total risk, and in this way determines how much the return *should* be if supply equals demand. That's where the concept of equilibrium stems from. The SML can also price inefficient assets. For instance, an inefficient asset may have too high risk for its return. To price it, CAPM says: if this risk is mostly idiosyncratic, its return should be small. If it's mostly unavoidable systematic risk, then its return should be higher. To measure systematic risk, we use the asset’s covariance with the market.

We've come a long way and have shown a complete derivation chain: `utility → mean–variance approximation → optimal portfolios → tangency → equilibrium → CAPM → SML pricing`. The strongest assumption was that all investors share their expectations over $\mathbf{m}$ and $\mathbf{\Sigma}$. Yet, without such homogeneous beliefs, the market portfolio need not be mean–variance efficient. This motivates further research beyond CAPM.