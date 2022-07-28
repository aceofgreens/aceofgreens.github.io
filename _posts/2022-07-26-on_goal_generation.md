---
layout: post
title: On Goal Generation
date: 2022-07-26 16:00:00 +0200
tags: [ai, ultra-rationalism, rl]
---

Previously, I've [tried to convince you](https://aceofgreens.github.io/2022/05/19/why_do_beetles_love_life.html) that the utter desire to live at any cost is not something fundamental or designed with any global purpose. It is a purely random quality which has serendipitously proved useful in increasing our fitness in the environment. As a result those who have the will to live survive, and the others do not. There was a time when the probability of life suceeding has been marginal, but luckily this time is long gone. The qualities that aid life have become stable and ubiquitous, and life flourishes. Given that, we still don't know how exactly it is that humans give meaning to their existence. Are there any observable patterns that can shine a light on this conundrum? Can we solve the plight of how we attribute meaning?

I will be borrowing concepts from reinforcement learning (RL) to illustrate my points. RL offers a simplified framework for agents acting purposefuly in an uncertain environment and while by simplified I mean *very simplified*, I find that such a schematic has incredible value - first because it keeps the complexity of the topic manageable, and secondly because it keeps the discussion on a sufficiently high level, above the nitty-gritty noisy details.

In most RL settings, the agent has global purpose. The task is phrased in the context of a [Markov Decision Process](https://en.wikipedia.org/wiki/Markov_decision_process) (MDP). The agent observes the current state of the world $s_t$ and selects an action $a_t$. After executing that action, the environment responds by returning a new state $s_{t+1}$, i.e. the agent observes the consequences of his actions. Importantly, in this setting, the environment returns also a reward $r_t$ depending on the state $s_t$ and the action $a_t$. The goal of the agent is to act in such a way that on average any trajectory (sequence of actions) yields maximum rewards.
<figure>
    <img class='small_img' src="/resources/mdp.svg" alt="The MDP" width="1200">
    <figcaption>Figure 1: The standard MDP setting.</figcaption>
</figure>
Notice that in this setting the reward function - how the rewards depend on the agent's actions - is predefined. The reward is typically engineered to be positive in those states which are desirable and negative in those which are bad. The agent will try to go to those states yielding high rewards and as a result, we can think of reward functions as goals. Any reward function defines a goal - a preference over states of the world. The relationship between reward functions and goals is not injective however. There are many reward functions which correspond to the same goal. In fact, the [inverse problem](https://en.wikipedia.org/wiki/Reinforcement_learning#Inverse_reinforcement_learning) of learning a reward function from optimal trajectories is ill-defined.

Since it may be hard to solve the MDP task using only the task-based reward $r_t$, it has become common to add a second reward component which comes from the agent itself. This leads to a setting where we have both task-based rewards and intrinsic rewards $\hat{r}_t$. These rewards could incentivize curiosity (by choosing actions whose outcome is more uncertain), safety (by choosing actions whose outcome is less likely to be bad), or even predetermined behaviour.
<figure>
    <img class='small_img' src="/resources/intrinsic_rewards.svg" alt="Intrinsic rewards" width="1200">
    <figcaption>Figure 2: An intrinsically-motivated agent in a MDP setting.</figcaption>
</figure>
The most important intrinsic reward is what I call the **curiosity itch**. It constitues those rewards encouraging exploration, curiosity, and creativity. The curiosity itch is important because
it is only through tinkering and fiddling around, that we explore more of the state space. We live in a universe where positive rewards are sparse, and we have to explore to find the best course of action. Theory is important, sure, but coming up with a theory is not an act of interaction with the environment. It does not lead to rewards. Scientific theory is just a model of the dynamics of the MDP that we call life.

The RL setting most close to us is actually the autotelic one, where there are only intrinsic, endogenously-generated rewards. There are no task-based performance signals here, just raw curiosity and inner drive, depending on the agent itself. This is the setting of our world. The question "What should I aim for in the next 10 years?" is ambiguous because no one can make that decision for you. There isn't any intelligent designer (apart from evolution) who has engineered us to prefer peace over war, or tranquility over commotion.
<figure>
    <img class='small_img' src="/resources/autotelic.svg" alt="Autotelic setting" width="1200">
    <figcaption>Figure 3: The autotelic setting with only intrinsic rewards.</figcaption>
</figure>

So what is that reward function? It surely has a curiosity component, a biochemical component to regulate our biological needs, and a psychological component whose desires aim to keep our mental models in tact.
But I bet you that none of these are consciously chosen by us. I expect that the human's reward system, our [mesocorticolimbic circuit](https://en.wikipedia.org/wiki/Reward_system) is just another evolutionary aspect guiding our adaptation. The rewards it generates are biochemical and we cannot change them, at least not naturally. The autotelic agent is still a puppet whose preferences over world states have evolved through a computational process.

Before moving on, let's explore one particular concept from Douglas Hofstadter's almighty book [Gödel, Escher, Bach](https://en.wikipedia.org/wiki/G%C3%B6del,_Escher,_Bach). While I disagree with some of his ideas, I believe this one is spot on and fits nicely in this discussion. Let's explore the $pq$-system.

The $pq$-system consists of theorems and axioms. Both of these are made up entirely out of the symbols $p$, $q$ and $-$ (a hyphen). An axiom is any combination of these symbols such that $x p - q x-$, where $x$ and $y$ consist of only hyphens. So, for example, all of the following strings belong to the $pq$-system as axioms.

$$
\begin{aligned}
& - p - q - - \\
& - - p - q - - - \\
& - - - p - q - - - - \\
& - - - - p - q - - - - - \\
\end{aligned}
$$

Apart from axioms, the $pq$-system also has a rule for defining theorems. Theorems are strings for which we can prove they belong to the system. The rule for defining new theorems is as follows: if $x$, $y$, and $z$ are strings containing hyphens only, and if $x p y q z$ is a theorem, then $x p y - q z -$ is also a theorem. So, for example, if

$$
--p--q-----
$$

is a theorem, then by the theorem production rule, 

$$
--p---q------
$$

is also a theorem. The central question of the $pq$-system is to determine whether any given string is a theorem. For example, is $- p q - q - $ a theorem? No, because starting from the axiomatic strings, even if we apply the theorem production rule as many times as we want, the resulting string will never be $- p q - q - $. On the other hand, is $ - - p - - - q - - - - - $ a theorem? Yes, because starting from the axiom $ - - p - q - - - $ and applying the production rule 2 times, we reach the required string.

Can you figure out a way to easily determine which strings are theorems? Have you spotted the regularity in the form of the theorems? As it turns out, a string is in the $pq$-system if it represents a valid addition statement. $ - p - - q - - -$ is in the system, because we can count the number of hyphens and reach $1 + 2 = 3$. The $p$ stands for plus, and the $q$ for equals. The theorems simply resemble addition.

In reality, it is not that the $pq$-system really performs addition, it's just that we have found a strong similarity between it and addition. We call this similarity meaning. Attaching meaning to an object means that we have found an isomorphism between the properties of the object and some of our previously known knowledge. This allows us to interpret the new object in the context of our previous knowledge.

With humans, I like to think that meaning and rewards are, likewise, closely related. Since rewards are sparse, it is not often that we find our actions and their results meaningful. I believe that meaning arises when we consider how our actions in the current state will increase or decrease the likelihood of obtaining rewards. Ultimately, we all have a mental model of past state-action-reward trajectories from which we learn. Our current actions become meaningful only when we find an isomorphism between the perceived effect of these actions in terms of reward collection and the past trajectories of collected state-action-reward transitions. In other words, I believe that the meaning we attribute to actions is ultimately tied to the biochemical rewards on which we depend.






<!-- The process of assigning rewards to state-action pairs is called deriving a meaning. Actions which lead to rewards (positive or negative) are meaningful. What gives meaning is an isomorphism between your mental model and the observables from the environment.

What are the rewards - psychosomatic, 
association. -->

<!-- Main ideas: 
Meaning as semantics (operational)
psychosomatic rewards
Control through sensors
Association between higher order states of the world
 -->