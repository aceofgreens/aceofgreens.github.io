---
layout: post
title: The Ising Model
date: 2022-05-11 16:00:00 +0200
tags: cs
---

The Ising model is a curious little toy model for ferromagnetism in the field of statistical mechanics. While surprisingly simple in terms of definition, it is able to produce very interesting various outcomes, whose explanations are in my opinion, quite deep. This post aims to give a quick introduction to the model, how to sample from it, and how to solve it analytically in one dimension.

The Ising model consists of a grid of $n$ sites, where each site $s_i$ can have a positive spin or negative spin, i.e. $s_i \in \{+1, -1 \}$. Let's call $n$ the size of the system. Then just based on that, we can say that the system has $N = 2^n$ possible states, where each state consists of the actual spins for all sites. 

The energy of each spin depends also on that spin's neighbors and the state of the system, consisting of all spins $s_i$, has overall energy $E(s) = -\sum_i \sum_j s_i s_j $. The interaction $-s_i s_j$ suggests a ferromagnetic interaction where this quantity is $1$ if $s_i$ and $s_j$ have different spins and $-1$ otherwise. Since physical systems generally try to be in a state that minimizes their energy, we have it that the system will be in a minimum-energy state if the spins at all sites are the same (which is what keeps the system magnetized).

Importantly, the state in which the system may end up in equilibrium may not be the minimum energy one. We model that state as a random variable with a Boltzmann distribution:

$$
P_{eq}(s) = \frac{\exp(-\beta E(s))}{\sum_s \exp(-\beta E(s))}.
$$

Here $E(s)$ is the energy of the state as defined above and $\beta = \frac{1}{T}$ is a coefficient depending on the temperature $T$. Generally, if $T \rightarrow \infty$, and therefore $\beta \rightarrow 0$, the system is equally likely to be in any of the states. If, on the other hand, $T \rightarrow 0$, and therefore $\beta \rightarrow \infty$, the system has positive probability of being only in states with the minimum energy.

Typically, we might be interested in the magnetization, defined as the average spin $m = \frac{1}{n}\sum_i s_i$. This sum is across all $n$ sites.

<figure>
    <img class='extra_big_img' src="/resources/ising_samples.png" alt="IMOL2022 highlights" width="1200">
    <figcaption>Figure 1: Three samples from the Ising model.</figcaption>
</figure>
