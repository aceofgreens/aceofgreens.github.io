---
title: On the Merits of Weighted Voting
date: 2022-08-01 16:00:00 +0200
tags: econ, ultra-rationalism
slug: on_the_merits_of_weighted_voting
---

[Weighted voting](https://en.wikipedia.org/wiki/Weighted_voting), the idea that some participants have bigger weight to their vote than others, is a controversial but important idea. While it can illuminate many of our modern world practices and suggest novel ways to look at them, it still seems under-developed in the literature, at least in those aspects which I'll discuss here. This topic is near and dear to me and I have spent the last four years thinking about it. I have discussed it with friends and acquaintances, finding that few share my enthusiasm on it. Nonetheless, time and logic have fully convinced me of its merit... Buckle up, this is going to be a ride.

People form societies with the goal of solving their mundane daily tasks in a more efficient manner. This is a most natural thing to do. A society consists of the individual people and the social relationships between them, this forming a social organization where

- the effects of one person's actions spill over to the others,
- people attain greater benefits from cooperation rather than competition.

However, conflicts inevitably arise between the individual members and they can be resolved using violence or diplomacy. Which of these is deployed depends largely on how costly violence would be for the participating parties. Contrary to violence, voting is a standard way of diplomatic conflict resolution. It is possible only if people agree that everyone will cast their vote, and a single outcome will be decided based on all votes, possibly weighted by certain merit criteria. Note that this includes the democratic case of equal voting weights. The procedure of selecting the final decision from the individual votes should be known and accepted by all so that the final outcome doesn't depend on e.g. the person counting the votes.

The final voting result creates winners and losers. Those whose individual vote is in agreement with the final result will be satisfied, while those whose votes are different from the final result will be malcontent. A big question in economics is whether we can objectively measure the outcome of such scenarios, where we have net winners and net losers on both sides. You see, the voting setup is just a tool for coordination, an algorithm for the problem of optimal allocation of scarce resources with globally-felt consequences. Therefore, we are mainly interested in the following:

- **How can we evaluate the outcome from a voting system when there are competing and self-contradicting performance metrics present?** To one net loser, the outcome may feel like a disastrous calamity, while for another it may just be a temporary setback. Which one of these opinions should we base our analysis on?
- **How can we design a voting system that will maximize the created value in most cases, under a given quality definition?** A better voting system will produce more value for all people. Obviously, we want to create value, rather than destroy it.

### The scourge of utility
People have [preferences](https://en.wikipedia.org/wiki/Preference_(economics)) over world states. These are the orderings that are attributed to hypothetical states of the world. For example, a person may prefer the state where he works as a teacher to that where he works as a car technician. In turn, he may prefer being a car technician to being unemployed. His preferences create a ranking of these scenarios according to how beneficial they are. A lot of theory could be developed around preferences - whether they are stable across time, complete, transitive, convex, strict, stochastic, and so on. None of these matter for this discussion. What matters is that preferences represent the attitudes of people toward different scenarios.

Using the concept of preferences we can get a first primitive performance metric for analyzing voting outcomes. For a binary vote with a yes/no outcome, we can simply count how many voters prefer the final vote to its alternative. Assuming that everyone voted for their preferred outcome, this is exactly like counting the people who voted for the final result. And if the final result is chosen by the majority vote, then this already maximizes our performance metric.

However, looking at just the preferential order of the outcomes misses the fact that these preferences have a magnitude, or intensity. One person may prefer peace to war much more strongly than another. And if this is not taken into account, the binary majority vote, while maximizing the number of preferred outcomes, may not maximize their total magnitude.

To represent the magnitude of preferences in a quantitative way we may use [utility functions](https://en.wikipedia.org/wiki/Utility). These are mathematical functions which take in as input a given world state and output a real number. For example, for a given person, the world state of having 3 cars and 2 houses may produce a utility of 250, while 2 cars and 3 houses - 350. Needless to say, working with actual numbers is beneficial because it allows us to create proper mathematical models - the entire [consumer choice](https://en.wikipedia.org/wiki/Consumer_choice) is based on utility functions.

While very useful for simple modelling, utility functions are not applicable to the real world because:

- Real world utility functions are *extremely* complex - they may be random, unstable, stochastic, or with no closed mathematical form. The famous [Cobb-Douglas](https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function) functional form is rarely found in real life.
- The utility units of measurement are meaningless. What does it mean to have utility 350? This is only meaningful when compared to a utility of 250 or 400.

The outcome of the vote implies a utility for everyone and hence, you can measure the total utility for that outcome. Some voters will be just happy, some other will be delighted, others may be indifferent, yet others may be in shock. A function representing the utility of a collective is called a [social welfare function](https://en.wikipedia.org/wiki/Social_welfare_function). This is any function that takes in the individual utility functions and aggregates them, representing the utility of the group.

We might try to maximize the total utility of the group, i.e. increase total happiness. But what if there is a person whose utility is extremely volatile and its magnitude is larger than that of the others. Then to increase total utility, we'll have to satisfy him in particular, which requires special treatment. Isn't this unfair?

So we might then try to maximize the average utility, or the median utility. This is more robust to outlier preferences, but still the utility of some individuals will dominate the aggregates. We might switch the objective to maximizing the utility of the least well-off individual (the Rawlsian principle), but then you are disregarding all but one person.

Defining a good social welfare function is problematic because it requires making judgement calls regarding who should be treated preferentially. Utility is only meaningful for comparing states by a single person, not by different people. Moreover, any calculation based on utility is subjective. I firmly believe that it is wrong to consider such a subjective quantity as our target variable to maximize when making decisions with group-wide effects. Instead, we need to come up with something objective, meaningful, and computable.

### The setup

In most countries, the voting setup is the following:

- People forcefully contribute a part of their income through taxation. 
- The contributions are pooled and spent however the government decides, most commonly on redistribution. 
- The voting that takes place is very indirectly about how this pool of money is spent. The people vote for the election of government officials who then change the spending policy.

Suppose that we're trying to design the weights of a voting system such that given all votes, the total utility is maximized. So we go around and ask people about their utilities under the different outcomes. The utility of a person is based on their starting income, how much is taken from them through taxation, and how much they receive from redistribution. But since utility is subjective, any assessment of the voting outcome based on measured utility will also be subjective. Likewise, the most vociferous voters will likely greatly under-report the utility for their undesided outcomes, so that the resulting vote favours them. Finally, nothing prohibits others from doing the same, thus creating an environment where the loudest and most raucous ones will have the largest weights.

Hence, in a voting system where we are trying to set the weights to maximize utility, the people who stand to lose the most utility have the largest weigths. Obvious reasons why we should move away from utility-based social welfare are:

- We are maximizing a subjective and non-static metric.
- Individual utilities from outcomes will be under-reported, in order to get more weight. This process may become more aggravated with time and may continue indefinitely.

A better and objective metric for assessing voting outcomes is the total quantity of money not spent where its owners wanted. In this case, we are setting the weights such that the sum of all contributions whose owners' votes are not equal to the passing vote is minimized. For example, suppose we have a binary vote about how to spend the collected contributions - on education, or on infrastructure. Suppose the passing vote is "infrastructure". Then the cost of that outcome is the sum of all contributions whose owners voted "education".

Counting misallocated money is an objective metric - it is not based on utility, but rather funds contributed, which are clearly measurable. It's also fair, as the different contributions are treated equally and no man is favoured at the expense of others. Let's call this quantity *forceful misallocation* to indicate that these funds are collected forcefully (through taxation) and are misallocated (not spent where their original owners want). 

Given these considerations, I state directly that **the democratic case of equal weights on all votes, does not minimize the forcefully misallocated funds**. The problem with equal votes is that any 51% majority can pass a vote where they misallocate the contributions of the remaining 49%. And if further, those 51% are with the least contributions, then, holding everything else fixed, this actually maximizes forceful misallocation!

I also claim that **minimizing forceful misallocation will tend to produce highly beneficial outcomes in terms of utility**. Why? Because we are willing to spend money on those things which provide the most utility to us. And if you cannot spend that money, then you cannot reap the utility from whatever you have missed out on. Hence, forceful misallocation in voting prevents people from maximizing their individual utility. Or in other words, if we minimize forceful misallocation, we maximize the sum of all individual utilities dependant only on their individual contributions.

<figure>
    <img class='img' src="/images/independent_utilities.svg" alt="Independent utilities" width="1200">
    <figcaption>Figure 1: Utility relationships with two voters. Suppose we have two voters with two utility functions. When considering how they would spend their contributions, the scope of their utilities is shown in yellow, along with their maximums in red. Considering both their own contribution and the other voter's contribution, their utilities can take on a larger set of values - the green ones. The sum of the utilities in the two blue points is nonsensical because these utilities have different scales and are dependent on each other. On the contrary, the sum of utilities in the two red points is meaningful, because they are resulting from separate contributions.</figcaption>
</figure>

### The solution?
So if equal weights do not minimize forceful misallocation, what does? I believe the answer is to have the weights proportional to the contributions. It's quite simple, people who contribute more should have bigger weights on their vote precisely because they stand to lose more if their contributions are misallocated.

This setup has several benefits:

- It is **pragmatic**, as the weights are bound to something objective and measurable. This pragmatism is lacking in other systems where weights are bound to wisdom, as in noocracy, or to technical knowledge, as in a technocracy.
- It is **fair**. Your weights do not depend on who you are, but on rather how much you contribute and this criterion is the same for everyone. Race, religion, and education are extraneous.
- It trades off cost and benefit proportionally. If your share of the contributions is larger than your share of the weights, you have an incentive to contribute less. In the opposite case, you have an incentive to free-ride. Weights tied to contributions is what gives you *skin in the game*.
- More practically, vote buying (or electoral clientelism) will be reduced. Since those who sell their votes are typically people who contribute less through taxes, under a weighted voting scheme they will have less say in the final outcome. This will make the act of buying votes less profitable.

Importantly, the weighted voting setting described above is different from plutocracy - rule of the rich. A wealthy person who does not contribute will have minimal weight and a wealthy person who contributes a lot will have a large weight. In general, wealthy people will be influential only if they contribute. And if they do become the most influential ones, they deserve it by virtue of having contributed the most. Do you not agree?

### Simulations
Let's try to get a better understanding of the effects caused by weighted voting. We'll simulate equal and non equal weights in different simplified problem settings and compare the results, obtaining precious intuition along the way. In all experiments, we'll take the weights to be linearly proportional to the contributions. So a person who has contributed twice as much as another, will have twice as much weight - much like voting rights in corporations.

First, we look at an unrealistic brutal scenario. Suppose there are $N$ voters, each having some wealth $w_i > 0, \ \forall i$. These wealths are sampled randomly from a Pareto distribution, for realism. The dynamic that we focus on is the following: at each iteration $t$, there is a proposed vote for the majority of the poorest voters to plunder the wealth of the remaining wealthier voters and split it uniformly among themselves. Each person can vote "yes" or "no" to support the appropriation or not. In the worst case, the maximum appropriation occurs when the poorest 51% appropriate the wealth of the richer 49%. This is the case we'll look at.

In a democratic setup of "one man, one vote", one would vote "yes" if they stand to gain from this appropriation, i.e. if they are in the bottom 51%, ranked by wealth. Otherwise, they would vote "no". At $t=0$ we have the initial wealths. At $t=1$ the used-to-be richest 49% are now the poorest and they, together with the poorest 2% from the previous 51%, will vote to plunder the wealth of the current 49%. At $t=2$ the previous plunderers will now be poorest, causing them to vote for the plundering of the current richest 49% and so on, creating a cycle.

Mathematically, this dynamic is represented as a folding map that takes in a vector of wealths, sets the elements above a certain threshold to 0, and uniformly distributes the sum of those elements to the elements less than that threshold. Iterating this map converges to an oscillating "equilibrium" with periodicity 2. This means that we eventually reach a state where if voter $i$ has positive wealth in the current iteration, he will lose it and in the next iteration he will have 0 wealth. But he will then be a beneficient of the wealth transfer in that iteration, and so on. There will be only 2 classes of people - those with wealth and those without. The forced misallocation each iteration would converge to a single value, it being the rate at which the cumulative wealth transfer increases.
<figure>
    <img class='big_img' src="/images/weighted_voting_simulation.svg" alt="First simulation" width="1200">
    <figcaption>Figure 2: Results from the first simulation.</figcaption>
</figure>

With weighted voting, more people would have to vote for the pillage. This will result not in a 51/49 split, but rather a 80/20 one. The experiments suggest that we still converge to an equilibrium with constant looting , but this time the wealth is cyclic with periodicity 3. Similarly, there are 3 wealth classes and the forced misallocation is also 3-cyclic. Importantly, it is lower than that under equal weights. This indicates that tying the weights to the contributions, or to how much you stand to lose, reduces forced misallocation.

Let's now look at a different, slightly more realistic scenario. Again, we have $N$ voters. Each voter has a constant income propensity $\xi_i > 0$ dictating how easy it is for them to obtain income (e.g. through labour). This propensity is intended to represent luck, intelligence, knowledge or any other factor that might contribute to having a large periodic income. At every iteration $t$, each voter collects this unconditional income. From this income, each voter pays taxes according to the current tax rate. The taxes are pooled together and divided uniformly among all voters. Hence, to calculate the new wealth for voter $i$, we take his current wealth, add the periodic income, subtract the paid taxes, and add the income from redistribution.

The dynamic that we'll model is whether new proposed changes to the tax rate are accepted or not. Specifically, at every iteration $t$ there is a proposal for a new tax rate and everyone votes whether this new rate should be adopted. Each voter votes "yes" only if they will be better off under the new tax rate, i.e. if their inflows through redistribution minus their outflows through taxes under the new tax rate is greater than that same quantity under the current tax rate. We are interested in how the tax rate will evolve under equal and unequal voting weights.

The simulation can be specified as follows:

$$\begin{align}
\xi_i & \sim \text{Pareto}(\alpha_0), \  \forall i \in \{1, ..., N\}  \\
l_i^t & \sim \mathcal{N}(\xi_i, \sigma_0 \xi_i), \ \forall i, \ \forall t\\
\omega_i^{t+1} & = \omega_i^t + l_i^t - l_i^t \tau(l_i^t, \alpha^t, \beta^t) + \frac{1}{N} \sum_{j = 1}^N l_j^t \tau(l_j^t, \alpha^t, \beta^t) \\
\tau(x, \alpha, \beta) & = 1 - \exp(-(x/\alpha)^\beta) \\
\bar{\alpha}^t & = \alpha^t + \mathcal{N}(0, 1) \\
\bar{\beta}^t & = \beta^t + \mathcal{N}(0, 1) \\
\alpha^{t+1} & = \begin{cases}
\bar{\alpha}^t, & \text{ if } \frac{\sum_i w_i v_i}{\sum_i w_i} > 0.5 \\
\alpha^t, & \text{ otherwise }
\end{cases} \\
\beta^{t+1} & = \begin{cases}
\bar{\beta}^t, & \text{ if } \frac{\sum_i w_i v_i}{\sum_i w_i} > 0.5 \\
\beta^t, & \text{ otherwise }
\end{cases} \\ w_i^t & = 
\begin{cases}
\frac{1}{N}, & \text{ if equal weights}\\
\frac{l_i^t \tau(l_i^t, \alpha^t, \beta^t)}{ \sum_{j = 1}^N l_j^t \tau(l_j^t, \alpha^t, \beta^t)}, & \text{ if unequal weights}\\
\end{cases} \\
\Delta \omega_i^t & = \big(\frac{1}{N} \sum_{j = 1}^N l_j^t \tau(l_j^t, \bar{\alpha}^t, \bar{\beta}^t) - l_i^t \tau(l_i^t, \bar{\alpha}^t, \bar{\beta}^t)\big) -
\big(\frac{1}{N} \sum_{j = 1}^N l_j^t \tau(l_j^t, \alpha^t, \beta^t) - l_i^t \tau(l_i^t, \alpha^t, \beta^t)\big) \\
v_i^t & = 
\begin{cases}
1, & \text{ if }\Delta \omega_i^t > 0 \\
0, & \text{ otherwise}
\end{cases} \\
\end{align}$$

In the notation, subscripts $i$ are used to index the voters, superscripts $t$ are used to index the time iterations. $l$ are the labour incomes, $\xi$ the income propensities, and $\alpha$ and $\beta$ parametrize the tax rate, which is a cumulative Weibull distribution (for simplicity). The proposed tax rates are $\bar{\alpha}$ and $\bar{\beta}$. The votes are $v$, the weights are $w$ and the wealths are $\omega$.

The results from this simulation are striking. Under the equal weights case, the tax rate parameters converge to $\alpha \approx 0$ and $\beta \approx 9.5$. The Weibull cumulative density with these parameters is for all practical purposes 1, for any $x>0$. This means that we converge to a flat 100% tax rate. Everyone pays all their labour income in taxes and receives one $N$-th of the pool - the ultimate communist setting. As a result, the wealths of the voters are approximately the same and grow at the same rate.

Why does this happen? Because labour incomes are heavily skewed to the right, with the mean being greater than the median. As a result, tax contributions are also skewed to the right. Hence, for the poorest 51%, the mean collected tax which they receive will always be higher than what they pay, prompting them to vote for ever increasing taxation.

<figure>
    <img class='big_img' src="/images/weighted_voting_simulation4.svg" alt="Second simulation" width="1200">
    <figcaption>Figure 3: Results from the second simulation.</figcaption>
</figure>

On the other hand, with weights bound to the contributions, we converge to the parameters $\alpha \approx 50$ and $\beta \approx 10$. The resulting tax rate is progressive with a well defined steep slope from 0 to 1 occurring at around $x \approx 45$. However, the labour incomes $l$ from which taxes are paid are less than 2 on average, and as a result, they fall within a range where the tax rate is practically 0. Thus, we reach a state where no one pays any income taxes and there is no redistribution. There is large inequality, and the wealth of individual voters grows differently, according to their income propensities.

Note that no income taxes implies no forceful misallocation, the main quantity of interest that we seek to minimize. This is in stark contrast to the case with equal votes, where just under half of all labour income is expropriated at every iteration. Under democracy, the cumulative expropriated funds scale as $O(t)$, while under meritocracy, with weights tied to taxes, it scales as $O(1)$. This does assume that the redistribution policy is fixed and that the tax rates cannot be regressive. Other models may yield different results. However, the distinction here is evident.

The two simulations above were not meant to be realistic. They were meant to be worst-case scenarios and to provide bounds on the quantities of interest. Average case analyses are much more complicated. Nonetheless, results suggest that

- Depending on the dynamics involved, weighted voting may or may not change the resulting equilibrium states,
- Compared to equal weights, weights proportional to contributions yields lower forceful misallocation of resources,
- Equal weights can lead to low inequality and high unfairness, while unequal weights can lead to high inequality and low unfairness.

Finally, a personal opinion which should be mentioned. I do not believe that giving more voting power to the highest contributors will hurt those really in need of help. If I had a weight of 0.51, being a de facto dictator in the votes, I would still donate to charities and help those in need. But I want to do it manually, not through the government. And if you think that weighted voting means the end of charity and compassion, answer me this: are people really cruel by heart, or are they just used to mindlessly delegating their altruistic attitudes to a mask-wearing, gun-pointing robber?