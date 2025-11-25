---
Title: Intertemporal Choice
Date: 2025-11-21 07:00:00 +0200
Tags: econ, rl, ultra-rationalism
slug: intertemporal_choice
status:
---

I want to explore the fundamental topic of intertemporal discounting - the preference toward current, as opposed to delayed, future satisfaction. This preference is innate in humans. We prefer the same amount of goods now, rather than tomorrow. If we are to receive them tomorrow, we demand *more* of them, so the additional amount compensates for the temporal delay. Intertemporal discounting stands at the foundation of many economic behavioral patterns - consumption, saving, fiscal restraint, discipline. We'll explore the topic from different angles: econ, reinforcement learning, and neuroeconomics.

### The Euler Equation

Optimal intertemporal choice is often governed by the Euler equation, which represents a necessary but not sufficient condition for a candidate optimal path in a temporal decision problem. Let's explore the equation through a concrete example:

- Single household, infinitely-lived, that seeks to choose how much to consume at each timestep $t$, indicated by $c(t)$, so as to maximize its long-term discounted utility, $u\big(c(t)\big)$
- The household's utility $u(\cdot)$ is an increasing function, as people always prefer more goods to less, but at a decreasing rate, as the marginal benefit of each additional unit consumed contributes less and less. So $u'(\cdot) > 0$ and $u''(\cdot) < 0$.
- The household produces one unit of labor at any $t$ and receives a wage such that it can afford $w(t)$ units of consumption.
- It can borrow to consume more than it has today, but it cannot borrow indefinitely.
- Markets are competitive. Wages $w(t)$ equal the marginal productivity of labor and interest $r(t)$ equals the marginal productivity of capital. 

We denote a continuously applied, future discount factor with constant rate $\rho$ as $e^{-\rho t}$. The household's initial wealth is $K_0$. Its optimization problem is to choose how much to consume, $c(t)$, so that it maximizes the present value of all future utility. However, it should keep the present value of its expenditure on consumption lower than that of its income, this being its budget constraint.

$$
\begin{aligned}
 \max_{c(t)} & \int_0^\infty e^{-\rho t} u\big(c(t)\big) dt \\
 \text{s. t.} &\int_{t=0}^\infty e^{-R(t)} c(t) dt \le K_0 + \int_{t=0}^\infty e^{-R(t)} w(t)dt.
\end{aligned}
$$

Note how a flow at time $t$ is discounted with the cumulative interest up to time $t$, $R(t) = \int_0^t r(\tau)d\tau$. The budget constraint can be rewritten as a limit up to a fixed $s$, with $s$ tending toward infinity $(^\ast)$. We can also write the household's wealth at time $s$, denoted $K(s)$, where each income, say from time $t$, has accumulated interest from $t$ to $s$ $(^{\ast\ast})$

$$
\begin{aligned}
^\ast & \lim_{s \rightarrow \infty} \left[K_0 + \int_{t=0}^s e^{-R(t)} \big(w(t) - c(t)\big)dt \right]\ge 0 \\
^{\ast\ast} & K(s) = K_0 e^{R(s)} + \int_{t=0}^s e^{R(s) - R(t)} \big(w(t) - c(t) \big)dt,
\end{aligned}
$$

Now, note that equation $^{\ast\ast}$ is exactly $e^{R(s)}$ times the expression in the brackets of equation $^\ast$. Therefore the budget constraint can be equally rephrased simply as requiring that for any long-term time $s$, the present value (PV) of the household's wealth should be non-negative:

$$
\lim_{s \rightarrow \infty} e^{-R(s)}K(s) \ge 0.
$$

This is a *no-Ponzi-game condition*. It prevents the agent from accumulating debt and rolling it over forever. The PV of lifetime consumption should not exceed that of your lifetime resources.

Since utility is increasing, the budget constraint should be satisfied with equality. Let's assume a concrete utility function, $u(c) = c^{1 - \theta}/(1 - \theta)$, called [constant relative risk aversion](https://en.wikipedia.org/wiki/Risk_aversion#Relative_risk_aversion) (CRRA). With this, we can formulate the following Lagrangian and obtain the first-order conditions (FOCs) using calculus of variations:

