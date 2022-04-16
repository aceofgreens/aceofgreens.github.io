---
layout: post
title:  Thoughts After IMOL
date: 2022-04-08 16:00:00 +0200
tags: rl
---

I recently attended the [Fifth International Workshop on Intrinsically Motivated Open-ended Learning](https://2022.imol-conf.org/) (IMOL 2022) in Tübingen, Germany. It was a very nice event, with interesting presentations and discussions all around. This post aims to summarize the highlights and provide some thoughts on the content discussed therein.

Reinforcement learning is a very interesting area. Unlike supervised or unsupervised learning where we have **prediction** tasks, here we have **control** tasks and control is fundamentally tied to consequences. For example, if you are forecasting sales, you cannot in any reasonable way claim that this is a control task, because your forecast will have absolutely no effect on the real sales in the future. Usually, such a forecast is useful to inform us, but it has no real-world consequences and cannot be considered an **action**.

This is not the case in RL problems, which are about acting in an optimal way. And that is what makes reinforcement learning one of the most important, and in my opinion most exciting, fields in ML right now. It is arguably the closest we have come to a study of Artificial General Intelligence (AGI).

While intelligence may be the ability to model complicated relationships, what ultimately matters is how you use that intelligence to act - and behaviour can only be observed in a control problem where we are endowed with the notions of time, actions, and states. What makes RL algorithms useful is this particular difference that their quality is evaluated in a behaviour space, rather than a loss space.

Likewise, your goals are ultimately defined in the behaviour space. Minimizing a certain loss or predicting accurately are just means to achieving these goals. Imagine if the reward function of the agent dependended not on the state, but just the action taken - this would correspond to a zombie-like agent that does not take the surroundings into consideration and therefore cannot possibly adapt to the environment.

Like many others, my goal is to assist in creating more and more human-like RL agents so that we can get insights about us ourselves. Just like a RL agent is trained to solve a task iteratively by interacting with the environment, so do we, humans, improve in understanding ourselves, by building models of ourselves (the RL agents) that we test on simpler environments. 

However, when comparing humans and RL agents, it’s hard to abstract away the vast difference in the difficulty of the environments where the two types of agents are tested. In the real world, we judge human-ness by the cohesiveness of the responses to questions and the adequateness of verbal and motoric responses to various prompts for interaction. But in the case of an RL agent, what does human-level performance look like if the testing environment is not complex enough to support these real-world criteria? What does human-like behavior look like in an Atari or MuJoCo game, where we cannot use language as “evidence” of consciousness?

A first step in making RL agents more human-like is to make the rewards endogenous to the agent, as opposed to given exogenously by the environment. With humans, we intrinsically set short-term and long-term goals which guide our behavior in a principled and directed manner. Similarly, we can think of an RL agent as choosing his short-term goals by sampling a reward function. The reward function defines a preference over states and therefore an implicit goal for the agent. This opens up interesting algorithms where the agent can learn to choose his short-term goals by sampling a reward function from a Gaussian process or learning it parametrically. However, what then prevents the agent from always sampling a reward function that always returns high rewards (the equivalent of a goal of doing nothing useful)? With humans this is solved by not being able to choose our long-term preferences over the world. We cannot purposefully reach a mental state of nirvana and stay in it forever. Similarly, if the RL agent is able to choose his short-term goals, there has to be a higher more primal and fundamental meta-reward function guiding him, which the agent cannot engineer.

Another way to make RL agents more human-like is by improving their models of the world (their estimated models for the transition dynamics of the environment). Humans process incredibly large amounts of data each second, but consciously perceive only on a tiny part of it. Similarly, an agent should have a powerful feature extractor that processes all signals from the environment but also subsamples the output considerably (through bottlenecks, attention, pooling, etc.) so that downstream tasks are performed faster and on condensed features only. This mimics the focus in humans and the conscious perception of only a handful of features – those carrying the useful information related to the task. We can then ask what happens if we exogenously add additional features in the environment– those representing another agent, perhaps even itself, and label them “you” or even “me”. Can recognizing the features of an agent exactly like you, and labeling these features “me”, be considered developing an actual identity?

### IMOL Highlights

RL is a big and growing research area. Within it we can identify the following possibly overlapping sub-areas:
- __Value-based methods__ - where the agent learns the mean value of states or state-action pairs;
- __Policy-based methods__ - where the agent learns a policy for suggesting the actions directly;
- __Model-based methods__ - where the agent has access to learned predictors for the MDP transition dynamics and can "plan" his actions;
- __Offline (batch) RL__ - where the agent cannot interact with the environment and has to learn entirely from past trajectories;
- __Imitation learning__ - where the agent does not have access to the reward function and has to learn an optimal policy through either mimicking the behaviour of an expert, or learning the reward function;
- __Meta-RL__ - where the agent learns how to learn so that he's able to efficiently few-shot any unseen test tasks;
- __Open-ended learning__ - where the agent learns to extract useful transferable knowledge in the presence of no task.

The IMOL conference is concerned primarily with the last one - learning knowledge without having any specific tasks set. This is generally accomplished by the agent setting his own goals and intrinsic motivation - a type of self-generated reward that is independent of the presence of any extrinsic tasks - is key to that regard.

I've summarized the main highlights in Figure 1 below. Note that this is my personal, opinionated selection of the highlights, there were other just as good presentations and topics which I've left out.

<figure>
    <img class='big_img' src="/resources/imol_tree.png" alt="IMOL2022 highlights" width="1000">
    <figcaption>Figure 1: A tree representing some of the discussed topics in IMOL 2022.</figcaption>
</figure>
