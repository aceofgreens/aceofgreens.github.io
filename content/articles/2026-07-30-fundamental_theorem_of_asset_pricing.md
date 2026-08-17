---
Title: The Fundamental Theorem of Asset Pricing
Date: 2026-07-30 07:00:00 +0200
Tags: econ
slug: fundamental_theorem_of_asset_pricing
status:
---

<!-- Suppose someone offers you a contract that pays you an uncertain amount of money in one year. What should you pay for it today? Whatever number you write down has your own attitude toward risk baked into it, because you are not indifferent between a sure dollar and a risky one. Ask everyone the same question and their answers aggregate into demand, which meets supply and produces a price - so the prices we observe are not statements about odds either, but numbers stuffed full of the risk attitudes of everyone who traded. Can we untangle them? Remarkably, yes: under one very weak assumption - that the market does not offer free money - all of that risk aversion can be absorbed into a distortion of the probabilities themselves, so that a price is just an expected payoff, discounted, under a *fictitious* measure. Pricing a risk attitude means turning it into a reweighting of the states of the world. This equivalence is the fundamental theorem of asset pricing (FTAP), it is the reason most of modern derivative pricing reduces to computing an expectation, and it is one of the deepest and most beautiful ideas in the subject. -->

What makes an uncertain promise worth something today? Is a price a forecast of the future, a measure of collective optimism, or an expression of how much we fear bad outcomes? Financial markets seem to bundle all of these forces into a single number. The fundamental theorem of asset pricing shows that, beneath that complexity, prices must obey a remarkably simple logic: consistent prices leave no room for a free lunch.

**The setting**. We'll illustrate the point through an absurdly simplified example. A stock trades at $S = 100$ today and, in one year, will be worth either $S_u = 120$ or $S_d = 80$. Only these two outcomes are possible and we don't know with what probability each one will occur. In addition, the risk-free rate is $r = 5\%$. It represents the return that a *riskless* asset can obtain. Finally, there's a call option with strike $K=100$ on the stock. The question: how much is it worth? 

<figure>
    <img class="theme-swap small_img"
        src="/images/simplest_call_light.svg"
        data-light="/images/simplest_call_light.svg"
        data-dark="/images/simplest_call_dark.svg"
        alt="DFA"
        style="display: block; margin: 0 auto;"
    >
  <figcaption>Fig. 1. A simple setting of a stock and a call option. The stock can go up or down with probability $p$ and $1-p$ respectively. The payoffs of the call option in both states are known. </figcaption>
</figure>

<script>
(function () {
  const sheet = document.getElementById('theme-stylesheet');
  if (!sheet) return;

  const apply = () => {
    const dark = /\/dark\.css(\?|$)/.test(sheet.href);
    document.querySelectorAll('img.theme-swap').forEach(img => {
      const next = dark ? img.dataset.dark : img.dataset.light;
      if (img.getAttribute('src') !== next) img.setAttribute('src', next);
    });
  };

  apply(); // on load
  new MutationObserver(apply).observe(sheet, { attributes: true, attributeFilter: ['href'] });
})();
</script>