$$
\begin{aligned}
& \mathcal{L} = \int_{t=0}^\infty e^{-\rho t} \frac{c(t)^{1 - \theta}}{1 - \theta} dt + \lambda \Big(K_0 + \int_{t=0}^\infty e^{-R(t)}\big(w(t) - c(t)\big) dt \Big)\\
& \frac{\partial \mathcal{L}}{\partial c(t)} = 0 \ \Rightarrow \  e^{-\rho t} c(t)^{-\theta} = \lambda e^{-R(t)}.
\end{aligned}
$$

Let's study the FOC a bit. Take the log of both sides, we get $-\rho t - \theta \ln c(t) = \ln \lambda - R(t)$. Upon differentiation with respect to time and rearranging we get the Euler equation

$$
\frac{\dot{c}(t)}{c(t)} = \frac{r(t) - \rho}{\theta}.
$$

This is a behavioral equation. It says that when acting optimally the household increases its consumption whenever the current rate of return $r(t)$ is greater than the discount rate $\rho$, and decreases it otherwise. Specifically, the rate of change $\dot{c}/c$ is given by the difference.

We can also derive the Euler equation in terms of utility. Start with the FOC expressed as utility $e^{-\rho t} u'\big(c(t)\big) = \lambda e^{-R(t)}$. Differentiate both sides with respect to time, substitute $e^{-\rho t} u'\big(c(t)\big)$ within $\lambda e^{-R(t)}$ in the resulting expression, and rearrange to obtain

$$
\frac{d}{dt} \ln u'\big(c(t)\big) = \rho - r(t). 
$$

This is, again, the Euler equation but in terms of utility and valid for any reasonable utility function, not only CRRA. Here $u'\big(c(t)\big)$ is the derivative of $u$ with respect to $c$. Intuitively, if we increase consumption infinitesimally, marginal utility falls infinitesimally. That's why the sign of $\rho - r(t)$ is flipped compared to the consumption version. Finally, consider the discrete-time Euler equation, where we set the discount factor to $0 < \beta < 1$:

$$
u'(c_t) = \beta (1+r) u'(c_{t+1}), \text{ where } 0 < \beta < 1.
$$

Hold the overall consumption path fixed except for a marginal reallocation of one unit from today to tomorrow. Reducing consumption today by a small amount raises marginal utility by $u'(c_t)$. Saving that amount yields $(1+r)$ in additional resources tomorrow, whose marginal utility is $u'(c_{t+1})$ but will require discounting by $\beta$. The left-hand side is the marginal cost of shifting one unit of consumption to the future; the right-hand side is the discounted marginal benefit of consuming the resulting resources tomorrow. Optimality requires these two margins to be equal.

### Permanent Income Hypothesis

Before we discuss the qualitative aspects of consumption, let's solve the household's optimization. From the Euler equation for consumption, by integrating and exponentiating we get
$$
c(t) = A \exp\left(\int_0^t \frac{r(\tau) - \rho}{\theta}d\tau\right).
$$

Here $A$ is a constant and the consumption path depends only on $r(t), \rho, \theta$. Whenever $r(t) > \rho$, consumption increases, otherwise it decreases. When $r(t)$ is much greater than $\rho$, consumption increases faster. If "on average" $r(t)>\rho$, the consumption will increase exponentially to infinity. This is because it's better to reduce consumption now, save, profit from the high interest rate, and consume more later. So consumption later should be higher than now, hence rising. Similarly, if on average $r(t) < \rho$, in the far future consumption will tend to zero. While $\rho$ is a pure subjective discount rate, $\theta$ governs how costly it is to change the consumption path. 

$$
A = \frac{K_0 + \int_0^\infty e^{-R(t)}w(t) dt}{\int_0^\infty e^{-R(t)} \exp\left(\int_0^t \frac{r(\tau) - \rho}{\theta}d\tau\right)dt}
$$

The constant $A$ is determined easily from the budget constraint. This is the only place where $w(t)$ enters. Therefore, the lifetime income $w(t)$ determines the overall consumption level, while the actual path is determined by $r(t)$. Overall, $c(t)$ can be very complicated. It's interesting to plot it for different values of $\rho, \theta$, and different $w(t), r(t)$. Diverse behavior is possible.

