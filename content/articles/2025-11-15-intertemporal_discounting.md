---
Title: Intertemporal Discounting
Date: 2025-11-15 07:00:00 +0200
Tags: econ, rl, ultra-rationalism
slug: intertemporal_discounting
status: draft
---

I want to explore the fundamental topic of intertemporal discounting -- the preference toward current, as opposed to delayed, future satisfaction. This preference is innate in humans. We prefer the same amount of goods now, rather than tomorrow. If we are to receive them tomorrow, we demand *more* of them, so the additional amount compensates for the temporal delay. Intertemporal discounting stands at the [base](synonym?) of many economic behavioral patterns - consumption, saving, fiscal restraint, discipline. We'll explore the topic from different angles: econ, reinforcement learning, and neuroeconomics.

### The Euler Equation

We can start with some theory. Intertemporal choice is often governed by the Euler equation, which represents a necessary but not sufficient condition for a candidate optimal path in a temporal decision problem. Consider a household, infinitely-lived, that seeks to choose how much to consume at each timestep $t$, indicated by $c_t$, so as to maximize its long-term discounted utility:

$$
\max_{c_t} \int_0^\infty \gamma^t u(c_t) dt
$$

Here $c_t$ is a function so this is basically a calculus of variations problem.