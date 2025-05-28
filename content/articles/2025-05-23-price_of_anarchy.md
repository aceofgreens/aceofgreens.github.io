---
Title: The Price of Anarchy
Date: 2025-05-23 07:00:00 +0200
Tags: cs, econ, ultra-rationalism
slug: price_of_anarchy
---

When it comes to economic calculation and scarce resource allocation, a capitalist decentralized system of decision-making is more efficient than a socialist centralized one. Why? Because a decentralized system breaks down the larger problem instance - e.g. resource allocation across a whole industry - into multiple smaller instances - allocation within a firm or a household - which are easier to solve. This approach of dividing the problem, solving the subproblems, and combining them, does not provide the best solution, but often is good enough. Here we're interested in quantifying this statement, at least for well-formalized simple problems. We'll build intuition about the behaviour of systems which when let alone evolve according to their selfish participants, and we'll compare them to their best possible outcomes.

### Selfish Routing

**A simple network**. Consider a very simple traffic routing problem where we're given an origin node $o$ and a destination node $d$ and there are only two edges from $o$ to $d$. The first has a constant cost $1$ and the second has a cost of $x$ where $x$ is the proportion of the total flow from $o$ to $d$ that uses that edge. Intuitively, the first path is like a wide and long road to the destination, whereas the second one is a very short but very narrow one, where congestions can happen, depending on how much traffic participants go through it. Drivers are infinitesimally small units of traffic and choose which edge to take in parallel.

**Price of anarchy**. For an individual driver, it is always beneficial to choose the second route, as the cost can be at most $1$. This reasoning represents decentralized decision-making where every driver selfishly makes a decision. Since everybody would choose the second route, all drivers end up with a cost of exactly $1$. Instead, in a centralized manner, an altruistic dictator could minimize the *average* travel time by randomly splitting the traffic equally between the two paths, in which case the average cost is $3/4$. We define the price of anarchy (PoA) as the minimal cost of the selfish setting divided by the minimum cost of the centralized setting. In this example it's $1/(3/4) = 4/3$.

**A nonlinear example**. Now, imagine the cost of the second edge is $x^p$ instead of $x$, with $p > 0$ and $x$ in $[0, 1]$ since it's a proportion. The second edge is still optimal and everyone uses it, leading to a scenario where the average cost is $1$. What can a benevolent dictator do? They can set the proportion $x$ to take the first edge of constant cost to be

$$
\min_x \ [x + (1 - x)(1 - x)^p] \Rightarrow x^\ast = 1 - \left( \frac{1}{p+1} \right)^{1/p}
$$

This sacrifices some drivers to take the long path, so that most other drivers can take the quick path without too much congestion. As $p \rightarrow \infty$ fewer and fewer drivers have to take the slower path and the average time to the destination tends to zero. The PoA here is unbounded in terms of $p$, indicating that the cost of selfish behaviour can become arbitrarily high as the cost of the second edge, depending on $p$, changes. More "nonlinear" costs lead to higher PoA.

**Selfish routing on graphs**. This very simple network with two paths is called a Pigou network. Now, we'll actually show a powerful result relating the PoA in such simple Pigou networks to the PoA of any general selfish routing graph. Suppose we have a graph $G = (V, E)$ along with the tuple $(o, d, r)$ where $r$ is the total traffic that needs to be transported, and a class of cost functions $\mathcal{C}$ which mark the cost functions along the individual edges. On this graph we mark the equilibrium flow $f$, representing selfish behaviour, and the best flow $f^\ast$. 

Some basic mathematical notation: 

1. The flow $f$ represents how much flow, out of $r$, goes through a path $P$ from $o$ to $d$. Naturally, the flow $f$ splits the traffic across all paths, $\sum_{P} f_P = r$.
2. Similarly, we denote $f_e$ as the flow going through a particular edge. It combines all the traffic from all paths that use this edge, $f_e = \sum_{P: e \in P} f_P$.
3. The cost of an edge is $c_e(f_e)$. The cost of a path is $c_P(f) = \sum_{e \in E} c_e (f_e)$.
4. The cost of the entire flow is $C(f) = \sum_{P} f_P c_P(f) = \sum_{e \in E}f_e c_e(f_e)$, where we can either sum the costs across all paths or sum the costs of individual edges.

Now, for the selfish equilibrium flow $f$ we know that each individual takes the optimal, minimum cost path, suppose of cost $L$, given that all other players do the same. Thus, the total cost is $rL$ which is lower or equal than that in the best flow $f^\ast$ with the costs now fixed at $c_e(f_e), \forall e$:

