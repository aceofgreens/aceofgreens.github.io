---
Title: Solving Markets With RL
Date: 2025-03-17 07:00:00 +0200
Tags: econ, rl
slug: solving_markets_with_rl
---

I was recently tinkering with some fairly realistic oligopolistic market simulations. Compared to textbook cases, where it is common to assume the market matches all buyers to all sellers simultaneously, in my case the simulation involved non-clearing markets, sequential search, and various computational constraints among the market participants. If you think about it, it gets quite hard to solve the market in this case. Analytic solutions are out of the question. One typically has to use numerical methods. Yet, I had the beautiful idea of using multi-agent RL for finding the equilibria. It turned out to be a very nice bridge between the two disciplines - one providing the problem setting, and another providing the tool to solve it.

### Background

Let's motivate the problem by building toward it from the ground up. We'll recap consumption and production, and then build the mathematical structure of the market.

**Consumption**. Consumers have preferences over world states. They can be expressed as binary relations between different bundles of goods. E.g. if the world state in which one has $q_1$ units of good A and $q_2$ units of good B is preferred over $q_1$ units of good B and $q_2$ of good A, we can denote this as $(q_1, q_2) \succeq (q_2, q_1)$. Here the quantities are what matters.

Now, under various important assumptions, called the [axioms of rational choice](https://en.wikipedia.org/wiki/Von_Neumann%E2%80%93Morgenstern_utility_theorem), these preferences are captured by a cardinal utility function. Its values are meaningless, yet it accurately captures the same preferences, so we might say that $u(q_1, q_2) \ge u(q_2, q_1)$. If peopel are rational, they would maximize this expected utility.

Consumption is about choosing how to best allocate scarce resources to maximize your immediate utility. For example, suppose a consumer has total income $Y$, and there are only two goods, with prices $p_1$ and $p_2$. Then, the consumer has to decide how much $(q_1, q_2)$ to consume of both goods so as to maximize his utility $u(q_1, q_2)$ while not going over his budget $Y$. He faces the problem.

$$
q_1^\ast, q_2^\ast = \max_{q_1, q_2} u(q_1, q_2)  \ \ \ \ \text{s.t.} \ \  p_1q_1 + p_2q_2 \le Y. 
$$

A common utility function is [Cobb-Douglas](https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function) which has realistic properties such as negative second derivatives representing diminishing marginal utility. When the consumption problem is solved, one obtains the optimal $q_1^\ast(p_1, p_2, Y)$ as a function of the prices and the income, and the same for $q_2^\ast$. Note that if we trace how $q_1^\ast$ changes as $p_1$ changes, we get the *[demand](https://en.wikipedia.org/wiki/Marshallian_demand_function)* function.

The demand is important because it shows how much units $q$ of a good are demanded at a given price $p$. Likewise, if we invert it, the inverse demand $p_1(q_1^\ast)$ shows the maximum price a consumer is willing to pay (WTP) for an additional unit of the good. To get the aggregate demand of the whole market we simply sum the quantities demanded at every price.


