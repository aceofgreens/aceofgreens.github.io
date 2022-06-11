---
layout: post
title: Principles of Optimal Induction
date: 2022-06-01 16:00:00 +0200
tags: [ai, cs]
---

Artificial general intelligence (AGI) still seems to be elusive. Although we are getting close to building a first [generalist RL agent](https://www.deepmind.com/publications/a-generalist-agent), it is unclear what exactly distinguishes, if at all, an AGI agent from a non-AGI one, trained on many different tasks, and able to generalize across them. Turns out, candidates for the kind of mathematical formalism that we need are already here. This post examines these beautiful, intuitive ideas and discusses what it takes to build an agent capable of coming up with the optimal-*est* optimal decisions.

Suppose you have the sequence $1, 1, 1, 1, 1$ and you're trying to predict the next number. It is sensible to predict $1$ again because the observed sequence had a constant value of $1$ in the past and there are no indications that the next number should be different. However, it is also possible to conjecture that the next number will be $5$ and that the data-generating process is e.g. "The first 5 numbers are ones, and after that it's all fives". This is certainly agreeing with the observations, but why do we find it absurd?

Our brains *feel* that some conjectures are better than others. This feeling is a manifestation of the abstractions that the human brain has evolved to provide. We prefer simpler solutions to complicated ones and this most probably reflects a regularity in the universe that simple-to-express relationships account for more events than difficult-to-express ones.

In any case, it is not a new idea that among all hypotheses that explain the observed data equally well we should favour the simplest one. This is exactly [Occam's razor](https://en.wikipedia.org/wiki/Occam%27s_razor). And note that this does not say anything about which, of all competing hypotheses, is true. It only says that we should act as if the simplest one is true.

In computer science, the simplicity of a description can be measured by its length and the complexity of an object can be defined as the length of that object's shortest description, this being the famous concept of [algorithmic (or Kolmogorov) complexity](https://en.wikipedia.org/wiki/Kolmogorov_complexity). If we have a Turing machine $T$ and a program $p$, we say that $p$ is a description of a string $x$ if $T(p) = x$. Then, if $\ell(p)$ is the length of the program $p$ in bits, 

$$
K_T(x) = \min_p \ \{\ell (p): T(p) = x \}
$$

is the length of the shortest description of $x$ under Turing machine $T$.

The definition depends on $T$ which is inconvenient. It can be proved that a universal Turing machine, being able to simulate other Turing machines on arbitrary inputs, can *almost* produce always the shortest program for any $x$:

$$
K_U(x) \le K_T(x) + C_{TU}.
$$

This means that a universal Turing machine can produce a description of $x$ that is only a constant number of bits longer than that of $T$, for all $x$ and $T$. This is useful, because it allows us to not focus on the exact $T$ that computes the description and just use a universal $T$. As a consequence, we can say that the **information content** or **algorithmic complexity** of an object is the length of the shortest program that produces that object as output, when ran on a universal Turing machine.

But if we have multiple hypotheses all consistent with the observed data, does it really make sense to discard all but the simplest? What if the simplest one has a algorithmic complexity of 51 symbols and that of the the next one is 53 symbols? Then these two hypotheses differ in complexity only slightly. Shouldn't we keep them? Bayes tell us that:

$$
p(\mathcal{H} | \mathcal{D}) = \frac{p(\mathcal{D} | \mathcal{H}) p(\mathcal{H})}{p(\mathcal{D})}
$$

where $\theta$ are the model parameters, $\mathcal{D}$ is the observed data, and $\mathcal{H}$ are the hyperparameters (model structure and hypothesis). In any case, we need a prior on $\mathcal{H}$ and one in line with Occam's razor is 

$$
p(\mathcal{H_i}) \propto 2^{-K_U (\mathcal{H_i})}.
$$

This prior suggests that we keep all consistent hypotheses, but weigh them exponentially according to their algorithmic complexity. The base of the exponent is $2$ because the number of programs, or hypotheses, of length $n$ is exactly $2^n$. The normalization factor for the prior considers all programs which are consistent with the data, of which there may be a countably infinite number.

This idea is in the right direction. From here, we can reach Ray Solomonoff's *universal probability distribution*, one of the most important concepts in the area of algorithmic information theory. This distribution is used to assign a prior to any observation. If we represent the observation as a binary string $x$, then $M(x)$ is defined as the weighted sum of the complexities of all explanations consistent with the data. That is,

$$
M(x) = \sum_{p: \ U(p) = x*} 2^{-\ell(p)}.
$$

We can think of this formula as follows. First, we fix the observed binary sequence $x$. Then, we select a universal Turing machine $U$ and set its input tape to contain a number of random coin flips of length $\ell(x)$. Note that the probability that $x$ was generated by a random coin process is $2^{-\ell(x)}$. Then, with this input, we find all programs $p$ that when ran on $U$ produce an output string starting with $x$. Subsequently, we compute the lengths of all these programs, and sum them in a weighted fashion, where the weights are exponential and inversely proportional to the lengths. This gives us the prior probability of observing $x$. The notation $x*$ means any string in which $x$ is a prefix.

Since any string $x$ can be computed on $U$ by 1 or more programs, $M(\cdot)$ assings a non-zero probability to all programs consistent with the data and we do not discard any plausible hypotheses. Because of the weights, programs with shorter length have exponentially larger weight compared to programs with longer length. As a result, $M(x) \approx 2^{-K_U(x)}$.

The fact that the output string can be longer than $\ell(x)$ relates to the ability to predict. In fact, a program $p$ may not halt after $\ell(x)$ symbols, it may produce infinitely many symbols. Those after the $\ell(x)$-th index can be treated as predictions for unobserved future data. The only constraint on the program $p$ is that it is consistent with the past, i.e. the output string strats with $x$.

If $x$ is past observed data and $y$ is future unobserved data, then the posterior of $y$ given $x$ is defined as $M(y\|x) = M(xy)/M(x)$. The notation $xy$ means that $x$ and $y$ are concatenated. It can be proved that $M(y \| x) \approx 2^{-K_U(y\|x)}$, where $K_U(y \| x)$ is a small variation of the Kolmogorov complexity definition where the universal machine $U$ is given as input a properly encoded string $x$ concatenated to the program $p$. In general, the above conditional probability $M(y \| x)$ is large only if $y$ has a short succinct explanation from $x$. In a sequential prediction setting, this implies that $M(y \| x)$ is large only if the past $x$ predicts the future $y$ well.

The combination of keeping all consistent explanations and weighing them by their length provides us with a **complete and universal theory of prediction**. Moreover, the prediction capabilities described above, also known as Solomonoff Induction, are as optimal as they can get. Solomonoff proved in 1978 that the expected squared loss, given a properly framed prediction problem, is bounded and $M(x_{n+1}\| x_1, ..., x_n)$ converges to the true data-generating distribution. This is valid for *any* computable sequence with only minimal data needed.

The downside is that the universal prior $M(x)$ is uncomputable, because some of the programs $p$ may not halt. As a result, it is impossible to implement Solomonoff's induction in practice. This motivates the need for approximation algorithms which trade-off accuracy for computability.

### Extensions

Given that $M(x)$ is uncomputable, we can approximate it as follows. We know that $M(x) \approx 2^{-K_U(x)}$ and that very roughly $K_U(x) \approx K_T(x)$. Then the concept of **Minimum Description Length** (MDL) is an approximation of the maximum a-posteriori solution of $y\|x$. It states that predicting $y$ of maximum $M(y \| x)$ is approximately the same as predicting $y$ of minimum complexity $K_T(xy)$. In other words, we are looking for a prediction $y$ that when combined with past observations $x$, this joint data is maximally compressible. In practice $T$ could be any powerful compression algorithm like [Lempel-Ziv-Welch](https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch) or [DEFLATE](https://en.wikipedia.org/wiki/Deflate).

This also reveals the connection between intelligence and compression. Intelligence is the ability to model and compression is the ability to distill something to only its important patterns. Both concepts rely on finding regularities in the underlying data and because of that, intelligence is equivalently defined as the ability to compress information.

The quantity $K_U(x \| y)$ mentioned above could be related to how similar the objects $x$ and $y$ are. Intuitively, they are similar if $x$ can be reconstructed from $y$ which happens if $K_U(x \| y)$ is small. However, $K_U(x \| y)$ is not suited for a distance metric because it's not symmetric, normalized or even computable. We can make it symmetric and normalized (but still not computable) if we define the distance metric as:

$$
0 \le d(x, y) := \frac{\max \{ K_U(x | y), K_U(y | x) \}}{\max \{ K_U(x), K_U(y)\}} \le 1.
$$

As a further enhancement, to approximate this quantity with a computable version, the **Normalized Compression Distance** [1] is defined as:

$$
d(x, y) \approx \frac{K_T(xy) - \min \{ K_T(x), K_T(y)\}}{\max \{K_T(x), K_T(y) \}}
$$

where $T$ is a compressor, as before. Again, two objects are similar if given one of the objects, there is a short and succinct program that outputs the other object. Efficient compression and intelligence, in general, is a requirement for being able to notice similarities between objects.

The biggest extension to the prediction theory presented above is when Solomonoff's universal induction is applied to a rational agent in an environment. This yields the [AIXI (or AI$\xi$)](https://en.wikipedia.org/wiki/AIXI) model [2, 3]. It relies on Occam's razor for induction, has no restrictions on the internal working of the agent, does not rely on hard-to-define terms like creativity, wisdom, consciousness, and being based on computation, is non-anthropocentric. There is strong evidence that this is **the most intelligent environmental independent agent possible**.

The AIXI agent interacts with an environment, receiving observations $o_t$ and rewards $r_t$. At every time step $t$, the agent has access to the history of all previous observations $o_1, ..., o_{t-1}$ and rewards $r_1, ..., r_{t-1}$ and has to select the action $a_t$ that would maximizes the long-term sum of future rewards. This is a standard reinforcement learning setup. The AIXI agent selects the action as

$$
a_t = \text{arg} \max_{a_t} \bigg ( \sum_{o_t, r_t}  ... \Big ( \max_{a_m} \sum_{o_m, r_m} [r_t + ... + r_m] (\sum_{p: \ U(p, a_1, ..., a_m) = o_1r_1...o_mr_m} 2^{-\ell(p)} ) \Big ) \bigg).
$$

We can think of this as follows. The agent considers a time horizon of $t - m$ steps into the future. Before step $t$ all the actions $a_{<t}$, observations $o_{<t}$, and rewards $r_{<t}$ are real and collected. After step $t$ and up to $m$ all the quantities are imagined and depend on the learned model dynamics. The agent aims to maximize the sum of imagined rewards from the current step $t$ to step $m$, which depends on the sequence of actions from $t$ to $m$. For every sequence of imagined actions, we get a sequence of imagined rewards, whose sum is multiplied by a penalty - a mixture of all computable environments consistent with the agent's past observations and rewards (what we called $M(\cdot)$ above). The AIXI agent then choose the action whose consequence will maximize that eventual sum of rewards. 

Unfortunately, while AIXI is powerful and able to learn the environment dynamics, whether it is optimal is unclear [4]. It can predict the value of its actions, but it cannot predict the value of counterfactual actions not taken. Claiming that a learned policy is Pareto optimal is only *relative* to the universal Turing machine (UTM) used in AIXI. There are UTMs that when used, result in priors which are retained indefinitely, possibly leading to insufficient exploration. And unfortunately, insufficient exploration automatically leads to non-optimal asymptotic performance in all computable environments.

The crux of this problem is that there cannot exist any invariance theorem for AIXI which bounds the quantity of rewards collected when changing the UTM. On the other hand, for Solomonoff induction such invariance theorems exist - the Kolmogorov complexities calculated by different UTMs differ only by a constant. It appears that the exploration-exploitation nature of reinforcement learning is a fundamental unavoidable obstacle.

This post covered the fundamental ideas of Kolmogorov complexity, Solomonoff induction, and its extensions to universal similarity and AIXI. I have purposefully avoided some minor technical details, in order to make the text less cumbersome. In particular, the $M(\cdot)$ distribution requires a *monotone* TM and is, itself, not a probability measure, but a *semi*-measure. The definition of $K_T(x\|y)$ was not presented because it relies on other notation like [Elias Delta codes](https://en.wikipedia.org/wiki/Elias_delta_coding). For a proper technical discussion one can visit the topics of [algorithmic probability](http://www.scholarpedia.org/article/Algorithmic_probability) and Marcus Hutter's awesome [book slides](http://www.hutter1.net/ai/suaibook.pdf).


### References
[1] Vitanyi, P. [Universal Similarity](https://arxiv.org/abs/cs/0504089) arXiv:cs/0504089 (2005).  
[2] Hutter, M. [A Theory of Universal Artificial Intelligence based on Algorithmic Complexity](https://arxiv.org/abs/cs/0004001) arXiv:cs/0004001 (2000).  
[3] Hutter, M. [Universal Artificial Intelligence: Sequential Decisions based on Algorithmic Probability](https://books.google.com/books?id=NP53iZGt4KUC). Texts in Theoretical Computer Science an EATCS Series. (2005).  
[4] Leike, J. and Hutter, M. [Bad Universal Priors and Notions of Optimality](http://proceedings.mlr.press/v40/Leike15.pdf) Proceedings of The 28th Conference on Learning Theory (2015).  