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

For example, the stochastic matrix
$$\small
\begin{pmatrix}
0 & 1/2 \\
1 & 1/2
\end{pmatrix}
$$ has eigenvalues $-\frac{1}{2}$ and $1$, and corresponding eigenvectors
$$ \small c_1 .
\begin{pmatrix}
-1 \\
1
\end{pmatrix}
$$ and 
$$ \small c_2 .
\begin{pmatrix}
1 \\
2
\end{pmatrix}
$$ 