The Euler equation is used in *many* settings and its exact functional form often depends on the specific technical problem. Here we'll adopt a slightly higher view. Consider the [Permanent Income Hypothesis](https://en.wikipedia.org/wiki/Permanent_income_hypothesis) (PIH). It says that consumption patterns are formed by future expectations and consumption smoothing, effectively by following the reasoning from above.

1. Households base their consumption not only on their current wealth, but their expected, *permanent*, lifetime wealth. It's coming from the sequence of expected wages $w(t)$.
2. Transient income shocks affect consumption less than permanent ones. Consider the unrealistic income function $w(t) = t$. With it, $c(t)$ has a certain smooth shape. Now consider $w(t) = t + 50\exp\big(-(t-20)^2\big)$. Income now has a noticeable spike at $t=20$. Optimal consumption doesn't have a spike at $t=20$ and has barely moved. Instead, if there's a permanent change, say income changes to $w(t)=1.1t$, then the entire consumption path changes quite noticeably. Transient income shocks barely affect lifelong wealth.
3. The Euler equation smooths out consumption. Even if income is stochastic and noisy, consumption evolves according to intertemporal preferences and market returns, not according to income fluctuations. This is the dynamic smoothing aspect of the PIH.

Does the PIH hold in the real world? There is a lot of evidence both for and against it. PIH agents are typically unconstrained and patient. Unconstrained means they can borrow however much they want and they have access to liquid financial assets so they can easily accumulate the interest $r(t)$. Instead, in the **Hand-to-mouth** model there are no assets and you cannot smooth consumption. A middle ground is the **Buffer-stock** model, in which agents have some income risk, are impatient, or have borrowing limits. There, households hold liquid assets as a [buffer against income risk](https://en.wikipedia.org/wiki/Buffer_stock_scheme), not to smooth consumption perfectly over the life cycle. Thus, evidence does not always favor PIH.

Consider one last important insight. Suppose a consumer uses PIH and doesn't care about risk, so that $w(t)$ is the expected income, $w(t) = \mathbb{E}[W]$. With rational expectations, all the available knowledge is already contained in the income estimate $w(t)$. Yet, as life goes on, a consumer will shift their consumption path as new information about their lifelong income comes in (e.g. an unexpected promotion). It follows that it is the unpredictable events that shift consumption. Hence, changes in consumption are unpredictable. They're a [random walk](https://en.wikipedia.org/wiki/Random_walk_model_of_consumption).

### Neuroeconomics and Policy

It's useful to list some other insights that are all related to intertemporal choice:

- Discounted utility assumes that if, say, one unit today is preferred over 2 units tomorrow, 1 unit 100 days from now will still be preferred over 2 units 101 days from now. This is contested by [hyperbolic discounting](https://en.wikipedia.org/wiki/Hyperbolic_discounting), which very steeply discounts immediate future payoffs, but for longer horizons, far away into the future, the rate of falloff is much slower.
- In terms of brain areas, it seems there are dual-system dynamics. Limbic regions (ventral striatum, posterior cingulate) respond more strongly to immediate rewards, while prefrontal regions (dorsolateral prefrontal cortex) support patience and planning. Dopamine also plays a role. Higher dopamine availability in the striatum is associated with lower discount rates (more patience), and disruptions increase impulsive choice.
- Discounting plays a central part also in reinforcement learning. The brain areas responsible there partially overlap with those associated with intertemporal choice, especially when it comes to encoding subjective values. RL relies on dopaminergic prediction-error signals (ventral tegmental area to striatum) and the representation of contingencies.

Regarding policies, in intertemporal choice the policies that matter most are the ones that directly change the relative price of consuming today vs. in the future. Everything else is secondary.

- The real interest rate $r$ is the price of shifting consumption across time. This is the most important variable. A higher $r$ implies more saving and less consumption.
- Taxation of capital income. A tax on interest, dividends, or capital gains decreases real return.
- Taxation of labor income. They affect the level of optimal consumption (under PIH) but not usually the intertemporal slope unless the taxes are age-dependent.
- Borrowing constraints. If the agent cannot borrow or consumption becomes liquidity-constrained, this will cause suboptimal outcomes.
- Social security, pensions, unemployment insurance usually reduce private discretionary saving.

Overall, it seems that we should strive for a well-oiled, healthy financial system and lots of education to emphasize the fundamental importance of saving and investing.  
