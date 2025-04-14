---
Title: Value-Based Methods
Date: 2025-02-11 07:00:00 +0200
Tags: rl
slug: value_based_methods
---

This post is a brief summary of the different classes of value-based RL methods. Personally, I find this topic incredibly rewarding in terms of its ability to provide precious deep intuition about how the RL algorithm landscape is spread out. Fundamental concepts like on-policy, off-policy, bootstrapping, and many others, all stem from these simple settings.

Consider a Markov decision process (MDP) $(\mathcal{S}, \mathcal{A}, \mathcal{P}, \mathcal{R}, \gamma)$ where $\mathcal{S}$ are the states, $\mathcal{A}$ the actions, $\mathcal{P}$ the transition probabilities, $\mathcal{R}$ the rewards and $\gamma$ is the discount rate. To most clearly understand how different algorithmic aspects are motivated by different problem settings, we'll only look at the setting where both the states $\mathcal{S}$ and actions $\mathcal{A}$ are discrete. Supposing also that there are not too many of them, it becomes possible to *enumerate* the state-action pairs. This is called the *tabular* setting.

**Discrete state-action pairs**. In the tabular setting you don't need a neural network to predict the values of states and actions. Instead, you can simply instantiate a big table of Q-values and periodically update them as you are improving the policy. Thus, deep RL is only needed when either the state space is continuous or it is discrete but too large to represent the Q-values as a table. Many board games have combinatorially exploding state spaces and easily fit these settings. In those cases a neural network can effectively compress a huge number of state-action values into a fixed number of weights.

**Basic definitions**. Assume experience traces come in the form of $(s_0, a_0, r_1, s_1, a_1, r_2, ...)$. We distinguish between the random variables $(S_t, A_t, R_{t+1})$ and their realizations $(s_t, a_t, r_{t+1})$. Using standard notation, the discounted sum of rewards is $G_t = \sum_{k=t+1}^T \gamma^{k-t-1}R_k$, where $T$ can be arbitrarily far into the future and $R_k$ is the random variable representing the reward at step $k$. Naturally, the return is a random variable with a very complicated distribution. The value function assigns a value to a state and is defined as

$$
v_\pi(s) = \mathbb{E}_{\pi} \left[ G_t | S_t = s \right] = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} | S_t = s\right], \ \forall s \in \mathcal{S}.
$$

Likewise, the state-action value function is similar, it assigns a value to individual actions:

$$
q_\pi(s, a) = \mathbb{E}_{\pi} \left[ G_t | S_t = s , A_t = a\right] = \mathbb{E}_\pi \left[ \sum_{k=0}^\infty \gamma^k R_{t+k+1} | S_t = s, A_t=a \right].
$$

These relationships are recursive. The Bellman equations express the value of the current state $s$ using the value of the future state $s'$. This holds for any policy $\pi$:

