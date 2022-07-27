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

Since it may be hard to solve the MDP task using only the task-based reward $r_t$, it has become common to add a second reward component which comes from the agent itself. This leads to a setting where we have both task-based rewards but also intrinsic rewards $\hat{r}_t$. These rewards could incentivize curiosity (by choosing actions whose outcome is more uncertain), safety (by choosing actions whose outcome is less likely to be bad), or even predetermined behaviour.
<figure>
    <img class='small_img' src="/resources/intrinsic_rewards.svg" alt="Intrinsic rewards" width="1200">
    <figcaption>Figure 2: An intrinsically-motivated agent in a MDP setting.</figcaption>
</figure>
The most important intrinsic reward is what I call the **curiosity itch**. It constitues those rewards encouraging exploration, curiosity, and creativity. The curiosity itch is important because
it is only through tinkering and fiddling around, that we explore more of the state space. We live in a universe where positive rewards are sparse, and we have to explore to find the best course of action. Theory is important, sure, but coming up with a theory is not an act of interaction with the environment. It does not lead to rewards. Scientific theory is just a model of the dynamics of the MDP that we call life.

The RL setting most close to us is actually the autotelic one, where there are only intrinsic, endogenously-generated rewards. There are no task-based performance signals here just raw curiosity and inner drive, depending on the agent itself. This is the setting of our world. The question "What should I aim for in the next 10 years?" is ambiguous because no one can make that decision for you. There isn't any intelligent designer (apart from evolution) who has engineered us to prefer peace over war, or tranquility over commotion.
<figure>
    <img class='small_img' src="/resources/autotelic.svg" alt="Autotelic setting" width="1200">
    <figcaption>Figure 3: The autotelic setting with only intrinsic rewards.</figcaption>
</figure>

So what is that reward function? It surely has a curiosity component, a biochemical component to regulate our biological needs, and a psychological component whose desires aim to keep our mental models in tact.
But I bet you that none of these are consciously chosen by us. I expect that the human's reward system, our [mesocorticolimbic circuit](https://en.wikipedia.org/wiki/Reward_system) is just another evolutionary aspect guiding our adaptation. The rewards it generates are biochemical and we cannot change them, at least not naturally. The autotelic agent is still a simple autonomous puppet whose preferences over world states have evolved through a computational process.

<!-- Main ideas: 
What it means to be autotelic
meaning as an isomorphism
Meaning as semantics (operational)
psychosomatic rewards
Control through sensors
Association between higher order states of the world
The Curiosity Itch
 -->