**The nature of $p$**. In reality $p$ is the probability distribution over the stock's future. No one knows it. We neither know $p$, nor all the factors that might determine it. We're dealing with unknown unknowns. For all purposes, the future is [epistemically uncertain](https://en.wikipedia.org/wiki/Knightian_uncertainty). To get a sense of where it comes from we can try to trace the dependencies in reverse. The price of a stock changes whenever somebody decides to buy at the last market price, or whenever people readjust their limit orders and a stock exchange opens the floor for trading. One step backward, people adjust their orders because they update their expectations about whether it would be profitable to do so. One step back this happens for example because:

- Global macroeconomic factors shift, or industrial shocks, scientific breakthroughs, regional wars or any political event happens. This is already hard enough to predict.
- Expectations about future earnings or the future price change. This is where bubbles, feedback loops, fads, and public manias live. 
- People's risk-preferences change. A person who is very risk-averse could be unwilling to hold an asset, even if it's clear that its mean return is much greater than the risk-free return.

Every investor has an individual demand for the stock, which is based on his unique risk tolerance and willingness to endure uncertainty. From the aggregation of all individual demands one obtains the market demand for the stock, which also aggregates the bidders' individual risk-preferences. Hence, if people become more risk-averse, the price drops and the probability of the stock price increasing to a given level decreases (or so it is convenient to believe). The point is that **the probability $p$ is the real-world probability, which aggregates incredibly complicated causal dependencies based on expectations and individuals' risk-profiles**. It is hubris to believe we know it.

Hence, in our simple setup the combination of $p$ and the future values $S_u=120$ and $S_d=80$ implicitly contain information about the *static* real-life earnings expectations, risk-preferences, economic outlooks and so on.

**Arbitrage**. If we can't know $p$, how do we determine the worth of the call option? Luckily, there is a way, by holding the right amount of cash (or equivalently a risk-free bond) and the underlying stock, such that this portfolio perfectly replicates the payoff of the call option. From the standard option formula $\max{S-K, 0}$, we know that in the up-state it is worth $C_u = 20$ and in the down-state $C_d = 0$. Now, let's consider that we hold $b$ units of a riskless cash bond and $s$ units of the stock. We want to find the value $(s, b)$ that obtains the same payoff.
$$
\begin{bmatrix}
S_u & 1+r \\
S_d & 1+r \\
\end{bmatrix}
\begin{bmatrix}
s \\
b
\end{bmatrix}
=
\begin{bmatrix}
C_u \\
C_d
\end{bmatrix}
\ \ \Rightarrow \ \ 
\begin{cases} 
120s + 1.05b = 20 \\
80s + 1.05b = 0
\end{cases}
\ \ \Rightarrow \ \
\begin{bmatrix}
s \\
b
\end{bmatrix}
\approx
\begin{bmatrix}
0.5 \\
-38.095
\end{bmatrix}
$$

With this exact combination of holding half a unit of stock and borrowing $38.095$, in the good state we get exactly $20$, and in the bad state exactly $0$, replicating the payoff of the call option. What is the cost of entering this replication strategy? Borrow $38.095$ and use $11.905$ of your own money to buy half a unit of the stock. At the end it's worth either $60$ or $40$, and after repaying $40$, you end up with either $20$ or $0$. The cost of this is $50 - 38.095 = 11.905$. Call this number $V$.

Consider what happens if the call option is cheaper. If $C < V$, you'd want to buy the call and short the cash-stock combination. So you first borrow half a share, sell it for $50$ and lend out $38.095$. This leaves you with $V=11.905$. With this, buy the call option. At the end of the period, you receive $40$ from the loan and $20$ or $0$ from the call option. This is enough to buy back the stock and return it to its original owner to complete the short. You just pocketed $V - C$ without incurring any risk.

A similar arbitrage argument holds when $C > V$. The point is that one needs $C=V$ in order to avoid eternal riskless profit. So that's our valuation mechanism: **the value of the call has to be the cost of replication in terms of the underlying stock and a risk-free asset**.

**Implications**. No-free-lunch describes the peculiar nature of the world we live in. A contradiction between prices is also an invitation. In that sense, market efficiency is a restless, decentralized process of error-correction (see also [Fama's efficient-markets formulation](https://doi.org/10.1111/j.1540-6261.1970.tb00518.x)). Its order depends on people willing and able to search for discrepancies, bear execution and funding risk, and enforce contracts. And this process is never perfect. If it was perfect, and prices already contained all available knowledge, nobody would pay to discover or verify facts in the first place. Hedge funds would not be profitable, whereas in the real world they are, precisely because they have a social utility in harvesting the arbitrage opportunities and keeping markets close to perfect efficiency. So a perfectly efficient market is [considered impossible](https://www.aeaweb.org/aer/top20/70.3.393-408.pdf). Errors may exist, but the errors large and accessible enough to finance their own correction tend not to survive.

There is broader similarity to other systems here. The closest physical analogue is thermodynamic equilibrium, especially when expressed in terms of free-energy gradients or chemical potentials, and [detailed balance](https://en.wikipedia.org/wiki/Detailed_balance). A difference in an intensive quantity creates an opportunity for a flow; the flow exploits that difference and, in doing so, tends to destroy it. Of course, systems can remain in long-term disequilibrium when outside forces continually supply energy or impose constraints. A good example are states, which can distort prices and lead the system into *unnatural* behavior.

**Risk-neutral pricing**. Consider that in all the valuation calculations we didn't use $p$. The arbitrage logic doesn't need to know the real distribution $p$! Now let's see another trick. We'll find another probability $q$, such that the expected stock payoff is equal to the risk-free return. We solve

$$
q S_u + (1-q)S_d = S(1+r) \ \ \Rightarrow \ \ q = \frac{S(1+r) - S_d}{S_u - S_d} = 0.625.
$$

Hence, if the probability of the up-state were $0.625$, then the stock would be on average $\mathbb{E}_q[S] = qS_u + (1-q)S_d = 105 = S(1+r)$ and the call option would pay out $\mathbb{E}_q[C] = qC_u + (1-q)C_d = 12.5$. The discounted price is then $C = 12.5/1.05 = 11.905$, the exact value we got from the no-arbitrage argument! This is nice because we obtained the same valuation but again without knowing the real probability $p$.

Let's unpack. $q$ is chosen so the stock earns the risk-free rate *in expectation*. Then, for the option, discounting its expected payoff under $q$ yields the same price enforced by no-arbitrage. The distribution $(\text{up} \mapsto q, \ \ \text{down} \mapsto 1-q)$ is called *risk-neutral* because, under it, investors behave as though they require no extra expected return for bearing risk. Note that real investors are not indifferent to risk. And $q$ does not forecast what will happen! It is only a set-up of mathematical probabilities at which current prices are *consistent*. This means that no one can earn above the risk-free rate on average.

**Implied volatility**. If we assume there's close to no arbitrage in the market, then the observed market price would equal the true valuation $V_0$. In turn, this implies a distribution $q$. In that sense, one can say "the market prices a 62.5% chance of the up-state". For a more realistic setting, consider the [Black-Scholes](https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model) model with observed market price $11.905$ and $K=100$, $S=100$, $r=5\%$. In that case the volatility which produces the observed price, called *implied volatility*, is $\sigma_{\mathrm{imp}} \approx 24\%$. Obviously, Black-Scholes is wrong as a literal model of prices: returns jump, volatility moves, and their distribution has skew and fat tails. So the implied volatility is not the market's forecast of the actual variance. Yet, it is still useful precisely because it is a common coordinate: mapping every option price into the model's variance rate lets us compare the variances that prices imply, without mistaking the coordinate system for reality.

**Incompleteness**. Let's consider also the case with three states: up $S_u = 120$, middle $S_m = 100$ and down $S_d = 80$. As before, we have $S=100$, risk-free rate $r=5%$, strike price $K=100$, which implies $C_u = 20$, $C_m = 0$ and $C_d = 0$. In this case the risk-neutral probability measure is a triple $(q_u, \ \ q_m, \ \ q_d)$. Upon trying to solve 

$$
\begin{cases}
120 q_u + 100 q_m + 80 q_d = 105 \\
q_u + q_m + q_d = 1
\end{cases}
$$

one obtains infinitely many risk-neutral measures, parameterized for example as $(0.625-q_m/2, \ \ q_m, \ \ 0.375 - q_m/2)$ with the domain $q_m \in [0, 0.75]$. As a consequence, the call option price can range anywhere from $4.76$ to $11.905$. This quickly shows that in an *incomplete* market (one in which there are fewer tradeable assets than number of possible future states), the no-arbitrage condition no longer selects a unique price for every payable claim: it only identifies a range consistent with the traded assets, while it is preferences, supply, and demand that determine where within that range the option trades.

**FTAP**. What we've observed numerically is the [Fundamental Theorem of Asset Pricing](https://en.wikipedia.org/wiki/Fundamental_theorem_of_asset_pricing) (FTAP). Suppose one can trade a collection of assets today and receive their uncertain payoffs, governed by $\mathbb{P}$ in the future. The FTAP says that this market contains no arbitrage if and only if there is a *suitable* risk-neutral probability measure $\mathbb{Q}$, under which the discounted price of every traded asset equals its expected future payoff. Further, every contingent claim has one and only one price implied by the traded assets if and only if the measure $\mathbb{Q}$ is unique. Equivalently, **every claim can be replicated by a portfolio of the available assets. Existence of the measure rules out a free lunch, while its uniqueness tells us whether no-arbitrage alone pins down a price.**

For a claim with payoff $X_T$ at a future date $T$, the general pricing formula at any earlier time $t$ is

$$
V_t = B_t\,\mathbb{E}_{\mathbb{Q}}\!\left[\left.{B^{-1}_T} X_T \,\right|\mathcal{F}_t\right].
$$

Here $B_t$ is the value of the risk-free money-market account and $\mathcal{F}_t$ is a [filtration](https://en.wikipedia.org/wiki/Filtration_(probability_theory)) that represents the information available at time $t$. Thus the price is the conditional expectation, under the risk-neutral measure $\mathbb{Q}$, not $\mathbb{P}$, of the payoff discounted back to time $t$. If the risk-free rate is constant at $r$, then $B_T/B_t = e^{r(T-t)}$, so the formula becomes $V_t = e^{-r(T-t)}\mathbb{E}_{\mathbb{Q}}[X_T \mid \mathcal{F}_t]$. More precisely, it is the *discounted price process* $B_t^{-1}V_t$ that is a [martingale](https://en.wikipedia.org/wiki/Martingale_(probability_theory)) under $\mathbb{Q}$: for $t \leq T$,

$$
\mathbb{E}_{\mathbb{Q}}\!\left[\left.\frac{V_T}{B_T}\,\right|\mathcal{F}_t\right] = \frac{V_t}{B_t}.
$$

Since $V_T = X_T$, this is exactly the pricing formula above. The undiscounted price process need not be a martingale, because the risk-free account grows over time; risk-neutral valuation makes discounted prices fair, not raw prices trendless.

**Stochastic discount factors**. We have so far deliberately avoided the real-world probability $p$. To see where risk preferences enter, imagine an investor who consumes $c_0$ today and will consume either $c_u$ or $c_d$ next year. Their expected utility $\mathbb{E}_p[u(c)]$ is

$$
\mathbb{E}_p[u(c)] = u(c_0) + \beta\big[p\,u(c_u) + (1-p)\,u(c_d)\big],
$$

where $u$ captures the diminishing usefulness of additional consumption and $\beta$ captures impatience. Now offer this investor a tiny amount $\varepsilon$ of a claim $X$: it costs $\varepsilon X_0$ today and pays $\varepsilon X_u$ or $\varepsilon X_d$ next year. At a price they are willing to trade, the gain and loss in utility must balance at the margin:

$$
\begin{aligned}
\mathbb{E}_p[u(c + \epsilon X)] &= u(c_0 - \epsilon X_0) + \beta\big[p\,u(c_u + \epsilon X_u) + (1 - p)\,u(c_d + \epsilon X_d)\big], \\
\Rightarrow \ \ \frac{\partial \mathbb{E}_p[u(c + \epsilon X)]}{\partial \epsilon} &= -X_0 u'(c_0 - \epsilon X_0) + \beta \big[p\,u'(c_u + \epsilon X_u)X_u + (1-p)\,u'(c_d + \epsilon X_d)X_d \big] \\
\Rightarrow \ \ 0 &= -u'(c_0)X_0 + \beta\big[p\,u'(c_u)X_u + (1-p)\,u'(c_d)X_d\big] \text{ as } \epsilon \rightarrow 0.
\end{aligned}
$$

Rearranging gives the pricing equation

$$
X_0 = \mathbb{E}_p[mX], \qquad m_s = \beta\frac{u'(c_s)}{u'(c_0)}, \quad s\in\{u,d\}.
$$

The random variable $m$ is called a *stochastic discount factor*. It is the rate at which the investor exchanges consumption in each future state for consumption today. It is high in a state where future consumption is scarce and an extra dollar is especially useful. In a market with many investors, the logic is the same: prices reflect the marginal value of money in each state. So we see that valuation depends on both the real probability $p$ and the subjective psychological preferences $m_s$ in each possible future state $s$. 

This also reveals the connection to the previous paragraphs. The bond, which pays $1.05$ in either state, satisfies $1 = \mathbb{E}_p[1.05m] = 1.05p\,m_u + 1.05 (1-p)\, m_d$. We can recognize a probability distribution $q$ where $q_s = 1.05p_s m_s$. They sum to one precisely because the bond is priced correctly. Substituting them back into the SDF equation gives

$$
X_0 = \frac{1}{1.05}\big[qX_u + (1-q)X_d\big] = \frac{1}{1.05}\mathbb{E}_q[X].
$$

So $q$ is the real-world distribution $p$, tilted toward states in which money matters more. This is why $q$ is not a forecast: it is what remains after risk preferences have been folded into the probabilities. Claims that pay in bad states are valuable insurance and therefore expensive; claims that pay chiefly in good states must offer a higher average return under $p$ to persuade people to hold them. Replication reaches the same prices without ever estimating $p$, $u$, or $m$ because it exploits only the price consistency that those underlying forces produce.

**Relationship with CAPM**. The famous CAPM is a quick consequence. For any asset with gross return $R_i$, the SDF equation gives $1 = \mathbb{E}_p[mR_i]$; for the risk-free asset, $1 = \mathbb{E}_p[m]R_f$. Therefore

$$
\mathbb{E}_p[R_i] - R_f = -\frac{\operatorname{Cov}_p(m,R_i)}{\mathbb{E}_p[m]}.
$$

If the SDF is linear in the market return, $m=a-bR_M$ with $b>0$, one gets:

$$
\mathbb{E}_p[R_i] - R_f
= -\frac{\operatorname{Cov}_p(a-bR_M,R_i)}{\mathbb{E}_p[m]} 
= \frac{b}{\mathbb{E}_p[m]}\operatorname{Cov}_p(R_i,R_M).
$$

The unknown factor $b/\mathbb{E}_p[m]$ is the same for every asset. Set $i=M$ in the preceding equation to determine it from the market itself:

$$
\mathbb{E}_p[R_M]-R_f
= \frac{b}{\mathbb{E}_p[m]}\operatorname{Var}_p(R_M)
\quad\Rightarrow\quad
\frac{b}{\mathbb{E}_p[m]}
= \frac{\mathbb{E}_p[R_M]-R_f}{\operatorname{Var}_p(R_M)}.
$$

Putting that expression back into the return equation gives

$$
\mathbb{E}_p[R_i] - R_f
= \underbrace{\frac{\operatorname{Cov}_p(R_i,R_M)}{\operatorname{Var}_p(R_M)}}_{\beta_i}
  \bigl(\mathbb{E}_p[R_M]-R_f\bigr).
$$

Only the part of a return that moves with the market earns a premium. That is, only systematic risk is what should get compensated. That is the CAPM's familiar $\beta$. In this way, we see how the need for risk premiums automatically arises out of the individual's risk preferences.

**Conclusion**. What should a claim with an uncertain future payoff cost today? In an arbitrage-free market, its price is constrained by the prices of other traded payoffs. Risk preferences still matter, because a dollar received in a bad state is worth more than a dollar received in a good one; the stochastic discount factor records that difference. Risk-neutral probabilities package those state-dependent values into a convenient pricing rule, rather than describing anyone's literal forecast of the future.


<!-- ### More technical version of the article -->

<!-- Where, then, did actual people and their risk profiles go? Their beliefs, wealth, and dislike of risk determine how much stock, bonds, and claims they wish to hold at each price: their demand curves. Together with supply, those demands determine the observed prices of the stock and bond in the first place. But once those prices are observed in this complete two-state market, competition and arbitrage pin down the call price without asking whose utility function is correct. The risk-neutral probabilities are simply the physical probabilities tilted by the price people put on wealth in each state: if the real up probability is $p$, then $q_{u}/p = (1.05)m_{u}$ and $q_{d}/(1-p) = (1.05)m_{d}$, where $m$ is the stochastic discount factor. Thus $\mathbb{Q}$ is not a rival account of people's beliefs. It is a compact way of carrying their aggregate valuation of risk into prices.

### The One-Period Market

We start with the simplest possible model, which already contains the whole theorem. Time has two dates, $0$ (today) and $1$ (tomorrow). Uncertainty is described by a finite set of states $\Omega = \{\omega_1, \dots, \omega_K\}$, exactly one of which will be realized. The real-world, or *physical*, probabilities are $p_k = \mathbb{P}(\omega_k) > 0$; we assume every state has positive probability, otherwise we should have deleted it from $\Omega$.

There are $N$ traded assets. Asset $i$ costs $S_i$ today and pays $D_{ik}$ tomorrow if state $\omega_k$ occurs. So we have a price vector $\mathbf{S} \in \mathbb{R}^N$ and a payoff matrix $\mathbf{D} \in \mathbb{R}^{N \times K}$. A portfolio is a vector of holdings $\mathbf{\theta} \in \mathbb{R}^N$, with negative entries meaning short positions. Its cost today is $\mathbf{\theta}^T \mathbf{S}$, a scalar, and its payoff tomorrow is $\mathbf{D}^T \mathbf{\theta} \in \mathbb{R}^K$, one number per state. Note the linearity: the payoff of a sum of positions is the sum of the payoffs. This is not a modeling assumption so much as an accounting identity, and it is the engine of everything below.

That's the entire market. No utility functions, no equilibrium, no dynamics. The only structure is a linear map from portfolios to state-contingent payoffs, plus a price for each column of the map.

### Arbitrage

An *arbitrage* is a portfolio that gives you something for nothing. Formally, $\mathbf{\theta}$ is an arbitrage if

$$
\mathbf{\theta}^T \mathbf{S} \le 0, \quad \mathbf{D}^T \mathbf{\theta} \ge 0, \quad (\mathbf{\theta}^T \mathbf{S}, \ \mathbf{D}^T \mathbf{\theta}) \ne \mathbf{0},
$$

where the vector inequality is componentwise. There are two flavors of this. In the first, the portfolio has strictly negative cost - you are paid to enter it - and never loses money tomorrow. In the second, it is free today and pays a non-negative amount in every state, strictly positive in at least one. Both are money pumps. It is convenient to bundle cost and payoff together into a single vector in $\mathbb{R}^{1 + K}$,

$$
\Phi(\mathbf{\theta}) = \big(-\mathbf{\theta}^T \mathbf{S}, \ \mathbf{D}^T\mathbf{\theta} \big) \in \mathbb{R}^{1+K},
$$

whose first coordinate is money received today and whose remaining coordinates are money received tomorrow in each state. The set $M = \{ \Phi(\mathbf{\theta}) : \mathbf{\theta} \in \mathbb{R}^N \}$ is a linear subspace of $\mathbb{R}^{1+K}$, since $\Phi$ is linear and short-selling is unrestricted. And the arbitrage condition becomes a statement of pure geometry:

$$
\text{no arbitrage} \iff M \cap \mathbb{R}^{1+K}_+ = \{\mathbf{0}\}.
$$

The market is arbitrage-free precisely when the subspace of attainable cash-flow patterns touches the non-negative cone only at the origin. Everything else is a consequence of this picture.

### State Prices

Two convex sets that meet only at a point can be separated by a hyperplane. Take the simplex $\Delta = \{ \mathbf{x} \in \mathbb{R}^{1+K}_+ : \sum_j x_j = 1 \}$, which is compact and convex, and under no arbitrage is disjoint from the closed subspace $M$. By the [separating hyperplane theorem](https://en.wikipedia.org/wiki/Hyperplane_separation_theorem) there is a $\mathbf{\lambda} \in \mathbb{R}^{1+K}$ and a constant $c$ with $\mathbf{\lambda}^T \mathbf{x} > c$ on $\Delta$ and $\mathbf{\lambda}^T \mathbf{m} < c$ on $M$. But $M$ is a subspace: if $\mathbf{\lambda}^T \mathbf{m} \ne 0$ for some $\mathbf{m} \in M$, we can scale $\mathbf{m}$ to make the inner product arbitrarily large, contradicting the bound. Hence $\mathbf{\lambda}^T \mathbf{m} = 0$ for all $\mathbf{m} \in M$ and $c < 0$, so $\mathbf{\lambda}^T \mathbf{x} > 0$ on the simplex. Evaluating at the vertices $\mathbf{e}_j$ gives $\lambda_j > 0$ for every $j$: the separating functional is *strictly* positive. This is the essential point, and it is what distinguishes the theorem from a triviality.

Write $\mathbf{\lambda} = (\lambda_0, \mathbf{\lambda}_{1:K})$. Orthogonality to $M$ says that for every portfolio,

$$
-\lambda_0 \mathbf{\theta}^T\mathbf{S} + \mathbf{\lambda}_{1:K}^T \mathbf{D}^T \mathbf{\theta} = 0 \quad \forall \mathbf{\theta} \in \mathbb{R}^N \ \Rightarrow \ \lambda_0 \mathbf{S} = \mathbf{D} \mathbf{\lambda}_{1:K}.
$$

Since $\lambda_0 > 0$ we may normalize, $\mathbf{\psi} = \mathbf{\lambda}_{1:K} / \lambda_0 \in \mathbb{R}^K_{++}$, and obtain the *state price vector*:

$$
\mathbf{S} = \mathbf{D}\mathbf{\psi}, \quad \text{i.e.} \quad S_i = \sum_{k=1}^K \psi_k D_{ik}, \quad \psi_k > 0.
$$

Every asset's price is a strictly positive linear combination of its state-by-state payoffs, with weights that are the same for all assets. The interpretation of $\psi_k$ is direct: it is the price today of an [Arrow-Debreu security](https://en.wikipedia.org/wiki/Arrow%E2%80%93Debreu_model) that pays exactly $1$ if state $\omega_k$ occurs and nothing otherwise. Such a security need not be traded; no arbitrage nevertheless forces a consistent shadow price for it.

The converse is easy and worth stating, because it is the direction one uses in practice. If a strictly positive $\mathbf{\psi}$ with $\mathbf{S} = \mathbf{D}\mathbf{\psi}$ exists and $\mathbf{D}^T\mathbf{\theta} \ge 0$ with some strictly positive entry, then $\mathbf{\theta}^T \mathbf{S} = \mathbf{\psi}^T \mathbf{D}^T \mathbf{\theta} > 0$, so the portfolio costs strictly positive money and is not an arbitrage. Existence of state prices and absence of arbitrage are therefore equivalent. Abstractly: no arbitrage means the pricing rule is a strictly positive linear functional on the space of attainable payoffs, and such functionals are always representable as weighted sums.

### The Risk-Neutral Measure

State prices are already the theorem, but they are not yet in the form used by practitioners. Suppose the market contains a riskless asset - a bond paying $1$ in every state - or that such a payoff can be built from the traded assets. Its price is $\sum_k \psi_k$, and we define the riskless rate by $\sum_k \psi_k = 1/(1+r)$. Now normalize the state prices into probabilities:

$$
q_k = \frac{\psi_k}{\sum_j \psi_j} = (1+r)\psi_k, \quad q_k > 0, \quad \sum_k q_k = 1.
$$

Since the $\psi_k$ are strictly positive and sum to $1/(1+r)$, the $q_k$ are a genuine probability distribution $\mathbb{Q}$ on $\Omega$. Substituting back into the pricing relation gives

$$
S_i = \sum_k \psi_k D_{ik} = \frac{1}{1+r} \sum_k q_k D_{ik} = \frac{1}{1+r} \mathbb{E}_\mathbb{Q}[D_i].
$$

Every asset's price is its expected payoff *under $\mathbb{Q}$*, discounted at the riskless rate. Equivalently, the discounted price process is a [martingale](https://en.wikipedia.org/wiki/Martingale_(probability_theory)) under $\mathbb{Q}$, which is why $\mathbb{Q}$ is called an *equivalent martingale measure*. It is equivalent to $\mathbb{P}$ in the technical sense that the two agree on which events are impossible - here both give every state positive probability - and this is exactly the condition that rules out arbitrage rather than merely making the algebra work. We can now state the theorem.

> **First FTAP.** The market admits no arbitrage if and only if there exists a probability measure $\mathbb{Q}$, equivalent to the physical measure $\mathbb{P}$, under which discounted asset prices are martingales.

The name "risk-neutral" is unfortunate and confuses many people. Nobody in this market is risk-neutral, and $\mathbb{Q}$ is not anybody's belief about the future. It is a bookkeeping device: a reweighting of the states that absorbs all risk preferences into the probabilities, so that the pricing operator looks like a plain expectation. Discounting at $r$ and expecting under $\mathbb{Q}$ is right; discounting at $r$ and expecting under $\mathbb{P}$ is wrong.

### The Stochastic Discount Factor

To see where the risk preferences went, factor the state prices through the physical probabilities. Define

$$
m_k = \frac{\psi_k}{p_k} > 0 \ \Rightarrow \ S_i = \sum_k p_k m_k D_{ik} = \mathbb{E}_\mathbb{P}[m D_i].
$$

The random variable $m$ is the *stochastic discount factor* (SDF), or pricing kernel. The same object appears as the [Radon-Nikodym derivative](https://en.wikipedia.org/wiki/Radon%E2%80%93Nikodym_theorem) relating the two measures, $d\mathbb{Q}/d\mathbb{P} = q_k/p_k = (1+r)m_k$. So the risk-neutral measure is the physical measure tilted by $m$, and the tilt is where risk aversion hides. In a consumption-based model with utility $u$ and discount factor $\delta$ one finds $m = \delta \, u'(c_1)/u'(c_0)$: the SDF is high in states where the investor is poor and marginal utility is large. $\mathbb{Q}$ therefore overweights bad states relative to reality, which is precisely why payoffs concentrated in bad states are expensive.

This single equation reproduces the entire cross-section of risk premia. Let $R_i = D_i / S_i$ be the gross return, so that the pricing relation reads $1 = \mathbb{E}[m R_i]$. The riskless asset gives $1 = \mathbb{E}[m] R_f$, hence $R_f = 1/\mathbb{E}[m] = 1 + r$. Expanding the expectation of the product,

$$
1 = \mathbb{E}[m]\mathbb{E}[R_i] + \text{Cov}(m, R_i) \ \Rightarrow \ \mathbb{E}[R_i] - R_f = -\frac{\text{Cov}(m, R_i)}{\mathbb{E}[m]}.
$$

An asset earns a premium over the riskless rate exactly to the extent that it pays badly when the SDF is high, i.e. when times are bad. Assets that pay well in bad states are insurance, and they command *negative* premia - people accept a low expected return for them. Nothing here mentions variance. An asset can be wildly volatile and still carry no premium, provided its volatility is uncorrelated with $m$. Choosing a specific functional form for $m$ recovers the standard models; making $m$ linear in the market return gives the CAPM, and its $\beta$ is just the special case of the covariance above.

### Completeness and the Second FTAP

The set of payoffs you can manufacture is the span of the rows of $\mathbf{D}$, i.e. $\{ \mathbf{D}^T\mathbf{\theta} : \mathbf{\theta} \in \mathbb{R}^N\} \subseteq \mathbb{R}^K$. The market is *complete* if this span is all of $\mathbb{R}^K$: any state-contingent payoff whatsoever can be replicated by trading. Since $\mathbf{D}^T$ is surjective onto $\mathbb{R}^K$ exactly when $\text{rank}(\mathbf{D}) = K$, and a rank-$K$ matrix with $K$ columns has independent columns, the map $\mathbf{\psi} \mapsto \mathbf{D}\mathbf{\psi}$ is then injective. The linear system $\mathbf{S} = \mathbf{D}\mathbf{\psi}$ has at most one solution:

> **Second FTAP.** An arbitrage-free market is complete if and only if the equivalent martingale measure is unique.

When the market is incomplete, $\text{rank}(\mathbf{D}) < K$ and the solutions form an affine set, $\mathbf{\psi}_0 + \ker \mathbf{D}$, intersected with the positive orthant - a convex polytope of measures, all consistent with the observed prices. A claim that lies in the span still has a unique price, because all the measures agree on it. A claim outside the span does not. Its no-arbitrage prices fill the open interval

$$
\left( \inf_\mathbb{Q} \frac{\mathbb{E}_\mathbb{Q}[X]}{1+r}, \ \sup_\mathbb{Q} \frac{\mathbb{E}_\mathbb{Q}[X]}{1+r} \right),
$$

with the endpoints being the cheapest super-replicating and the most expensive sub-replicating portfolio. Outside that band you can be arbitraged; inside it, theory is silent and the price is set by preferences, supply and demand, or hedging costs. This is the precise sense in which no-arbitrage pricing is a consistency requirement rather than a theory of value.

### A Worked Example

Take one stock at $S_0 = 100$ that moves to either $120$ or $90$, and a bond with $r = 5\%$. So $K = 2$, $N = 2$, and

$$
\mathbf{S} = \begin{pmatrix} 1 \\ 100\end{pmatrix}, \quad \mathbf{D} = \begin{pmatrix} 1.05 & 1.05 \\ 120 & 90 \end{pmatrix}.
$$

Solving $\mathbf{S} = \mathbf{D}\mathbf{\psi}$ gives $\psi_u = \psi_d = 1/2.1 \approx 0.4762$, hence $q_u = q_d = 1/2$. In general the up-probability is

$$
q_u = \frac{(1+r)S_0 - S_d}{S_u - S_d},
$$

which lies in $(0,1)$ if and only if $S_d < (1+r)S_0 < S_u$. That inequality is the no-arbitrage condition in this market, and it is intuitive: if the stock beat the bond in *both* states you would borrow and buy it for free money, and if it lost in both you would short it. Notice also that the physical probability of an up-move never appeared. It is irrelevant to the price.

A call struck at $100$ pays $(20, 0)$, so its price is $20 \cdot 0.4762 = 9.52$. The replication check: hold $\Delta = (20-0)/(120-90) = 2/3$ shares, worth $66.67$ today with payoff $(80, 60)$, and borrow $60/1.05 = 57.14$ to strip out the constant $60$. Net cost $66.67 - 57.14 = 9.52$, exactly as the measure predicted. Two computations, one hedging and one probabilistic, must agree - that is the content of the theorem.

Now break completeness by adding a third state in which the stock is unchanged at $105$. The matrix $\mathbf{D}$ is $2 \times 3$ and has rank $2 < 3$. The measures satisfy $q_u + q_m + q_d = 1$ and $120 q_u + 105 q_m + 90 q_d = 105$; subtracting $105$ times the first from the second gives $q_u = q_d = t$, so $\mathbb{Q}_t = (t, 1-2t, t)$ for any $t \in (0, 1/2)$. The call now pays $(20, 5, 0)$, and its price is $(5 + 10t)/1.05$, which ranges over $(4.76, 9.52)$. One extra state, and a sharp price became an interval spanning a factor of two. Incompleteness is not a technicality.

### More Dates, and Continuous Time

Nothing essential changes with many dates. One introduces a filtration $\mathcal{F}_0 \subseteq \dots \subseteq \mathcal{F}_T$ describing the arrival of information, restricts attention to self-financing strategies whose holdings at $t$ are $\mathcal{F}_t$-measurable, and the theorem reads the same: no arbitrage over the whole tree is equivalent to the existence of an equivalent $\mathbb{Q}$ making the discounted price process $S_t / B_t$ a martingale. The value of a claim at any intermediate date is then $V_t = B_t \, \mathbb{E}_\mathbb{Q}[ V_T/B_T \mid \mathcal{F}_t]$, and the hedge ratios are the increments of the martingale representation. For arbitrary state spaces in discrete time this is the [Dalang-Morton-Willinger theorem](https://en.wikipedia.org/wiki/Fundamental_theorem_of_asset_pricing).

Continuous time is where the statement needs genuine repair. With infinitely many trading dates one can construct doubling strategies that manufacture a sure profit in the limit, so "no arbitrage" as stated is too weak to characterize anything, while requiring an *equivalent martingale* measure is too strong. The fix is the condition of *no free lunch with vanishing risk* (NFLVR): there is no sequence of admissible strategies whose downside shrinks to zero while their profits do not. The [Delbaen-Schachermayer theorem](https://en.wikipedia.org/wiki/Fundamental_theorem_of_asset_pricing) then says NFLVR holds if and only if an equivalent local martingale measure exists. The economics is unchanged; the qualifiers exist to control pathologies of continuous trading.

The machine that produces $\mathbb{Q}$ in continuous time is [Girsanov's theorem](https://en.wikipedia.org/wiki/Girsanov_theorem), which describes how a change of measure changes the drift of a diffusion while leaving its volatility alone. If under $\mathbb{P}$ the stock follows $dS_t = \mu S_t dt + \sigma S_t dW_t^\mathbb{P}$, then setting $W^\mathbb{Q}_t = W^\mathbb{P}_t + \int_0^t \theta_s ds$ with the *market price of risk* $\theta = (\mu - r)/\sigma$ yields

$$
dS_t = r S_t dt + \sigma S_t dW_t^\mathbb{Q}.
$$

Under $\mathbb{Q}$ the stock drifts at the riskless rate. The claim's price is then the discounted expectation, $V_t = e^{-r(T-t)} \mathbb{E}_\mathbb{Q}[(S_T - K)^+ \mid \mathcal{F}_t]$, and evaluating that Gaussian integral gives back the Black-Scholes formula $V = S N(d_1) - Ke^{-r(T-t)}N(d_2)$ - the same answer obtained from the delta-hedging PDE, as [Feynman-Kac](https://en.wikipedia.org/wiki/Feynman%E2%80%93Kac_formula) guarantees it must. The striking part is what dropped out: $\mu$ is nowhere in the formula. The expected return of the stock, the hardest quantity in finance to estimate, is irrelevant to the price of its options, because a hedged position does not care which way the stock drifts. Only $\sigma$ survives.

### Reading $\mathbb{Q}$ Off the Market

Since $\mathbb{Q}$ is not a belief, it cannot be estimated from historical returns. It can, however, be observed directly, because option prices *are* statements about $\mathbb{Q}$. For a continuum of strikes on the same maturity, $C(K) = e^{-r\tau}\mathbb{E}_\mathbb{Q}[(S_T - K)^+]$, and differentiating twice under the integral,

$$
\frac{\partial C}{\partial K} = -e^{-r\tau}\, \mathbb{Q}(S_T > K), \qquad \frac{\partial^2 C}{\partial K^2} = e^{-r\tau} f_\mathbb{Q}(K).
$$

This is the [Breeden-Litzenberger](https://en.wikipedia.org/wiki/Breeden%E2%80%93Litzenberger_formula) result: the risk-neutral density is the second derivative of the call price curve with respect to strike, which is exactly the limit of a butterfly spread. It also explains why $C$ must be convex in $K$ - a concave kink would make some butterfly cost negative while paying non-negative amounts, an arbitrage. Applied to real option chains, the recovered density is not lognormal: it is left-skewed and fat-tailed, which is the same fact as the implied volatility smile. Part of that shape is genuine belief about crash risk and part is the $m$-tilt, i.e. the premium investors pay for insurance. The FTAP guarantees a consistent $\mathbb{Q}$ exists but cannot separate those two components; that requires a model of preferences.

### What It Does and Does Not Give You

The theorem's real function is to convert an economic axiom into an object one can compute with. Prices are linear in payoffs by accounting and positive by no arbitrage, and a strictly positive linear functional is always an expectation under some measure. Everything downstream - risk-neutral valuation, the SDF, martingale hedging, numeraire changes - is a restatement of that one sentence. It is also worth appreciating how little was assumed: no equilibrium, no utility, no rationality, no distributional form. Only that free money is not lying around.

The flip side is that the theorem is silent about which $\mathbb{Q}$. It is a statement about the internal consistency of a price system, not about whether prices are sensible. A market can be arbitrage-free and still be a bubble; every price in it is consistent with every other. And the frictionless setting is doing real work. With transaction costs, bid-ask spreads, short-sale constraints, or collateral requirements, no arbitrage no longer pins down a single measure but a family of them, and prices become intervals - the pricing functional becomes sublinear rather than linear. Even the exact arbitrages the theorem excludes are not always exploitable in practice, as arbitrageurs face funding limits and mark-to-market risk and can be forced to close a converging trade at a loss. The theorem describes the geometry that prices must respect. It does not promise anyone is around with the capital to enforce it. -->
