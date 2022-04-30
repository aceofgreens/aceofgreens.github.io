---
layout: post
title: Counting by Sampling
date: 2022-04-27 16:00:00 +0200
tags: cs
---

Markov chain techniques have proven themselves incredibly valuable in fields like statistics and machine learning where the goal is to sample from a distribution whose density is too complicated to calculate analytically. Algorithms like [Metropolis-Hastings](https://en.wikipedia.org/wiki/Metropolis%E2%80%93Hastings_algorithm) produce samples from the required distribution by iterating a discrete stochastic process where the next state depends only on the current state (this being the Markov property). The typical statistical treatment of such an algorithm ends somewhere around here - you implement the algorithm, you let it run for a predefined number of steps, and you assess the quality of the results by looking at outputs like trace plots, autocorrelation plots, and burn-in periods. However, like any other algorithm, Markov chain sampling algorithms have a time complexity which can be analyzed... and computer science has a lot to say about that.

### todo: fill this outline later

We begin by recalling some basic facts about Markov chains.

Markov chains are stochastic processes where the probability of the next state in time $t+1$ depends only on the current state at time $t$. We'll be mostly interested in discrete Markov chains which can be represented as (possibly infinite) directed graphs where the nodes are the states and the edges are the transitions. The chain is *irreducible* if any state $y$ is eventually reachable with non-negative probability from any chain $x$. If also, for every state $x$ in which we start, there is a number of steps $t$, such that for all $t' \ge t$, the probability of returning to $x$ is positive, then this chain is *aperiodic*. If a Markov chain with finitely many states is irreducible and aperiodic, then it is ergodic - it will always converge to a unique equilibrium distribution as $t \rightarrow \infty$.

The Markov chain can be represented as a stochastic matrix. If the chain is ergodic, this matrix has an eigenvalue of 1, whose eigenvector is the equilibrium distribution. All other eigenvalues have an absolute norm less than 1.

Typically, we're interested in quantifying how close is the current distribution over the states at time $t$ compared to the equilibrium distribution. This can be done with the total variation distance:

$$
0 \le {\lVert P - Q \rVert}_{\text{tv}} = \frac{1}{2}\sum_{x}|P(x) - Q(x)| \le 1
$$

Consider this example, we have a Markov chain with two states. From state 1 we always transition to state 2, while in state 2 we move to state 1 with 50% probability and remain in state 2 with 50% probability. Then the stochastic matrix corresponding to this Markov chain is
$$\small M = 
\begin{pmatrix}
0 & 1/2 \\
1 & 1/2
\end{pmatrix}
$$. Its eigenvalues are $1$ and $\lambda = -\frac{1}{2}$, and the corresponding eigenvectors are
$$ \small P_{eq} = 
\begin{pmatrix}
1 \\
2
\end{pmatrix}
$$ 
and 
$$ \small v = 
\begin{pmatrix}
1 \\
-1
\end{pmatrix}
$$.
The eigenvectors form a basis and therefore any distribution over the states at $t=0$, for example
$$
\small P_0 = 
\begin{pmatrix}
1 \\
0
\end{pmatrix}$$, can be represented as a combination of the equilibrium distribution $P_{eq}$ and the other eigenvector $v$:
$$
P_0 = P_{eq} + \frac{2}{3}v
$$. The distribution after $t$ steps is then

$$
P_t = M^t (P_{eq} + \frac{2}{3}v) =  P_{eq} + \frac{2}{3} \lambda^t v = P_{eq} + (-1)^t 2^{-t} \small\begin{pmatrix}
2 \\ -3 \end{pmatrix}.
$$


Importantly, as $t \rightarrow \infty$, the memory of the initial state decays exponentially fast as $\|\lambda \|^t = 2^{-t}$ and as a result the total variation decays similarly 

$${\lVert P_t - P_{eq} \rVert}_{\text{tv}} = \frac{2}{3} \left| \lambda \right|^t = \frac{2}{3}2^{-t}.$$

The number of steps needed to reach a small distance $\epsilon$ from $P_{eq}$ is given by $t = \log_2 \frac{2}{3\epsilon} = O(\log \epsilon^{-1})$, which motivates the definition of *mixing time* - a "loose" measure of the runtime, or computational complexity of that Markov chain. The $\epsilon$-mixing time is the smallest $t$ such that irrespective of the starting distribution, at time $t$ the total variation between $P_t$ and $P_{eq}$ is at most $\epsilon$:

$$
\tau_\epsilon = \min \big\{ t \ | \max_{P_0} {\lVert P_t - P_{eq} \rVert}_{\text{tv}} \le \epsilon \big\}.
$$

In reality, what we are interested in is how the mixing time depends on $n$ - the system size, not $\epsilon$ per se, because this allows us to understand how the mixing time scales with larger and larger problem instances. The total number of possible states $N$ could be exponentially large in $n$ (as in Ising models or graph coloring problems) and to be able to sample from such large spaces we'll need polynomial mixing times in $n$, i.e. $\tau = O(\text{poly}(n))$. An optimal mixing time which we call *rapid mixing* is when $\tau$ scales as $O(n \log n)$.