$$
\begin{align}
& \sum_{P} f_P c_P(f) = \sum_{e \in E}f_e c_e(f_e) = rL \\
& \sum_{P} f^\ast_P c_P(f) = \sum_{e \in E}f^\ast_e c_e(f_e) \ge rL \\
\Rightarrow &\sum_{e \in E}(f^\ast_e - f_e) c_e(f_e) \ge 0.
\end{align}
$$

The first line expresses the total cost of the equilibrium flow either by summing over paths, or by edges. The second line shows that when holding the costs "frozen" at their equilibrium values, the "best" flow is not best, which is obvious. Now, here is the connection with the Pigou network.

We will define the Pigou bound $\alpha(\mathcal{C})$, which depends on the family of cost functions $\mathcal{C}$, as the largest PoA over any Pigou network with cost functions in $\mathcal{C}$ and traffic $r$:

$$
\alpha(\mathcal{C}) = \sup_{c \in \mathcal{C}} \sup_{r \ge 0} \sup_{x \ge 0} \left\{ \frac{r c(r)}{xc(x) + (r-x)c(r)}\right\}.
$$

Specifically, $rc(r)$ is the selfish equilibrium cost where everyone attains the full cost $c(r)$ and $x$ is the proportion of the traffic that goes to the "fast" edge which can get congested. Now, we instantiate the righthand side of the Pigou bound for every edge $e$ in our graph. Necessarily, the quantity $\alpha(\mathcal{C})$ is larger than the corresponding calculation where we've substituted $c_e$ for $c$, $f_e$ for $r$, and $f^\ast_e$ for $x$. From this it follows,

$$
\begin{align}
 \alpha(\mathcal{C}) & \ge \frac{f_e c_e(f_e)}{f^\ast_e c_e(f^\ast_e) + (f_e - f^\ast_e) c_e(f_e)} \\
\Rightarrow  \  f^\ast_e c_e(f^\ast_e) & \ge \frac{1}{\alpha(\mathcal{C})} f_e c_e(f_e) + (f_e - f^\ast_e) c_e(f_e) \\
\Rightarrow  \  C(f^\ast) &\ge \frac{1}{\alpha(\mathcal{C})} C(f) + \sum_{e \in E}(f^\ast_e - f_e) c_e(f_e) \ge \frac{C(f)}{\alpha(\mathcal{C})}.
\end{align}
$$

**PoA bound**. Thus the price of anarchy $C(f)/C(f^\ast)$ is at most $\alpha(\mathcal{C})$. And here is the intuition. If the cost function is not *too nonlinear*, it may not be at all too costly to let the traffic evolve according to the selfish behaviour of the participants, instead of sacrificing some of them to the slow paths, so that the average cost could be slower. We can imagine that in real life, for large systems it may be infeasible to obtain the best solution. Implementing it could even require significant coercion over some participants. In that case, letting the selfish equilibrium rule may not be such a bad idea...

### Over-provisioning


**Setting**. Next, we'll change the setting a bit by imagining that each edge acts as a small $M/M/1$ [queueing system](https://en.wikipedia.org/wiki/Queueing_theory). Specifically, the edge has an infinitely long queue that stores incoming traffic, arriving at a Poisson distribution with rate $x$. There is also a single server that processes traffic from the queue with service times given by independent and identically distributed exponential random variables with mean $1/u_e$. The parameter $u_e$ represents the capacity of the edge $e$. Intuitively, if the rate of arrivals $x$ is much smaller than $u_e$, the processing time is essentially zero. However, if $x$ becomes close to $u_e$, the processing time quickly shoots up to $+\infty$. Therefore, the cost function represents the average waiting time for the edge and has the form

$$
\begin{align}
c_e(x) = \begin{cases}
1/(u_e - x) &\text{ if } x < u_e,\\
+\infty &\text{ otherwise}.
\end{cases}
\end{align}$$

We can imagine that the selfish equilibrium flow $f$ will likely reach the capacity of at least some edges, in which case the price of anarchy will be very high. Instead, we can *over-provision* our routing network to prevent this. This means that for an equilibrium flow $f$, for every edge $e$ we have $f_e \le (1 - \beta)u_e$. If we over-provision by $b=10\%$, then the total flow across any of the equilibrium edges must be at most $90\%$ of the capacity of that edge. Again, the PoA in such over-provisioned networks is at most the Pigou bound in similar $\beta$-over-provisioned networks. The ratio comes out to $(1 + \beta^{-1/2})/2$, which tends to $0$ as $\beta \rightarrow 1$. With just $10\%$ over-provisioning, the price of the selfish equilibrium is up to $2.1$ times that of the best one.

