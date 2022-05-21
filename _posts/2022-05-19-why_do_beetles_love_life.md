---
layout: post
title: Why Do Beetles Love Life?
date: 2022-05-19 16:00:00 +0200
tags: [ai, ultra-rationalism]
---

Have you ever seen a beetle stuck on its back, trying to roll over? It moves its legs in all directions trying to grab onto any sticks, straws, or ledges from which to push itself. In its foresty natural habitat, if a beetle falls on its back, this is not a terribly problematic situation because the terrain around it is typically very rugged with lots of things to grab onto. Moreover, many species of beetles have small hooks on their legs which facilitate the "grabbing process". In a non-natural surrounding however, when there's nothing to grab on to, the poor creature may be left squirming around for an extended period of time. Obviously, a beetle has developed instincts, driving it to try to roll-over. But what is the purpose of those instincts? To keep the beetle alive as long as possible? More importantly, what is it exactly that causes virtually all organisms to try to stay alive and to fight for their life, even in the direst of situations? Why do we choose life?

The question "Why do all organisms try to stay alive?" sounds a lot like "What is the purpose of life?" but the latter one is a meaningless. This is because a purpose, as we understand it, exists only in the context of an agent capable enough to conceptualize the need for action in a situation where a different outcome than the current one is desired. I can say that my purpose is to act so as to cause a certain effect, or that my purpose is to be the driver of specific directed actions, but all this is anthropocentric babble not getting to the heart of the issue. It presumes a conceptual understanding of things like "self", "action", and "opportunity", and we know that life has emerged much before any organism could have time to conceptualize these. 

We can't meaningfully say that a chemical reaction has purpose. But treating life simply through the lens of complexity requires us to make the connection between the high level understanding of "purpose" and the low-level understanding of "cause and effect". Any explanation for the purpose of our existence based on developments from recent history is bound to miss the point. You can't say that the purpose of life is to maximize the likelihood of the species' survival, because a most primitive organism does not even know what a species is. Even more, how do genes know what the species of their carrier is? If life has any global purpose at all, this purpose has to be fundamental, primitive, and simple.

