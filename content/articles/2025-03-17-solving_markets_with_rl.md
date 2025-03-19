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
q_1^\ast, q_2^\ast = \text{arg}\max_{q_1, q_2} u(q_1, q_2)  \ \ \ \ \text{s.t.} \ \  p_1q_1 + p_2q_2 \le Y. 
$$

A common utility function is [Cobb-Douglas](https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function) which has realistic properties such as negative second derivatives representing diminishing marginal utility. When the consumption problem is solved, one obtains the optimal $q_1^\ast(p_1, p_2, Y)$ as a function of the prices and the income, and the same for $q_2^\ast$. Note that if we trace how $q_1^\ast$ changes as $p_1$ changes, we get the *[demand](https://en.wikipedia.org/wiki/Marshallian_demand_function)* function.

The demand is important because it shows how many units $q$ of a good are demanded at a given price $p$. Likewise, if we invert it, the inverse demand $p_1(q_1^\ast)$ shows the maximum price a consumer is willing to pay (WTP) for an additional unit of the good. To get the aggregate demand of the whole market we simply sum the quantities demanded at every price.

**Production**. On the other side of the consumers are producers that supply products. Producers have a production function $q = f(L, K)$ where $L$ and $K$ represent the labour and capital inputs, respectively. Different combinations of inputs produce different quantities $q$ of the product. Additionally, there are factor cost associated with $K$ and $L$ - wages $w$ and rent $r$, respectively. Thus, the cost of producing at $(L, K)$ is given by $C(L, K) = wL + rK$, where we assume factor prices $w$ and $r$ are constant.

Producers face two important [dual](https://en.wikipedia.org/wiki/Duality_(optimization)) problems. They can either minimize cost given fixed $q$, or maximize $q$ given fixed cost. Consumers also have a dual problem similar to the one described above, which minimizes the expenditure given a constant utility. For the producers, the primal (on which we'll focus here) is the cost minimization problem: determine the inputs $(L, K)$ at which producing exactly $q$ units yields minimum cost:

$$
L^\ast, K^\ast = \text{arg}\min_{L, K} wL + rK \ \ \ \ \text{s.t.} \ \ f(K, L) = \bar{q}.
$$

Evaluating the cost at $(L^\ast, K^\ast)$ yields the minimum cost $C(q)$ needed to produce $q$ units, which depends on $q$, $r$, and $k$. Now what remains is to determine the value produced $q$.

**Perfect competition**. In perfect competition, which is an idealized market model, firms are price takers. They maximize profit $\pi$ by setting the quantity $q$ so that 

$$
q^\ast = \text{arg}\max_{q} \pi = p q - C(q) \ \ \Rightarrow \ \ q^\ast = \left\{q \ | \ p = \frac{dC(q)}{dq}\right\}.
$$

Thus, each firm sets the quantity to that point where its marginal cost $dC(q)/dq$ is equal to the constant market price $p$. Let's motivate this result a bit. What does it mean for a firm is a price taker? It means that it cannot influence the price. Whatever quantity it sets, the price is constant. Тhe demand is horizontal at the market price $p$ and firms can sell as much as they want at that price. For that reason, if they produce a quantity $q$, their revenue will be $pq$. If a firm sets the price higher than $p$, it will sell zero. If it sets it below $p$, it will sell as much as it will sell if the price is $p$.

To derive the supply curve one can trace how the selected quantity $q^\ast$ depends on the price $p$. Hence, the supply is given by $q_s = [dC(q)/dq]^{-1}(p)$, and only whenever $p$ is greater than the average cost curve (otherwise, it's more profitable to shut down). The total supply is given by the sum of all quantities supplied by the individual firms. Markets clear because however much is produced, is also bought. There are other complications which we'll skip.

**Monopoly**. A monopolist is a price setter - he is able to set any price $p$ he wants. If he sets a price $p$, the market demand is $Q_d(p)$ so that's how many sells he can get. Thus, he will produce exactly that many in terms of quantity $q$. The problem becomes

$$
\begin{align}
&p^\ast = \text{arg}\max_{p} \pi = p Q_d(p) - C\big(Q_d(p)\big)\\
&\Rightarrow \ Q_d(p) + \frac{dQ_d(p)}{dp} p  = \frac{dC\big(Q_d(p)\big)}{dQ_d(p)}\frac{dQ_d(p)}{dp} \Rightarrow \frac{p - dC(q)/dq}{p} = \frac{1}{|\epsilon|}.
\end{align}
$$

The last line shows the profit maximizing equation where marginal revenue equals marginal cost. Further reshuffling yields the [Lerner index](https://en.wikipedia.org/wiki/Lerner_index), a useful formula showing that the monopolist sets the price above the marginal cost and the markup is inversely proportional to the demand elasticity. 

Note the hidden assumption of perfect information. The monopolist needs to perfectly know the demand $Q_d(p)$ at price $p$, so he can produce exactly that much in terms of quantity, $q_s = Q_d(p)$. This makes the market clear. If we remove that assumption then the monopolist has to set the quantity supplied $q_s$ separately - a situation in which he may end up with not enough production or with leftover inventory:

$$
p^\ast, q_s^\ast = \text{arg}\max_{p, q_s} \pi = p \min\{Q_d(p), q_s \} - C(q_s).
$$

This is a more general setting which allows for rationing. If $q_s > q_d(p)$, then the monopoly will produce more than the market demands. If $q_s < q_d(p)$ then the monopolist reduces the number of transactions below the desired ones. Note also that there is no clearly defined supply function here. There is only a supply *point* since the monopolist sets both the price and the quantity.

### Problem Setting
Let's move to more realistic settings involving market friction. This is any factor that introduces transaction fees, product search, price dispersion, buyer-seller matching, or a myriad other phenomena. In our case instead of assuming that buyers and sellers are matched instantaneously, we'll build a very simple [order book](https://en.wikipedia.org/wiki/Order_book) inspired from the workings of stock market exchanges.

So, consider a market where there are $N$ firms and $M$ consumers. Each of the consumers has a downward sloping linear demand function, whose precise parameters are chosen randomly. Trading happens day by day. Firm $i$ sets its price $p^i$ and quantity $q_s^i$ for each day. The quantity $q_s^i$ becomes the available inventory for that firm to sell during the day. We simulate a trading day by iterating over $K$ transaction opportunities. Within each iteration a random buyer is selected. Then, we filter the firms by considering only those firms that have positive inventory (have something to sell), and whose set price is lower than the willingness to pay (WTP) of that buyer, evaluated at their prices. Then, out of all remaining firms the buyer chooses the one with the lowest price. If the buyer will not go over his average (across the prices) quantity demanded by buying one more unit, a transaction happens. We decrease the inventory of that firm by 1, increase its sales by 1, and increase the quantity bought by that buyer by 1. The trading day halts earlier if all sellers have empty inventories or if their prices are above any of the WTPs of the consumers.

After the $K$ iterations, the firms have accumulated their sales $n^i$ and can calculate profits simply as $n^i p^i - C(q_s^i)$. We assume firms have linearly increasing costs $C^i(q) = c^iq$. Thus, they have constant marginal costs but at different levels $c^i$.

This is how we'll model the market process. At the end of each day it provides the number of sales $n^i$ for each firm. The function $n^i(p^i, \mathbf{p}^{-i}, q^i, \mathbf{q}^{-i})$ depends on all prices and quantities and is discrete in values. It is also random and not differentiable. The problem of the firm $i$ is

$$
p^\ast, q_s^\ast = \text{arg}\max_{p^i, q_s^i} \pi = n^i(p^i, \mathbf{p}^{-i}, q_s^i, \mathbf{q}_s^{-i}) p^i - C(q_s^i), \ \ \forall i \in \{1, .., N \}.
$$

What does it mean to solve the market in this case? This objective has to be solved for all firms simultaneously. But since the $N$ firms are sharing (partitioning) the market through their sales, this becomes a strategic game involving different interactions. A transaction for one firm is a lost transaction for another firm. Thus, we're in the area of [multiobjective optimization](https://en.wikipedia.org/wiki/Multi-objective_optimization), where each firm has its own objective.

What does the solution look like? Generally, one object of interest is the [Pareto frontier](https://en.wikipedia.org/wiki/Pareto_front) which contains all the price-quantity tuples that are non-dominated. A setting $(p^i, q_s^i)$ is non-dominated if firm $i$ cannot increase its profit $\pi^i$ without hurting the profit of another firm... Yet, this is not what we want. In our case firms will gladly increase their profits at the expense of other firms. We're actually looking for a Nash equilibrium. It represents a point $(p^1, q_s^1, ..., p^N, q_s^N)$ such that the profit $\pi^i$ of firm $i$ is maximal with respect to $(p^i, q_s^i)$ if all other firms set their price-quantities precisely to $(\mathbf{p}^{-i}, \mathbf{q}_s^{-i})$. The same is simultaneously valid for them. A maximal profit in this case means that you don't have incentives to deviate. Thus, the Nash equilibrium represents a point of convergence from which no firm has any incentive to deviate. It is a [fixed point](https://en.wikipedia.org/wiki/Fixed_point_(mathematics)) with respect to the dynamics of the system.

Proving whether a Nash equilibrium exists and whether it's unique is tricky. There are various [theorems](https://en.wikipedia.org/wiki/Kakutani_fixed-point_theorem). Let's avoid this question altogether. Assuming it exists, the way to find it is by first computing a best-response function for each player. It simply returns the best action for each player, assuming a given set of other actions for the other players. In our setting for player $i$ it is $\text{BR}(\mathbf{p}^{-i}, \mathbf{q}^{-i}, c^i) = \text{arg}\max_{p, q_s} \pi^i(p, \mathbf{p}^{-i}, q_s, \mathbf{q}_s^{-i}) = (p^\ast, q_s^\ast)$. It computes the best price-quantity for firm $i$ given that the other price-quantities are $(\mathbf{p}^{-i}, \mathbf{q}_s^{-i})$. Once we have all BR functions we need to find their intersection which is the Nash equilibrium. This can be done through an iterative approach where we start from a random set of price-quantities and we evolve them according to the BRs until they converge.

### Multi-Agent Policy Gradients
