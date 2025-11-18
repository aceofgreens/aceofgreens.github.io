---
Title: Intertemporal Discounting
Date: 2025-11-15 07:00:00 +0200
Tags: econ, rl, ultra-rationalism
slug: intertemporal_discounting
status:
---

I want to explore the fundamental topic of intertemporal discounting - the preference toward current, as opposed to delayed, future satisfaction. This preference is innate in humans. We prefer the same amount of goods now, rather than tomorrow. If we are to receive them tomorrow, we demand *more* of them, so the additional amount compensates for the temporal delay. Intertemporal discounting stands at the [base](synonym?) of many economic behavioral patterns - consumption, saving, fiscal restraint, discipline. We'll explore the topic from different angles: econ, reinforcement learning, and neuroeconomics.

### The Euler Equation

Optimal intertemporal choice is often governed by the Euler equation, which represents a necessary but not sufficient condition for a candidate optimal path in a temporal decision problem. Let's explore the equation through a concrete example:

- Single household, infinitely-lived, that seeks to choose how much to consume at each timestep $t$, indicated by $c_t$, so as to maximize its long-term discounted utility, $u(c_t)
- The household's utility $u(\cdot)$ is an increasing function, as people always prefer more goods to less, but at a decreasing rate, as the marginal benefit of each additional unit consumed contributes less and less. So $u'(\cdot) > 0$ and $u''(\cdot) < 0$.
- The household produces one unit of labor at any $t$ and receives a wage such that it can afford $w(t)$ units of consumption.
- It can borrow to consume more than it has today, but it cannot borrow indefinitely.
- Markets are competitive. Wages $w(t)$ equal the marginal productivity of labor and interest $r(t)$ equals the marginal productivity of capital. 

We denote a continuously applied, future discount factor with constant rate $\rho$ as $e^{-\rho t}$. The household's initial wealth is $K_0$. Its optimization problem is to choose how much to consume, $c_t$, so that it maximizes the present value of all future utility. However, it should keep the present value of its expenditure on consumption lower than that of its income, this being its budget constraint.

$$
\begin{aligned}
 \max_{c_t} & \int_0^\infty e^{-\rho t} u(c_t) dt \\
 \text{s. t.} &\int_{t=0}^\infty e^{-R(t)} c(t) dt \le K_0 + \int_{t=0}^\infty e^{-R(t)} w(t)dt.
\end{aligned}
$$

Note how a flow at time $t$ is discounted with the cumulative interest up to time $t$, $R(\tau) = \int_0^\tau r(t)dt$. The budget constraint can be rewritten as a limit up to a fixed $s$, with $s$ tending toward infinity $(^\ast)$. We can also write the household's wealth at time $s$, denoted $K(s)$, where each income, say from time $t$, has accumulated interest from $t$ to $s$ $(^{\ast\ast})$

$$
\begin{aligned}
^\ast & \lim_{s \rightarrow \infty} \left[K_0 + \int_{t=0}^s e^{-R(t)} \big(w(t) - c(t)\big)dt \right]\ge 0 \\
^{\ast\ast} & K(s) = K_0 e^{R(s)} + \int_{t=0}^s e^{R(s) - R(t)} \big(w(t) - c(t) \big)dt,
\end{aligned}
$$

Now, note than equation $^{\ast\ast}$ is exactly $e^{R(s)}$ times the expression in the brackets of equation $^\ast$. Therefore the budget constraint can be equally rephrased simply as requiring that for any long-term time $s$, the present value (PV) of the household's wealth should be non-negative:

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

We can also derive the Euler equation in terms of utility. Start with the FOC expressed as utility $e^{-\rho t} u'(c_t) = \lambda e^{-R(t)}$. Differentiate both sides with respect to time, substitute $e^{-\rho t} u'(c_t)$ within $\lambda e^{-R(t)}$ in the resulting expression, and rearrange to obtain

$$
\frac{d}{dt} \ln u'(c_t) = \rho - r(t). 
$$

This is, again, the Euler equation but in terms of utility and valid for any reasonable utility function, not only CRRA. Here $u'(c_t)$ is the derivative of $u$ with respect to $c$. Intuitively, if we increase consumption infinitesimally, marginal revenue falls infinitesimally. That's why the sign of $\rho - r(t)$ is flipped compared to the consumption version. Finally, consider the discrete-time Euler eqn:

$$
u'(c_t) = \rho (1+r) u'(c_{t+1}), \text{ where } 0 < \rho < 1.
$$

Hold the overall consumption path fixed except for a marginal reallocation of one unit from today to tomorrow. Reducing consumption today by a small amount raises marginal utility by $u'(c_t)$. Saving that amount yields $(1+r)$ in additional resources tomorrow, whose marginal utility is $u'(c_{t+1})$ but will require discounting by $\rho$. The left-hand side is the marginal cost of shifting one unit of consumption to the future; the right-hand side is the discounted marginal benefit of consuming the resulting resources tomorrow. Optimality requires these two margins to be equal.

### Permanent Income Hypothesis

Before we discuss the qualitative aspects of consumption, let's solve the household's optimization. From the Euler equation for consumption, by integrating and exponentiating we get
$$
c(t) = A \exp\left(\int_0^t \frac{r(\tau) - \rho}{\theta}d\tau\right).
$$

Here $A$ is a constant and the consumption path depends only on $r(t), \rho, \theta$. Whenever $r(t) > \rho$, consumption incrases, otherwise it decreases. When $r(t)$ is much greater than $\rho$, consumption increases faster. If "on average" $r(t)>\rho$, the consumption will increase exponentially to infinity. This is because it's better to reduce consumption now, save, profit from the high interest rate, and consume more later. So consumption later should be higher than now, hence rising. Similarly, if on average $r(t) < \rho$, in the far future consumption will tend to zero. A small $\theta$ prioritizes consumption sooner rather than later, while $\rho$ is the personal discount rate of household. 

$$
A = \frac{K_0 + \int_0^\infty e^{-R(t)}w(t) dt}{\int_0^\infty e^{-R(t)} \exp\left(\int_0^t \frac{r(\tau) - \rho}{\theta}d\tau\right)dt}
$$

The constant $A$ is determined easily from the budget constraint. This is the only place where $w(t)$ enters. Therefore, the lifetime income $w(t)$ determines the overall consumption level, while the actual path is determined by $r(t)$. Overall, $c(t)$ can be very complicated. It's interesting to plot it for different values of $\rho, \theta$, and different $w(t), r(t)$. Diverse behavior is possible.


The Euler equation is used in *many* settings and its exact functional form often depends on the specific technical problem. Here we'll adopt a slightly higher view. Consider the [Permanent Income Hypothesis](https://en.wikipedia.org/wiki/Permanent_income_hypothesis) (PIH). It says that consumption patterns are formed by future expectations and consumption smoothing, effectively by following the reasoning from above.

1. Household base their consumption not only on their current wealth, but their expected, *permanent*, lifetime wealth. It's coming from the sequence of expected wages $w(t)$.
2. Transient income shocks affect consumption less than permanent ones. Consider the unrealistic income function $w(t) = t$. With it, $c(t)$ has a certain smooth shape. Now consider $w(t) = t + 50\exp\big(-(x-20)^2\big)$. Income now has a noticeable spike at $t=20$. Optimal consumption also has a spike at $t=20$, very localized, and is otherwise exactly similar to its form without the spike.