**A more general PoA bound**. Now, we'll prove another important result that bounds the PoA of any selfish routing network, with *any* cost function. Specifically, we start with the network $G = (V, E)$, along with the traffic rate $r$, and denote as $f$ and $f^\ast$ the equilibrium flow and the best flow at traffic rates $r$ and $2r$, respectively. A similar calculation as before reveals:

$$
\begin{align}
\sum_{e \in E} f_e c_e(f_e) & = \sum_P f_P c_P(f) = rL \\
\sum_{e \in E} f^\ast_e c_e(f_e) & = \sum_P f^\ast_P c_P(f) \ge 2rL
\end{align}
$$

Next, you can become convinced that $f^\ast_e\big(c_e(f_e) - c_e(f^\ast_e)\big) \le f_e c_e(f_e)$. This holds true if we assume that the cost function $c(\cdot)$ is positive and nondecreasing. When we sum across all edges we get that the best flow $f^\ast$ at traffic $2r$, evaluated with costs fixed at the equilibrium cost at traffic $r$, overestimates the true best cost by at most the cost of $f$: 

$$
\underbrace{\sum_{e \in E} f^\ast_e c_e(f^\ast_e)}_{\text{cost of } f^\ast} \ge \underbrace{\sum_{e \in E} f^\ast_e c_e(f_e)}_{\ge 2rL} - \underbrace{\sum_{e \in E}f_e c_e(f_e)}_{=rL}
$$

The conclusion here is that for any selfish routing network and traffic rate $r>0$, and any cost function, the equilibrium cost is at most the cost of the best flow for that network on double the traffic, $2r$. Pretty neat. Even with crazy complicated cost functions, the selfish equilibrium does not perform arbitrarily worse.

### Atomic Routing

Now, let's consider a different setup, called *atomic* selfish routing. Here there are $k$ agents of non-negligible size and each one has its own origin-destination pair $(o_i, d_i)$. For simplicity we'll assume that each agent routes $1$ unit of traffic along a single path from $o_i$ to $d_i$. Other extensions exist but we'll not bother with them. Naturally, as different agents choose paths with overlapping edges, the costs in those edges starts to increase. If all agents choose paths that go through the same edge, they will all face very large costs, because of that edge. Each agent tries to minimize their cost by choosing the right path to its destination.

In this game the players' actions are the paths they choose to route over. A flow, consisting of all the selected paths, $f = (P_1, ..., P_k)$, is an equilibrium flow if no agent has the incentive to deviate from his path, assuming that other players' paths remain the same. The cost of an equilibrium flow is the sum of all costs for all agents. Note that in atomic selfish routing there could be multiple equilibrium flows with *different* costs. To accommodate for this, we need to change the price of anarchy definition so that it now considers the cost of the *worst* equilibrium flow with respect to the cost of the best flow.

The good news is that another limiting result exists for atomic routing. Specifically, in every atomic selfish routing network with affine cost functions, the price of anarchy is at most $2.5$, i.e. the worst selfish equilibrium is at most $2.5$ times the cost of the best one. Similar bounds can be derived for any polynomial cost for the edges. For non atomic routing, and polynomial cost functions up to degree $p$, the PoA bound is $\Theta(\frac{p}{\log p})$. For atomic routing this relationship is exponential, $\Theta(c^p)$, hence much less efficient.

### Equilibrium Types

Finally, we'll close by exploring different formalisms for equilibria in strategic games. This is important because we need to recognize that not all types of equilibria exist for all games. For example, in this [oligopoly game](https://aceofgreens.github.io/attempts_to_solve_a_market.html), it's likely that a pure Nash equilibrium does not exist, but a mixed one does. Likewise, some types of equilibria are easier to compute than others. It pays off to be able to classify the type of equilibrium we're dealing with.

We consider a non-sequential, i.e. single timestep, cost minimization game with $k$ players. The players' actions $a_1, ..., a_k$ constitute an action profile $\mathbf{a}$. Each player has their own cost function depending  on the entire action profile, $C_1(\mathbf{a}), ..., C_k(\mathbf{a})$, leading to strategic interactions. Note that instead of cost minimization we could easily frame the game as a payoff, utility, or reward maximization one, where we simply consider the negative cost instead.

**Pure Nash equilibrium**. A pure Nash equilibrium (PNE) in a cost-minimization game is an action profile $\mathbf{a}$ such that for every agent and every unilateral deviation $a_i'$ of agent $i$, $C_i(\mathbf{a}) \le C_i(a_i', \mathbf{a}_{-i})$. Thus, in a PNE player $i$ does not have any incentive to change his action if other players don't change their, and the same is valid for them. Here the set of actions of all agents except $i$ is denoted as $\mathbf{a}_{-i}$. The action $a_i$ is a best response given the actions of the other agents, $\mathbf{a}_{-i}$, that is, it minimizes the cost $C_i(a_i', \mathbf{a}_{-i})$ over $a_i'$. Intuitively, this best response function is deterministic - it always returns a deterministic action $a_i$ from inputs $\mathbf{a}_{-i}$. Note that a PNE is interpretable, but difficult to compute and may not always exist.

