---
Title: Basic Policy Gradients
Date: 2025-01-08 07:00:00 +0200
Tags: rl
slug: basic_policy_gradients
---

The performance of a predictor trained using supervised learning is bounded by the quality of the data. The performance of a policy trained using reinforcement learning (RL), on the other hand, is practically unbounded. Thus, RL has the potential of reaching superhuman performance in multiple domains. Yet, the fundamental idea of RL is quite primitive and intuitive - just reinforce those behaviours that work and penalize those that don't, this being the very very basic premise of policy gradient methods. Let's explore them a bit.

The policy is $\pi_\theta$ and in each state $s_t$ selects an action $a_t$ to execute. We can sample a trajectory $\tau$ from it by performing a roll-out according to the policy, $\tau \sim \pi_\theta(\tau)$. Here the trajectory is defined as $s_1, a_1, s_2, a_2, ..., s_T, a_T$. The probability of the trajectory is given by the sequential multiplicative composition of the policy $\pi_\theta(a_t | s_t)$ and the environment dynamics $p(s_{t+1} | s_t, a_t)$, i.e. $\pi_\theta(\tau) = p(s_1) \prod_{t=1} \pi_\theta(a_t | s_t) p(s_{t+1} | s_t, a_t)$. The goal of the agent is to obtain high rewards *on average*. Thus we have to maximize the sum of rewards on the average trajectory:

$$
\max_\theta \ J = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[\sum_{t} r_t \right].
$$

Here for simplicity we assume $r_t$ is a deterministic function returning the reward from taking action $a_t$ in state $s_t$, i.e. $r_t := r(s_t, a_t)$. If the reward is stochastic, we'd have to take the expectation over its distribution too. How does the reward depend on the policy weights $\theta$? In general, if the reward function is differentiable, then the gradient $\partial r_t / \partial a_t$ will be available from the environment. These can then be comined with $\partial a_t / \partial \theta$ to optimize the policy directly. This is called [analytic policy gradients](https://aceofgreens.github.io/analytic_policy_gradients.html) and is usually very efficient. The idea is quite straightforward: we use gradient descent to update the policy in a way that directly maximizes the rewards of the average rolled-out trajectory. Implementation is a bit tricky because it may require detaching the state in the reward calculation, i.e. $r_t = r(\text{sg}[s_t], a_t)$.

If the environment is not differentiable it is common to treat it like a black box. The expectation over the executed trajectory can be approximated using a finite sample of $N$ trajectories, where we assume that the individual policy roll-outs are i.i.d:

$$
\begin{equation}
\max_\theta \ J = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[\sum_{t} r_t \right] = \int \pi_\theta(\tau) \Big(\sum_{t=1}r_t^\tau \Big) d\tau \approx \frac{1}{N}\sum_{i=1}^N \Big(\sum_{t=1} r_t^i\Big).
\end{equation}
$$

Here $\tau$ is a sampled trajectory, of which there are $N$. Both $r_t^i$ and $r_t^\tau$ indicate the $t$-th reward in a given trajectory. The gradient of the loss function, $\nabla_\theta J(\theta)$, is given by

$$
\begin{align}
\nabla_\theta J(\theta) &= \int \nabla_\theta \pi_\theta(\tau) \Big(\sum_{t=1} r_t^\tau \Big) d\tau \\
&= \int \pi_\theta(\tau) \nabla_\theta \log \pi_\theta(\tau) \Big(\sum_{t=1} r_t^\tau \Big) d\tau\\
&= \mathbb{E}_{\tau \sim \pi_\theta(\tau)}\left[ \nabla_\theta \log \pi_\theta(\tau) \Big(\sum_{t=1} r_t \Big)\right].
\end{align}
$$

The last equation comes from the fact that $\nabla_\theta \log \pi_\theta(\tau) = \nabla_\theta \pi_\theta(\tau) / \pi_\theta(\tau)$. Now, what is the gradient of the log probability of a given trajectory? Things simplify as follows:

$$
\begin{align}
\nabla_\theta \log \pi_\theta(\tau) &= \nabla_\theta \left[ \log \Big(p(s_1)\prod_{t=1}^T \pi_\theta(a_t | s_t) p(s_{t+1}|s_t, a_t) \Big) \right] \\
&= \nabla_\theta \left[ \log p(s_1) + \sum_{t=1}^T \log \Big(\pi_\theta(a_t | s_t) p(s_{t+1}|s_t, a_t) \Big) \right] \\
&= \sum_{t=1}^T \nabla_\theta \log \pi_\theta(a_t | s_t)
\end{align}
$$

Thus, we see that to update the policy, one only needs to compute the gradients of the log probability of the selected actions. This is natural, as the agent does not control the transition probabilities of the underlying MDP,

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[ \sum_{t=1} \nabla_\theta \log \pi_\theta(a_t | s_t) \Big( \sum_{t=1}r_{t} \Big) \right] \approx  \frac{1}{N} \sum_{i=1}^N \sum_{t=1} \nabla_\theta \log \pi_\theta(a_t^i | s_t^i) \Big( \sum_{t=1}r_{t}^i \Big).
$$

Here the sum of rewards uses the same index $t$ because it is factored out from the innermost sum and there is no ambiguity. The same value multiplies all the innermost terms. This setup is the classic REINFORCE algorithm. To train the algorithm, we roll-out a trajectory and update the policy weights as $\theta' = \theta + \eta \nabla_\theta J(\theta)$. The collected trajectory is discarded. No replay buffers are used. We can also roll-out a batch of trajectories and perform a batched update with them. But we cannot perform multiple sequential updates on the same trajectory (not yet).

Note that the REINFORCE algorithm simply formalizes the idea of "trial and error". The agent has to experience different rewards in order to get a sense of what works and the likelihood of which actions should be maximized. If the reward is the same everywhere, the agent doesn't learn because it does not learn to prioritize one action at the expense of another one. Same thing happens if the reward is zero - the agent does not learn. Thus, optimal policy learning is a *search* task. Unlike classification, regression, or other supervised tasks, here the agent requires variability in the reward in order to search more efficiently.
