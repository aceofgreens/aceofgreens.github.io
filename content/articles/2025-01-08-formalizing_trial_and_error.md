---
Title: Formalizing Trial And Error
Date: 2025-01-08 07:00:00 +0200
Tags: rl
slug: formalizing_trial_and_error
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

Here the sum of rewards uses the same index $t$ because it is factored out from the innermost sum and there is no ambiguity. The same value multiplies all the innermost terms. This setup is the classic REINFORCE algorithm [1]. To train the algorithm, we roll-out a trajectory and update the policy weights as $\theta' = \theta + \eta \nabla_\theta J(\theta)$. The collected trajectory is discarded. No replay buffers are used. We can also roll-out a batch of trajectories and perform a batched update with them. But we cannot perform multiple sequential updates on the same trajectory (not yet).

Note that the REINFORCE algorithm simply formalizes the idea of "trial and error". The agent has to experience different rewards in order to get a sense of what works and the likelihood of which actions should be maximized. If the reward is the same everywhere, the agent doesn't learn because it does not learn to prioritize one action at the expense of another one. Same thing happens if the reward is zero - the agent does not learn. Thus, optimal policy learning is a *search* task. Unlike classification, regression, or other supervised tasks, here the agent requires variability in the reward in order to search more efficiently.

The problem with this basic algorithm is that its variance is too large. Since both $a_t | s_t$ and $s_{t+1} | s_t, a_t$ are random variables, the variance of $\tau$ can be huge and hence the updates $\nabla_\theta J(\theta)$ while unbiased, will be very inconsistent from iteration to iteration. To address this, we need to make a few modifications.

First, we don't need to have the full sum of rewards $\sum_{t=1} r_t$ at every single step. In reality, action $a_t$ only affects rewards $r_t, r_{t+1}, r_{t+2}, ...,$, not $r_1, ..., r_{t-1}$. Hence the log probability can be weighted by the "reward to go", $G_t = \sum_{j=t} r_j$. With this change the update becomes

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[\sum_{t=1} \nabla_\theta \log \pi_\theta(a_t | s_t) G_t \right] = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[\sum_{t=1} \nabla_\theta \log \pi_\theta(a_t | s_t) \sum_{j=t}^T r_j\right]
$$

This change improves credit assignment by weighing each log-prob with only the rewards that follow it. This reduces variance while still being unbiased. The underlying objective function optimized is the same. But the variance can be reduced even more.

The value of a state $s_t$ is defined as the total sum of discounted rewards, called *return*, collected from following the policy $\pi$ starting in this state. Likewise, the value of an action $a_t$ in a state $s_t$ is, similarly, the return from following $\pi$ after executing $a_t$ in $s_t$:

$$
\begin{align}
V^\pi(s_t) &= \mathbb{E}_{a_t, s_{t+1}, a_{t+1}, ... \sim \pi(\tau)} \sum_{j=t} \gamma^{j - t} r_{j} \\
Q^\pi(s_t, a_t) &= \mathbb{E}_{s_{t+1}, a_{t+1}, s_{t+2}, ... \sim \pi(\tau)} \sum_{j=t} \gamma^{j - t} r_{j}.
\end{align}
$$

The discounting factor $\gamma$ controls how myopic the agent is, i.e. how much it prefers rewards closer to the current timestep compared to farther into the future. A discount factor is needed to ensure finite returns in infinite-horizon settings. Naturally, we can replace the reward-to-go with $Q(s_t, a_t)$. If the estimate of $Q(s_t, a_t)$ is unbiased, the estimate of the gradients will also be unbiased.

We can also use the *advantage*, $A^\pi(s_t, a_t) = Q^\pi(s_t, a_t) - V^\pi(s_t)$. It quantifies how much better action $a_t$ is compared to the "average action" in $s_t$. Substituting the advantage into the gradient estimate significantly reduces its variance:

