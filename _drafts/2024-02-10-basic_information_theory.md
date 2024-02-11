---
layout: post
title: Information, Codes, and Content
date: 2024-02-10 07:00:00 +0200
tags: [cs]
# excerpt_separator: <!--more-->
---

Information theory is the subfield of applied mathematics concerned with topics like information content, data compression, information storage and transmission. Some of the key terms appear often in machine learning and I have found myself sometimes cross-referencing various concepts from both disciplines. In this post, we cover some of the absolute basics - entropy, some simple codes, and some limiting results. I think these ideas integrate nicely with other fields and are useful as a general background context for machine learning.

What is a bit? What is information? These questions are surprisingly abstract and difficult to formalize. Some philosophers are dedicating their entire careers on these concepts. For us, a good definition I've heard is: a bit is a *single discernible difference*. This difference is always between two comparable objects. Are they different? Yes or no - these are the options. Just two. Naturally, with 2 bits we can represent 4 different states - for example "no", "somewhat", "almost", and "yes". With 3 bits we can represent 8 states, and so on. With $n$ bits we can represent $2^n$ different states. From here one intuitively understands why the exponents and logarithms are used. The beauty of the bit is that it's a formal concept, defined only by its *form*, representing any difference between two objects, somewhat similar to how the number 5 represents any group with 5 objects.

Even if we live in a deterministic universe, our *beliefs* about the current world state are limited and can be represented as probabilities, this being called the subjective interpretation of probability, as opposed to the frequentist one. In that case the outcomes of interest become random variables. And by virtue of the fact that random variables can have multiple *discernably different* outcomes, we conclude that the information of an outcome depends on its probability.

The information content, or uncertainty, of a random outcome $x$ is given by $H(X = x) = -\log_2 p(x)$. The entropy of the whole random variable $X$ is the average uncertainty of any one outcome, 

$$
H(X) = -\sum_{x} p(x) \log_2 p(x) = \mathbb{E}_x[\log_2 p(x)].
$$

It is maximal when all outcomes are equiprobable. If the entropy is $n$ bits, then observing any outcome gives us 5 bits of information. Some particular outcomes may give us more or less information.

In general an *encoding* is a function which maps outcomes to strings of symbols. For simplicity, we can think of it as taking a particular $x$ and mapping it to a binary string called a *code*, e.g. $011011$. Typically, we are interested in finding an encoding which minimizes the length of the average code, according to the probabilities of the random variable $X$. As we'll see shortly, there is a fundamental limit on how short the average code can be without losing information.

Compressing data refers to encoding it in a way such that the total code length is less than the length of the unencoded data. There are two types: a lossy compression algorithm always maps some outcomes to the same code making decoding ambiguous and therefore losing information, a lossless compression algorithm does not lose information but produces some codes that are longer than the description.

Let's consider lossy compression. Suppose $X$ is the random variable, $\mathcal{A}\_X$ are the outcomes. For any $0 \le \delta \le 1$, we can compute the smallest $\delta$-sufficient subset $S\_\delta$, satisfying $P( x \in S\_\delta) \ge 1 - \delta$. Intuitively, this set contains the most probable outcomes - those until their sum becomes greater than $1 - \delta$. Intuitively, this setup allows for block lossy compression, where we encode only the most likely outcomes, failing to produce an encoding for the rest. The tolerable error rate is $\delta$. The quantity $\log_2 \| S\_\delta \|$ is called the essential bit content of $X$, $H\_\delta(X)$. Finally, consider $N$ i.i.d. random variables like $X$, $X^N = (X_1, X_2, ..., X_N)$. The joint entropy is given by $NH(X)$, for any one $X$. But can we say anything about $H_\delta(X_1, ..., X_N)$?

For concreteness assume the outcomes $\mathcal{A}\_X$ are different symbols from an alphabet. Consider the "most typical" outcome of $X^N$. $X^N$ will likely contain $p(x_1)N$ instances of the first symbol, $p(x_2)N$ instances of the second symbol and so on. The information content of this typical string is precisely $NH$. Slightly less typical strings will have information content somewhere around $NH$. Now consider the information content of $\textbf{x}$ itself as a random variable, $-\log_2 p(\textbf{x})$. Its expected value is $NH$. If we scale it by $N$, it's expected value will be $H$. Now, define a threshold $\beta$ that will determine whether $\textbf{x}$ is "typical" enough, as evidenced by how close its information content is to the expected information content:

$$
T_{N\beta} = \Big\{ \textbf{x} \in \mathcal{A}_X^N : \lvert  -\frac{1}{N} \log_2 p(\textbf{x})  - H \rvert < \beta \Big\}.
$$

Here $\mathcal{A}_X^N$ is the set of all joint outcomes. Naturally, the probability of any typical $\textbf{x}$ satisfies 
$2^{-N(H + \beta)} < P(x) < 2^{-N(H - \beta)}$ and hence, by the law of large numbers the probability that $\textbf{x}$ is typical will become close to unity, as $N$ increases:

$$
\begin{align}
P(\textbf{x} \in T_{N\beta}) &\ge 1 - \frac{\sigma^2}{\beta^2 N}, \\
\sigma^2 &= \text{Var}(- \log_2 p(x_n)).
\end{align}
$$

There is an important relationship between $T_{N\beta}$ and $H_\delta(X^N)$. To find the essential bit content $H_\delta(X^N)$ we need to find the most likely $\textbf{x}$-s. The typical elements $T_{N \beta}$ likely do not belong in this set. But if there are many typical elements, then necessarily there are not many high-probability outcomes, which bounds the essential bit content. The smallest probability that a typical $\textbf{x}$ can have is $2^{-N(H + \beta)}$. We need $\| T_{N\beta}\| 2^{-N(H + \beta)} < 1$ and hence $\| T_{N\beta} \| < 2^{N(H + \beta)}$. Hence $H_\delta(X^N)$ is bounded from above by $N(H + \beta)$. We now set $\beta = \epsilon$ and choose some possibly large $N_0$ such that $\frac{\sigma^2}{\epsilon^2 N_0} \le \delta$. The result is that $1/N \cdot H_\delta(X^N) < H + \epsilon$, which is independent of $\delta$.