**Mixed Nash equilibrium**. Nothing prevents each agent to randomize their action - instead of a deterministic action, player $i$ can select a distribution over their actions, $\sigma_i$ and sample an action from that distribution. A mixed Nash equilibrium (MNE) is now a profile of action distributions $\mathbf{\sigma} = (\sigma_1, ..., \sigma_k)$ such that for all agents the *average* cost of any unilateral deviation is not smaller than the average cost at those equilibrium action distributions:

$$
\mathbb{E}_{\mathbf{a} \sim \sigma} \left[ C_i(\mathbf{a}) \right] \le  \mathbb{E}_{\mathbf{a} \sim \sigma} \left[ C_i(a_i', \mathbf{a}_{-i}) \right], \ \ \forall i, \ \ \forall a_i'.
$$

Here $\sigma$ is the product distribution over the action distributions of all agents, $\sigma = \sigma_1 \times \ldots \times \sigma_k$. Players randomize their strategies independently, without any communication. The canonical example here is rock-paper-scissors. The best one can do is to play uniformly random independently of the other player, which is the mixed equilibrium. In terms of theory, a MNE exists always for games with finite players, actions, and outcomes, but is intractable to compute. It is related to the [PPAD](https://en.wikipedia.org/wiki/PPAD_(complexity)) complexity class.


**Correlated equilibrium**. This is a bit complicated to understand. A correlated equilibrium (CE) is a distribution $\sigma$ over action profiles $\mathbf{a}$ such that after $\mathbf{a}$ is drawn, for player $i$, conditioned on seeing $a_i$, there is no incentive to play any other action apart from $a_i$, given that others also play according to their profile $\mathbf{a}_{-i}$,

$$
\mathbb{E}_{\mathbf{a} \sim \sigma} \left[ C_i(\mathbf{a}) | a_i \right] \le \mathbb{E}_{\mathbf{a} \sim \sigma} \left[ C_i(a'_i, \mathbf{a}_{-i}) | a_i \right], \ \ \forall i, \ \ \forall a_i'.
$$

Okay, let's unpack. There is some, say, trusted external *device* that produces action tuples according to a possibly correlated distribution $\sigma$. These actions can be considered *suggested* by the device. In a CE each player observes its own suggested action and acts according to it. Everyone sticks to those suggested actions. A canonical example for a correlated equilibrium is two vehicles on opposite sides of a traffic light. The traffic light is the device producing suggestions $(\text{go}, \text{stop})$ or $(\text{stop}, \text{go})$ which are correlated - whenever the light is green for one player, it's red for the other. Each player observes the signal meant for themself, e.g. $\text{go}$, and knows that the signal for the other agent is likely $\text{stop}$. Following these suggested actions is in the best interest of all players and nobody has any incentive to deviate. A CE usually attains much better outcomes than a MNE. It always exists and is easy to compute.


**Coarse correlated equilibrium**. A distribution over strategies $\sigma$ is a coarse-correlated equilibrium (CCE) if for every agent $i$ and every unilateral deviation $s_i'$ we have:

$$
\mathbb{E}_{\mathbf{s} \sim \sigma} [C_i(\mathbf{a})] \le \mathbb{E}_{\mathbf{a} \sim \sigma} [C_i(a_i', \mathbf{a}_{-i})], \ \ \forall i, \ \ \forall a_i'.
$$

Here $\sigma$ doesn't have to be a product distribution, as in a MNE. The actions in it can be correlated, and player $i$ does not see the realization $a_i$. It's like knowing that the traffic light shows either $(\text{go}, \text{stop})$ or $(\text{stop}, \text{go})$ but not seeing what your own current light is. In that sense, $\text{go}$ is the best action only on average, when the other players select $\text{stop}$. Likewise, stopping is the best action on average when the other agents have decided to go. This is the most general type of equilibrium. It always exists and is easy to compute.

**Dynamics**. The broader class of CCEs are important because they arise as the convergence action profiles under what's called *no-regret* dynamics. In no-regret dynamics, each player adjusts their actions so that the long-run average payoff is at least as good as the best fixed action in hindsight. In other words, you play that action which minimizes long-run regret, not necessarily the best immediate payoff (associated with best-response dynamics). Under no-regret dynamics, agents converge to a CCE, even in games in which a pure NE does not exist.