$$
\nabla_\theta J(\theta) = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[\sum_{t=1} \nabla_\theta \log \pi_\theta(a_t | s_t) A_t \right].
$$

This change naturally brings us to actor-critic methods. An actor $\pi_\theta$ selects actions, while a critic estimates a kind of value for each action. This value could be the reward to go $G_t$, or the Q-value $Q(s_t, a_t)$, or the advantage $A_t$. Since the critic, being a neural network, only approximates the true returns, the gradient estimates become a little biased but usually the faster learning from reduced variance is worth it.

There is another way to control the bias and variance. In a full Monte-Carlo setup we roll-out a trajectory, and then iterate backward to compute $\sum_{j=t}^T \gamma^{j-t} r_j$ for every timestep. We can also bootstrap the returns from future estimated returns. For example $Q(s_t, a_t) = r_t + \gamma V(s_{t+1})$ and $A(s_t, a_t) = r_t + \gamma V(s_{t+1}) - V(s_t)$. By calling the learned critic at a future state, we bootstrap the value of the current state. One can choose different setups, e.g $Q(s_t, a_t) = r_t + \gamma r_{t+1} + V(s_{t+2})$. This is a 2-step estimated return. The less rewards we accumulate, the more bias we introduce, but also the less variance in the gradients.

There is a smarter way to trade-off bias and variance when choosing the $n$-step returns. We can use a parameter $\lambda$ which interpolates between all possible $n$-step returns, of which there are infinitely many. This $\lambda$-return is simply an exponentially-weighted average of $n$-step returns with decay equal to $\lambda$. If $R_t^n$ is the $n$-step return, then

$$
R_t(\lambda) = (1 - \lambda)\sum_{n=1}^\infty \lambda^{n-1} R_t^n.
$$

Efficient ways to calculate this are possible by starting from the end of the roll-out and going backwards. If $\lambda=0$, we ge the standard single-step return. If $\lambda=1$, we get the full Monte Carlo return, effectively of infinitely many steps. Computing the advantage as $R_t(\lambda) - V(s_t)$ is called *generalized advantage estimation*.

Now, note that we still cannot perform multiple updates on the same collected trajectory because we wouldn't be optimizing the specific objective above. To alleviate this, we need to use importance sampling, stating that $\int p(x) f(x) dx = \int q(x) p(x)/q(x) f(x) dx$. In our case $q(\cdot)$ will be the old policy $\pi_{\theta}$ with which the trajectory was collected, and $p(\cdot)$ will be the current policy, $\pi_{\theta'}$, after possibly many updates on the same trajectory.

