---
layout: post
title:  Phase Transitions in Computation
date:   2022-03-05 23:32:03 +0200
tags: cs
---

One of my all-time favourite topics in theoretical computer science is that of phase transitions in computational problems. I think these are one of the most beautiful and incredible phenomena because of their mystic and fundamental nature. Unlike in physics, where phase transitions have been known for quite some time now, they are relatively new in computer science, where they first first appeared in the 1990s. This post explores some very basic phase transitions in the 3-SAT problem. All content for this post comes from Cristopher Moore and Stephan Mertens' awe-inspiring book [The Nature of Computation](https://www.amazon.com/Nature-Computation-Cristopher-Moore/dp/0199233217/ref=sr_1_1?crid=2CWBHWPZCPT26&keywords=nature+of+computation&qid=1648843521&sprefix=nature+of+computation%2Caps%2C169&sr=8-1).

Phase transitions can be thought of as abrupt qualitative changes to the behaviour and characteristics of a system, dependant on specific values of key parameters in that system. Typical examples of phase transitions in physics are:
- The transition of matter from a solid state to liquid state (melting) or from a liquid state to a solid state (freezing),
- The emergence of superconductivity when cooling certain metals,
- The phenomenon where some materials lose their permanent magnetic properties when heated above a certain temperature.

Here however, we'll be concerned with computational problems and our phase transitions will be interpreted as a rapid change in the amount of computation needed to find a solution to a given decision problem or assert that no solution exists. Importantly, the problem instances will be random instead of the typical worst-case instances chosen by a malevolent adversary.

We begin by defining a uniform distribution over 3-SAT formulas with $n$ variables and $m$ clauses. There are $M = 2^3 {n \choose 3}$ possible clauses because out of $n$ variables we need to choose 3, and each one of these can be negated. To generate a random formula we sample uniformly *with replacement* $m$ clauses out of the possible ones. The parameter governing the solvability of the sampled formula is the density of clauses to variables $\alpha = \frac{m}{n}$.

For solving NP-complete problems like 3-SAT we can use a backtracking algorithm. Specifically, for 3-SAT we can use the `DPLL` algorithm (which stands for Davis, Putnam, Logemann, Loveland):

```
DPLL
  input: a SAT formula S
  output: is S satisfiable?
  begin
    if S is empty, return true;
    if S contains an empty clause, return false;
    select an unset variable x;
    if DPLL(S[x = true]) = true, return true;
    if DPLL(S[x = false]) = true, return true;
    return false;
  end
```