Some people believe that **the purpose of life is to increase complexity**. The complexity of living organisms (informally understood as the complexity of the biological structures in their cells) is much greater than that in non-living ones. [Assembly theory](https://en.wikipedia.org/wiki/Assembly_theory) measures the complexity of molecules and proves empirically that molecules occurring in living organisms have a higher assembly index that those in non-living objects. 

Similarly, **living organisms tend to be more ordered than non-living ones**. The second law of thermodynamics states that all isolated systems will, with time, reach a state of maximal entropy. So why does life on Earth flourish? Well, because the biosphere is not an isolated system. Organisms reduce the entropy inside of them (they harvest [negentropy](https://en.wikipedia.org/wiki/Negentropy) packets) at the expense of their surrounding. As this process continues, living organisms can become more ordered, while the environment in which they live - more unordered.

While all of this is true - that life increases complexity and order - these relationships are observed consequence of the way life functions. They are not its purpose.

**In reality, life has no ultimate purpose**... What we observe all around us are organisms with behavioural traits that simply help them survive. Coming back to our example, why does a beetle stuck on its back try to roll over? Because this helps it survive. Why do all beetles around us have this behaviour? Because they wouldn't be around us, if they hadn't adopted this behaviour.

### How life evolved
Life has developed and evolved from primitive molecules. One plausible hypothesis is that as the chemical composition of the early universe was changing, larger and heavier molecules started to form. This was an entirely chemical process - when the right molecules would bump into each other, and under the right thermodynamic circumstances, a reaction would be triggered and new more complex molecules would be created. This process continued and eventually, by chance, a very special molecule was formed - one that could produce an exact copy of itself under the right conditions.

This proved a game changer because a molecule that could replicate itself meant that its copies would also replicate themselves. Therefore, in a given pool of molecules, the proportion of molecules with that specific chemical composition started to increase.
However, during the copying process, random changes, or *mutations* would occur. Some of these decreased the probability that a molecule with these mutations would replicate, while others increased it. One can easily see then, that under such a selection process those molecules with mutations that favour their replication would start to dominate the total pool of complex molecules.
Those with mutations that didn't favour replication would simply decrease in proportion to the rest and possibly become extinct.

Through this process of replication, mixed with random changes, the molecules continued to increase in complexity and form structures which in turn started to form even bigger structures. It is believed that the cell is the smallest unit of life because it can replicate and produce feedback loops to adapt to the environment and regulate its own state.

### Simulations
Let's look at evolution from a more computational perspective. For evolution to commence, we need to have three components:
- an agent that can replicate,
- a mutation operator to mutate agents,
- a fitness function which computes the probability that an agent will replicate at time $t$.

Then the evolution of the organisms consist of a sequence $\mathcal{A}_0, \mathcal{A}_1, ... \mathcal{A}_t, ...$ where $A_t$ is a set of all living agents at time $t$, and $n_t$ is the number of living agents at time $t$: 

$$\mathcal{A}_t = \{A^1_t, A^2_t, ..., A^{n_t}_t\}.$$

To simulate the evolution from one step to the next we take the current agents, and assess whether each one of them will replicate using the fitness function. At the next step, those who are deemed to replicate create copies of each other, but with small changes added to the copies. In reality the fitness function is incredibly complicated - it is random, changing with time, and depending on the current set of organisms $\mathcal{A}_t$. This reflects the availability of resources, the competition between agents due to population growth, and numerous other factors.

Let's simulate a very basic evolutionary process. A creature, for example some kind of bacteria, will be a vector of $10$ discrete integers, called features, each in the range $\\{0, ...., 7 \\}$. The fitness function will be time-invariant and deterministic. It takes in a single creature as input, and outputs $1$, meaning that this creature will replicate, only if the first feature of the creature is $1$ and the last one is not more than $5$:

$$
P(A^i \text{ will replicate}) = 
\begin{cases}
1 & \text{ if } A^i [0] = 1 \text{ and } A^i[9] \le 5 \\
0 & \text{ otherwise}. 
\end{cases}
$$

When a creature replicates, it creates a copy of itself and then a mutation is applied to both its copy and itself. The mutation consists of setting a random feature to a random value. Only those creatures for which the fitness function yields a $1$ get to replicate. The ensemble of all agents at time $t$ can be represented as a matrix $M$ where the rows of $M$ index the creatures and the columns index the features. In figure 1 below, we begin with an initial set of $30$ random creatures and evolve them for just $5$ steps. When comparing the ensembles we see that the creatures in the evolved one have developed strongly correlated first and last features. This is because these features are important for replication and if you do not develop them in such a way, you will simply not replicate. The other features are irrelevant to the probability of replication and hence there's more sustained diversity there.

<figure>
    <img class='small_img' src="/resources/deterministic_fitness.svg" alt="Deterministic fitness" width="1200">
    <figcaption>Figure 1: A comparison of an initial and an evolved ensemble. The evolved ensemble has developed regularities in those features that are important for replication.</figcaption>
</figure>

Let's try with another example where the fitness function is random and there is some population capacity. In this case the probability that $A^i_t$ will replicate is given by

$$
P(A_t^i \text{ will replicate}) = \frac{N - n_{t-1}}{N (1 + \exp(- \mathbf{w}^\intercal A_t^i ))}
$$

where $N$ is the maximum population capacity, $n_t$ is the current population size, $A_t^i$ is a vector with the features of creature $i$ in time $t$, and $\mathbf{w}$ is a fixed vector of replication weights that defines which feature increases the probability of replication and by how much. In the experiment, we use $30$ features, each with real values. The mutation selects one of the features and sets it to a random value coming from a standard normal distribution. 

Figure 2 summarizes the results after 300 iterations. The top graph shows the mean and standard deviation of the features across the ensemble after 300 iterations. We can see that generally when the replication weights are negative, the evolved features are also negative. Likewise, if the replication features are positive, then the evolved features are also positive. The bottom plot shows how the correlation between the mean features and the replication weights evolves with time. The correlation is not $1$ because of the constant noise from the mutations.

<figure>
    <img class='img' src="/resources/probabilistic_fitness.svg" alt="Probabilistic fitness" width="1200">
    <figcaption>Figure 2: Distributional statistics for the features evolved after 300 iterations (top). Evolution of the correlation between the mean ensemble features and the replication weights (bottom).</figcaption>
</figure>

The two experiments above suggest that:
- Only a fitness function, a mutation operator, and the ability to create copies, are needed in order for evolution to occur;
- The evolution process favours those changes which increase the fitness of the agent, where the fitness is related to how probable it is to replicate;
- The evolution process can create order and complexity out of chaos and uniformity. It has no global purpose and is driven simply by computation, manifested in the behaviour of the agents. Does this count as virtual life, albeit extremely simple?

### Implications

Evolution is most probably the greatest natural stochastic process, responsible for the continuous development of all life based on organic chemistry. If aliens exist and have a similar organic structure, we can expect they go through a similar type of evolution.

Specifically with humans however, the effects of evolution have started to become, and will become, trumped by those of technology. As technology progresses and life becomes arguably safer and easier, your survival will depend less and less on your physical and mental capabilities. As a result, the biological variance between people will increase. It will be more likely to encounter wild deviations from the mean in every aspect of society. Better healthcare, social welfare, mass communication, and artificial intelligence are just some of the things which make life easier for the individual, but are also likely to increase entropy on a macroscale... Is this trade-off worth it? I think yes. This is the price of progress.

Treating evolution as computation shows that there is no global purpose to our lives. Ultimately, we are autotelic agents, capable of inventing our own purposes. There is no predefined, global reward function. Each one of us should come up with their own in order to live a meaningful life. And in the market for global reward functions there are many players - religious prophets, philosphers, writers, politicians... they're all selling. So are you willing to buy?