$$
\begin{align}
v_\pi(s) &= \mathbb{E}_\pi\left[G_t | S_t = s \right] = \mathbb{E}_\pi \left[ R_{t+1} + \gamma G_{t+1} | S_t = s \right] \\ 
&= \sum_{a} \pi(a|s) \sum_{s', r} p(s', r | s, a) \Big[r + \gamma v_\pi(s') \Big], \\
q_\pi(s, a) &= \mathbb{E}_\pi\left[G_t | S_t = s, A_t = a \right] = \mathbb{E}_\pi \left[ R_{t+1} + \gamma G_{t+1} | S_t = s, A_t = a \right] \\ 
&= \sum_{s', r} p(s', r | s, a) \Big[r + \gamma v_\pi(s') \Big] = \sum_{s', r} p(s', r | s, a) \Big[r + \gamma \sum_{a'}\pi(a'|s')q_\pi(s', a') \Big].
\end{align}
$$

Policies are functions that assign actions to states, $\pi: \mathcal{S} \rightarrow \mathcal{A}$. Value functions define a partial ordering over policies. A policy $\pi$ is deemed better than policy $\pi'$ if and only if the value of state $s$ obtained from policy $\pi$ is greater or equal than the value of state $s$ from policy $\pi'$, for all states:

$$
\pi \ge \pi' \ \Longleftrightarrow \ v_\pi(s) \ge v_{\pi'}(s), \ \forall s \in \mathcal{S}.
$$

In that sense, there is an optimal policy $\pi_\ast$ whose values $v_\ast$ are greater than the values obtained from any other policy. There is always a unique optimal state-value function $v_\ast$ and action-value function $q_\ast$, but there may be multiple optimal policies $\pi_\ast$ that attain them.

An optimal policy also has a recursive nature. To see this, consider that the value $v_\ast(s)$ must be the highest Q-value at that state, $v_\ast(s) = \max_a q_\ast(s, a)$, otherwise the policy will not be optimal. Similarly, the optimal Q-value at $(s, a)$ requires that we take the best action from the next state $s'$. These are called the Bellman *optimality* equations and they play a key role in many algorithms:

$$
\begin{align}
v_\ast(s) &= \max_a q_\ast(s, a) = \max_a \sum_{s', r} p(s', r | s, a) \Big[ r + \gamma v_\ast(s') \Big] \\
q_\ast(s, a) &= \sum_{s', r} p(s', r | s, a) \left[ r + \gamma \max_{a'} q_\ast(s', a') \right].
\end{align}
$$

A very convenient way to represent these equations is through backup diagrams, as shown in Fig. 1. States are shown as circles, while actions as squares. Arcs show max-aggregation operations.

<figure>
    <img class='img' src="/images/bellman_optimality_state2.svg" alt="Bellman optimality state" width="1200">
    <figcaption> Figure 1: Backup diagrams for the Bellman optimality equations.</figcaption>
</figure>

**Dynamic programming**. Consider the case when the environment dynamics $p(s', r | s, a)$ are known. In that case there is no need to do *learning*, we can evaluate and optimize policies directly. Specifically, we can just run multiple sweeps across all the states and use the known dynamics to estimate the value functions for the current policy $\pi$. The process of obtaining $V_\pi(\cdot)$ from $\pi$ is called *policy evaluation* and looks something like the following:

1. Instantiate $V(s)$ arbitrarily
2. For every state $s$, set $V(s) \leftarrow \sum_a \pi(a|s) \sum_{s', r}p(s', r | s, a)[r + \gamma V(s')]$.
3. Repeat step 2. until a stopping criterion is met.

**Bootstrapping**. Dynamic programming uses what's called bootstrapping - updating the value of the current state using an estimate of the value of a neighboring state. In that sense, we're pulling ourselves by our own bootstraps. It also uses full-width backups, meaning that we are using the known dynamics to aggregate information about all possible next states $s'$ when updating $s$.

Policy evaluation could be implemented in a synchronous manner where we update the values of all states at the same time. This requires having two copies of the current value function. It can also be implemented in an asynchronous way, where the values of different states are updated in different order in-place. All it matters to ensure the eventual convergence is that over time all states continue to be selected for updates. 

To improve the policy we need to use $V_\pi(\cdot)$ to obtain a new $\pi$. A simple way to do it is to make the policy greedy with respect to the value function in every state, which is a guaranteed improvement: $\pi(a | s) = \text{arg}\max_a \sum_{s', r}p(s', r | s, a)[r + \gamma V(s')]$. Once we improve the policy we can re-evaluate it and improve it again, and again, and again. This *policy iteration* approach of repeatedly evaluating the policy and improving it is common to pretty much all value-based methods. It also allows us to be flexible in terms of how many sweeps we use to evaluate the policy before we improve it. The special case of using a single sweep is called value iteration.

<figure>
    <img class='img' src="/images/policy_evaluation_dyn_prog2.svg" alt="Bellman optimality state" width="1200">
    <figcaption> Figure 2: Backup diagrams for the policy evaluation and Q-policy iteration. Here we simply aggregate neighboring values according to their probabilities. The left diagram finds $v_\pi(s)$, the right one finds $q_\pi(s, a)$.</figcaption>
</figure>

**Monte Carlo**. Let's now depart from the assumption of known dynamics. The class of techniques which estimate an optimal policy without knowing or learning the dynamics is called *model-free* methods. Crucially, if you don't know the probabilities $p(s' | s, a)$ you need to sample the state space and this is the biggest difference compared to dynamic programming - the agent will now *learn from experience*. It will play out different policies, collecting data, and then use the collected data to update its value estimates.

The need to collect different trajectories brings out also the need to explore. This stems from the fact that rewards provide an inherently evaluative feedback to the agent, they tell it whether some action is good or bad, without telling it which action is better/worse. Contrast this to supervised learning, where due to the presence of gradients, there is instructive feedback precisely guiding the agent in how to change its predictions.

So, the idea behind Monte Carlo methods is that the agent will rollout entire trajectories, from start to finish, and then will estimate values for the traversed states based on the collected rewards. Thus, instead of expected returns, it will estimate empirical returns as follows:

1. Initialize $V(s)$ arbitrarily and $\text{Returns}(s)$ an empty list for all $s$.
2. Collect a number of traces $\tau$.
3. For every trace and every state $s$ appearing in it, append its return $G_t$ to $\text{Returns}(s)$.
4. Set $V(s) \leftarrow \text{average}(\text{Returns}(s))$, for all states $s$.

This simple algorithm evaluates $v_\pi(s)$. We can use the same procedure to evaluate also $q_\pi(s, a)$. It can be implemented in an online (update policy after every episode) or batched manner. It does not use bootstrapping, because we're updating the value function using only the true collected rewards, not estimates of them. Because of that it has high variance, but is unbiased. It also requires that episodes have finite length.

<figure>
    <img class='small_img' src="/images/mc_trace2.svg" alt="Bellman optimality state" width="1200">
    <figcaption> Figure 3: Backup diagrams for Monte Carlo policy iteration. The agent performs sample trace backups - rolls out a policy until a terminal state, indicated with a T, and estimates mean empirical returns. The dashed arrows show that rewards are obtained from the corresponding transitions.    </figcaption>
</figure>

What about MC control? We follow the broad approach of repeatedly evaluating the policy and improving it. Policy improvement consists of making the policy greedy with respect to the Q-values, $\pi(s) = \text{arg}\max_a q(s,a)$. We use the Q-values because they do not require knowing the environment dynamics. However, to guarantee convergence we need to make sure that given infinitely many episodes, all states $s$ are visited infinitely many times. One way to achieve this is with *exploring starts* - by starting each episode from a different state we would ensure that all possible states are eventually experienced. This is unrealistic though, and hence it's more typical for the agent to purposefully explore on its own, by using soft policies, where there is a $\epsilon$ chance of taking a random action. This ensures that any $(s, a)$ pair has a nonzero probability of occurring.

All learning control methods face a dilemma: they seek to learn action values conditional on subsequent optimal behavior, but they need to behave non-optimally in order to explore all actions (to find the optimal actions). This leads to on-policy and off-policy learning. On-policy methods compromise in that they learn action values not for the optimal policy, but for a near-optimal policy that still explores. Off-policy methods on the other hand use two policies - a *behaviour policy* for exploring, and a *target policy* that we want to actually optimize.

On-policy MC control works by having an $\epsilon$-greedy policy collecting trajectories. Then, as we're collecting returns and updating the Q-values, we update the policy as 

$$
\pi(a | S_t) \leftarrow \begin{cases}
1 - \epsilon + \epsilon/|\mathcal{A}(S_t) |, \ \ &\text{if } a = \text{arg}\max_a Q(S_t, a) \\
\epsilon /  |\mathcal{A}(S_t) |, \ \ &\text{otherwise.}\\
\end{cases}
$$

The off-policy MC control setup is more complicated and our discussion will be necessarily brief. It involves the target policy $\pi$ and the behaviour policy $b$ and corrects the returns $G_t$ according to the importance sampling ratio $\prod_{k=t}^{T-1} \frac{\pi(A_k | S_k)}{b(A_k | S_k)}$. There are many ways to do it: ordinary importance sampling simply averages the weighted returns from many $(s, a)$ occurrences. It is unbiased but can have unbounded variance. On the other hand, weighted importance sampling takes the weighted mean of the returns, weighted by their importance ratios, which has bias (converging asymptotically to zero) and drammatically lower variance.

**Temporal difference learning**. The most popular type of learning setup is actually temporal difference (TD) learning. Unlike MC, which performs sample trace backups, TD performs sample transition backups. Hence we don't need to wait for the episode to end, we just bootstrap the value of the current state from the value of the next experienced state. Since initially the value function is incorrect, TD produces biased estimates, yet the variance is much smaller than that of the MC methods, which usually translates to faster learning.

TD algorithms work by collecting episodes and then updating the value functions using individual transitions from the episodes. $V(s)$ is updated by moving $V(S_t)$ towards $R_{t+1} + \gamma V(S_{t+1})$ and similarly for $Q(S_t, A_t)$. If the learning rate $\alpha$ is decreasing properly, convergence is guaranteed: 

$$
\begin{align}
V(S_t) &\leftarrow V(S_t) + \alpha\big(R_{t+1} + \gamma V(S_{t+1}) - V(S_t)\big) \\
Q(S_t, A_t) &\leftarrow V(S_t) + \alpha\big(R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t)\big) \\
\end{align}
$$

Backup diagrams for evaluating $v_\pi(s)$ and $q_\pi(s, a)$ are shown in Fig. 4. The main benefit compared to MC is that TD allows us to learn in infinite episodes, for example if the task is continuing from before. It also allows us to naturally learn in an online manner, as we don't have to wait until the episode finishes.

<figure>
    <img class='img' src="/images/td_trace2.svg" alt="Bellman optimality state" width="1200">
    <figcaption> Figure 4: Backup diagrams for TD algorithms. Left is policy evaluation. Middle is Q-policy iteration as used in Sarsa. Right is the TD Bellman optimality equation, as used in Q-learning. </figcaption>
</figure>

**Sarsa**. When it comes to control, the on-policy TD algorithm is called Sarsa. The name comes from the quintuple $(s, a, r, s', a')$. We initialize the Q-values arbitrarily and set the initial policy to be $\epsilon$-greedy with respect to the Q-values. We collect transitions using that policy and update the Q-values according to the on-policy transitions. $Q(s, a)$ is updated toward $r + \gamma Q(s', a')$, with $a \sim \pi(s')$. The policy is improved by making it $\epsilon$-greedy with respect to the new, updated Q-values. Since both the transitions collected and the Bellman targets are coming from the $\epsilon$-greedy policy, this is an on-policy method.

**Q-learning**. The off-policy TD control algorithm is the classic Q-learning, where everything is the same except that we update the Q-values as

$$
Q(S, A) \leftarrow Q(S, A) + \alpha \left[ R + \gamma \max_a Q(S', a) - Q(S, A)\right].
$$

Why is this off-policy? Because the behaviour policy collecting the data is $\epsilon$-greedy wrt Q, while the Bellman targets with which the policy is updated are actually greedy wrt Q. This is the mismatch. The Bellman target follows the form in the corresponding optimality equation.

Note that Q-learning suffers from a selection bias. Because usually the estimated Q-values are noisy, and because we always select the best one, it may happen that because of noise, a poor action is selected more often than it should. This may lead to overly optimistic Q-values and may hurt learning. The solution is to have two sets of Q-values, $Q_1$ and $Q_2$, one for selecting the action and one for evaluating it. The value used in the Bellman target is $Q_2(s, \text{arg}\max_a Q_1(s, a))$.

Another thing is that for all $\epsilon$-greedy policies the initial starting Q-values greatly affect exploration. If the true range of Q-values in a given state is $[0, 1]$, but we initialize them in the range $[10, 11]$, then all of actions will be tried out sooner rather than later because of the $\epsilon$-greedy policy. On the other hand, if one of the Q-values is initialized to $-1$, then it's likely that it will rarely be picked, only ever by chance. This particular trick to encourage/discourage exploration is called optimistic/pessimistic initialization. Similarly, if we have some kind of uncertainty signal like prediction error, or information gain, and we use it to select for execution those actions with the highest such signal, this is called *optimism in the face of uncertainty*.

**Multistep bootstrapping**. Finally, one should recognize that a TD target like $r + \gamma V(s')$ bootstraps from only one step ahead. But it may use more than that, e.g. $r + \gamma r' + \gamma^2 r'' + \gamma^3 V(s''')$. All on-policy and off-policy methods could be adapted to work in this manner. This kind of multistep bootstrapping trades off increased variance with decreased bias. The more we rely on bootstrapping, the more biased is the estimate.

This completes our basic overview of value-based model-free tabular RL methods. The two main dimensions of interest are depth and width of the update. Depth refers to how much they bootstrap. Width refers to whether they rely on sample updates (from a trajectory) or expected updates (from a distribution of possible trajectories). TD methods have small depth (single transition) and small width (sampling). MC methods have large depth (entire traces) and small width (sampling). Dynamic programming has small depth and large width (one-step expected updates). Exhaustive search has large depth and width. 