$$
\begin{align}
J(\theta')& = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[ \frac{\pi_{\theta'}(\tau)}{\pi_{\theta}(\tau)} \sum_{t=1}r_t \right] \\
\nabla_{\theta'} J(\theta') & = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[ \frac{\nabla_{\theta'} \pi_{\theta'}(\tau)}{\pi_\theta(\tau)} \sum_{t=1}r_t \right] = \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[ \frac{ \pi_{\theta'}(\tau)}{\pi_\theta(\tau)} \nabla_{\theta'} \log \pi_{\theta'}(\tau) \sum_{t=1}r_t \right] \\
&= \mathbb{E}_{\tau \sim \pi_\theta(\tau)} \left[ \Bigg(\frac{\prod_{t=1} \pi_{\theta'}(a_t | s_t)}{\prod_{t=1} \pi_{\theta}(a_t | s_t)} \Bigg) \left( \sum_{t=1} \nabla_{\theta'}\log \pi_{\theta'}(a_t | s_t) \right) \left( \sum_{t=1} r_t \right) \right]
\end{align}
$$

The more times we update on the same data, the more $\theta'$ becomes different from $\theta$, and hence the more the first term in the last equation diverges from 1. This could very easily lead to vanishing or exploding gradients. To address this, we need to keep the policies close to each other, i.e. $D_\text{KL}(\pi_{\theta'} || \pi_\theta) \le \delta$. This is the idea behind the Trust Region Policy Optimization (TRPO) algorithm [2]. There is a lot of math behind it, so we'll skip it, but the bottom line is that it improves stability by keeping the current policy sufficiently close to the old one.

Another method along the same idea of restricting how much the policy changes is Proximal Policy Optimization (PPO) [3]. Suppose $r_t(\theta') = \pi_{\theta'}(a_t | s_t) / \pi_\theta(a_t | s_t)$. PPO simply works by maximizing the minimum between $r_t(\theta)$ and a clipped version of it:

$$
L^{\text{CLIP}} = \mathbb{E}_t \left[ \min(r_t(\theta)A_t, \text{clip}(r_t(\theta), 1 - \epsilon, 1 + \epsilon)A_t \right].
$$

The loss function here is written only for a single transition. To understand this, consider a positive advantage equal to $1$, so that in principle the agent should increase the probability of the selected $a_t$. Suppose $\epsilon = 0.2$. If $r_t(\theta) = 5$, its clipped value is $1.2$ and the smaller between $5$ and $1.2$ is $1.2$. Thus, the value to maximize is $1.2$ instead of $5$, so this limits the magnitude of the update. If instead $r_t(\theta) = 0.5$, the value to maximize is $0.5$, as small updates are not penalized. If the advantage is $-1$, and $r_t(\theta) = 0.5$, then the objective value becomes $-0.8$ instead of $-0.5$, so this acts as a pessimistic lower-bound on the unclipped objective.

PPO is the default algorithm for policy gradients. There are some variations which are in use, like DD-PPO which allows for synchronized parallel data-collection on many devices, but overall the method has held up nicely. So now that we've explored the method, let's take a look at an important application - reinforcement learning from human feedback - the main technique for aligning LLMs so that they respond in more human-likable manner.

Suppose we have a LLM that has been pretrained on a large corpus using next-token prediction, and then finetuned on a smaller dataset of question-answer pairs, so that it knows how to format its responses. People can still have preferences over how the LLM should respond and we'll try to align the LLM to them. Here is how RLHF works.

Let the initial policy be the LLM after supervised fine-tuning (SFT), $\pi^{\text{SFT}}$. We select prompts $x$ and generate pairs of answers $(y_1, y_2) \sim \pi^{\text{SFT}}(y | x)$. Human reviewers then rank them by preference, denoted as $y_w \succ y_l | x$, where $y_w$ is the preferred response and $y_l$ the dispreferred one. Now, in principle, we can assume that there is some underlying reward model (the equivalent of a utility function in economics) $r^\ast$ which generates these preferences. Our goal is then to learn an approximation $r_\phi$ as close as possible to $r^\ast$. Note that we do not observe the true rewards $r^\ast(x, y_1)$ and $r^\ast(x, y2)$, only their pairwise comparisons. [Bradley-Terry](https://en.wikipedia.org/wiki/Bradley%E2%80%93Terry_model) is a famous model establishing how to work with such preferences.

It models the probability that $y_1$ is preferred as given by 

$$
p(y_1 \succ y_2 |x) = \frac{\exp\big(r^\ast(x, y_1)\big)}{\exp\big(r^\ast(x, y_1)\big) + \exp\big(r^\ast(x, y_2)\big)}.
$$

We will learn a parameterized reward model $r_\phi$ to approximate $r^\ast$. To do so, we view preference prediction as binary classification. The negative log-likelihood of the Bradley-Terry model directly becomes the loss function with which we can train $r_\phi$:

$$
\mathcal{L}_R(r_\phi, \mathcal{D}) = -\mathbb{E}_{(x, y_w, y_l) \sim \mathcal{D}} \Big[ \log \sigma\big(r_\phi(x, y_w) - r_\phi(x, y_l) \big) \Big].
$$

If the reward for the preferred response is much larger than the reward for the dispreffered one, then their differences is a positive large number, its sigmoid is 1, and the total loss after the log becomes 0. Otherwise, the sigmoid becomes close to 0, and the final loss is very large. So this loss function makes sense. Once we have the reward model, we formulate the RL loss as:

$$
\max_\theta \ \mathbb{E}_{x \sim \mathcal{D}, y \sim \pi_\theta(y | x)} \big[r_\phi(x, y)\big] - \beta D_\text{KL}\big(\pi_\theta(y | x)  \ \Vert \  \pi^\text{SFT}(y | x)\big).
$$

This encourages the model to maximize the reward while not deviating too much from the SFT policy. It also prevents mode-collapse to single high-reward answers. Of course this is very difficult to optimize, so instead we redefine the rewards as follows, and maximize using PPO: 

$$
r(x, y) = r_\phi(x, y) - \beta\big( \log \pi_\theta(y | x) - \log \pi^\text{SFT}(y|x)\big).
$$

This setup is too complicated. We can simplify as follows, though we'll skip the derivations. First, one can prove that the policy solving the optimization problem above with the KL has the form:

$$
\pi_r(y | x) = \frac{1}{Z(x)}\pi^\text{SFT}(y | x) \exp\big(\frac{1}{\beta}r(x, y)\big).
$$

From here we can take the log and solve for $r(x, y)$:

$$ 
r(x, y) = \beta\log\frac{\pi_r(y | x)}{\pi^\text{SFT}(y|x)} + \beta\log Z(x).
$$

This is very convenient because in the Bradley-Terry model the probability that one sample is preferred only depends on the differences of rewards, not their actual values. We can then construct a maximum likelihood objective for a parametrized policy $\pi_\theta$:

$$
\mathcal{L}_\text{DPO}(\pi_\theta; \pi^\text{SFT}) = -\mathbb{E}_{x, y_w, y_l \sim \mathcal{D}} \left[ \log \sigma \Bigg( \beta \log \frac{\pi_\theta(y_w |x)}{\pi^\text{SFT}(y_w|x)} - \beta\log \frac{\pi_\theta(y_l | x)}{\pi^\text{SFT}(y_l | x)} \Bigg) \right]
$$

This method is called Direct Preference Optimization (DPO) and is very powerful. Can you find the reward model $r_\phi$ in it? Exactly, it's not there. In fact, the equation shows that we can finetune the LLM policy directly on human preferences, without needing to train a reward model beforehand and without needing to do RL. By finetuning with this loss the LLM learns the underlying reward function implicitly, which saves us a lot of trouble. Neat.

### References

[1] Sutton, Richard S., and Andrew G. Barto. Reinforcement learning: An introduction. MIT press, 2018.   
[2] Schulman, John, et al. [Trust Region Policy Optimization.](https://proceedings.mlr.press/v37/schulman15.html) Proceedings of the 32nd International Conference on Machine Learning, vol. 37, 2015, pp. 1889-1897.   
[3] Schulman, John, et al. [Proximal policy optimization algorithms.](https://arxiv.org/abs/1707.06347) arXiv preprint 1707.06347 (2017).   
[4] Wijmans, Erik, et al. [Dd-PPO: Learning near-perfect pointgoal navigators from 2.5 billion frames.](https://arxiv.org/abs/1911.00357) arXiv preprint arXiv:1911.00357 (2019).   
[5] Ouyang, Long, et al. [Training language models to follow instructions with human feedback.](https://proceedings.neurips.cc/paper_files/paper/2022/hash/b1efde53be364a73914f58805a001731-Abstract-Conference.html) Advances in neural information processing systems 35 (2022): 27730-27744.   
[6] Rafailov, Rafael, et al. [Direct preference optimization: Your language model is secretly a reward model.](https://arxiv.org/abs/2305.18290) Advances in Neural Information Processing Systems 36 (2024).