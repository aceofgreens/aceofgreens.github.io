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

In general an *encoding* is a function which maps outcomes to strings of symbols. For simplicity, we can think of it as taking a particular $x$ and mapping it to a binary string called a *code*, e.g. $011011$. Typically we are interested in finding an encoding which minimizes the length of the average code, according to the probabilities of the random variable $X$. As we'll see soon, there is a fundamental limit on how short the average code can be without losing information.

Compressing data refers to encoding it in a way such that the total code length is less than the length of the unencoded data. One important criterium is average information content per source symbol. Suppose we have a source file and we encode it into a file with $L$ bits per source symbol. If we can recover the data reliably, then necessarily the average information content of that source is at most $L$ bits per symbol. Not all encodings compress the data. If there are $M$ outcomes we can always encode them with $M$ codes, all of the same length, each with $\log_2 M $ bits. This encoding does not consider the probabilities and hence cannot does not compress anything. 

There are two types of compressors. А lossy algorithm maps *all* outcomes to shorter codewords, but some outcomes are mapped to the same keyword. As a result, the decoder cannot unambiguously reconstruct the outcome, which sometimes leads to decoding failures. Instead, a lossless algorithm maps *most* outcomes to shorter keywords. It preserves all information but some outcomes, the rare ones, have longer codewords.

Let's consider lossy compression. For any $0 \le \delta \le 1$, we can compute the smallest $\delta$-sufficient subset $S\_\delta$, satisfying $P( x \in S\_\delta) \ge 1 - \delta$. Intuitively, this set contains the most probable outcomes - those until their sum becomes greater than $1 - \delta$. How does it relate to lossy compression? One needs to recognize that the length of the code is always proportional to the number of possible outcomes. To distinguish between $n$ outcomes, you need $\log_2 n$ symbols for the binary codes. Therefore, if we simply disregard some of the rarer outcomes, we can in principle have shorter codes. The quantity $\delta$ is then the probability, set by us, that an outcome will not be encoded at all. If $\delta$ is very high, then most outcomes will not be encoded. Those that will be, will be very few, and hence the codes will be short. The quantity $\log_2 \| S\_\delta \|$ is called the essential bit content of $X$, $H\_\delta(X)$. It gives the number of symbols needed to distinguish the most common outcomes of $X$, with an accepted error of $\delta$.

Finally, consider $N$ i.i.d. random variables like $X$, $X^N = (X_1, X_2, ..., X_N)$. The joint entropy is given by $NH(X)$, for any one $X$. But can we say anything about $H_\delta(X_1, ..., X_N)$? For concreteness assume the outcomes $\mathcal{A}\_X$ are different symbols from an alphabet. Consider the "most typical" outcome of $X^N$. $X^N$ will likely contain $p(x_1)N$ instances of the first symbol, $p(x_2)N$ instances of the second symbol and so on. The information content of this typical string is precisely $NH$. Slightly less typical strings will have information content somewhere around $NH$. Now consider the information content of $\textbf{x}$ itself as a random variable, $-\log_2 p(\textbf{x})$. Its expected value is $NH$. If we scale it by $N$, it's expected value will be $H$. Now, define a threshold $\beta$ that will determine whether $\textbf{x}$ is "typical" enough, as evidenced by how close its information content is to the expected information content:

$$
T_{N\beta} = \Big\{ \textbf{x} \in \mathcal{A}_X^N : \lvert  -\frac{1}{N} \log_2 p(\textbf{x})  - H \rvert < \beta \Big\}.
$$

Here $\mathcal{A}_X^N$ is the set of all joint outcomes. Naturally, the probability of any typical $\textbf{x}$ satisfies 
$2^{-N(H + \beta)} < P(x) < 2^{-N(H - \beta)}$ and hence, by the law of large numbers the probability that $\textbf{x}$ is typical will become close to unity as $N$ increases:

$$
\begin{align}
P(\textbf{x} \in T_{N\beta}) &\ge 1 - \frac{\sigma^2}{\beta^2 N}, \\
\sigma^2 &= \text{Var}(- \log_2 p(x_n)).
\end{align}
$$

There is an important relationship between $T_{N\beta}$ and $H_\delta(X^N)$. To find the essential bit content $H_\delta(X^N)$ we need to find the most likely $\textbf{x}$-s. The typical elements $T_{N \beta}$ likely do not belong in this set. But if there are many typical elements, then necessarily there are not many high-probability outcomes, which bounds the essential bit content. The smallest probability that a typical $\textbf{x}$ can have is $2^{-N(H + \beta)}$. We need $\| T_{N\beta}\| 2^{-N(H + \beta)} < 1$ and hence $\| T_{N\beta} \| < 2^{N(H + \beta)}$. Hence $H_\delta(X^N)$ is bounded from above by $N(H + \beta)$. We now set $\beta = \epsilon$ and choose some possibly large $N_0$ such that $\frac{\sigma^2}{\epsilon^2 N_0} \le \delta$. The result is that $1/N \cdot H_\delta(X^N) < H + \epsilon$, which is independent of $\delta$.

A proof by condradiction based on similar logic shows that $1/N \cdot H_\delta(X^N) > H - \epsilon$, which is again, indepedent of $\delta$. This result is quite deep and is called [Shannon's source coding theorem](https://en.wikipedia.org/wiki/Shannon%27s_source_coding_theorem):

$$
 H - \epsilon < \frac{1}{N} \cdot H_\delta(X^N) <  H + \epsilon.
$$

Here's how to interpret it. We have a source of information - a random variable. We first fix the probability of error $\delta$ that they are willing to accept. We might even fix it something arbitrarily close to $0$. Now, the average minimal bits per symbol consistent with $\delta$ are given by $H_\delta(X^N)/N$. For any finite sequence of $N$ samples, the required bits per symbol do not exceed $H + \epsilon$. $N$ and $\epsilon$ depend on each other, so for a fixed length $N$, we can calculate an $\epsilon$ or vice versa, for a desired $\epsilon$ we can calculate a required $N$. As $N$ tends to infinity the bits per symbol of the encoding cannot increase beyond the entropy. Likewise, one needs at least $H-\epsilon$ bits per symbol to specify $\textbf{x}$, even if we allow errors most of the time. Therefore, this result establishes that for lossless compression the average optimal code length cannot be shorter than the entropy.