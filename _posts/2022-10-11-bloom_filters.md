---
layout: post
title: Bloom Filters
date: 2022-09-14 16:00:00 +0200
tags: [cs]
---

One of my favourite data structures is the Bloom filter, a simple yet efficient probabilistic structure for tracking membership in a set of elements. Bloom filters have nice theoretical properties with simple proofs backing them up. In that sense, they rank very highly in terms of joint usefulness and simplicity. I think this is one measure of the beauty of an idea - how impactful it is in the real world, and how simple (or *regularized*) it is to explain. While this is obviously incredibly subjective, Bloom filters are not.

A [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) for a given set is used to answer the question "Is a given element $x$ in the set?". The two possible answers are "Maybe" and "No", and in that sense the Bloom filter is a probabilistic data structure. The answer "No" guarantees that the element $x$ is not in the set, while the answer "Maybe" means that the element might, or might not be in the set. This uncertainty in the result is something that we have to contend with. It is a trade-off from the space-efficiency of the structure.

A Bloom filter is represented as a binary array $M$ of length $m$, $M \in \\{0, 1\\}^m$, along with $k$ different hash functions. Each of these maps the input (of almost any type) to an integer from $0$ to $m - 1$, included. Moreover, it does so in a uniformly random way, such that similar inputs in terms of bytes $x$ and $x'$ may result in totally different hash values $h(x)$ and $h(x')$. For good hash functions it is very unlikely that $h(x) = h(x')$ for two different random inputs $x$ and $x'$. Nonetheless, this may occur, as ultimately hash functions map an infinite domain to a finite one.

So how do we represent the set membership relation? When adding an element $x$, we compute the hash values $h_1(x), h_2(x), ... h_k(x)$ which are all between $0$ and $m-1$ and flip the corresponding bits in the array $M$ to $1$. Simple as that. 

To query an input $x'$ we compute $h_1(x'), ..., h_k(x')$ and look whether all the corresponding array bits are $1$. If even a single position is $0$, then most certainly $x'$ is not in the set. Why? Because if it's in the set, we would have set $h_1(x'), ..., h_k(x')$ all to $1$ upon adding $x'$. On the other hand, if all of $h_1(x'), ..., h_k(x')$ are $1$, then either $x'$ is really in the set, or we've modified $h_1(x'), ..., h_k(x')$ by chance when previously adding other elements. In that case, the result "Yes" *may* turn out to be a false positive.

We can calculate its probability easily. We model the set $\mathcal{S}$ with the bit array $M$. The probability that a hash function sets a given bit is $\frac{1}{m}$, where $m$ is the size of the bit array. The probability of not setting that bit is $1 - \frac{1}{m}$. Likewise, assuming the hash functions are all independent, the probability of a bit not being set by all $k$ hash functions is

$$
P(M[i] = 0) = \big (1 - \frac{1}{m} \big )^k.
$$

If we have inserted $n$ previous elements, then the probability that bit $i$ is set is

$$
P(M[i] = 1) = 1 - \big ( 1 - \frac{1}{m} \big)^{kn} \approx 1 - e^{-kn/m}. 
$$

A false positive occurs when all $k$ bits corresponding to an element $x'$ not in the set, are equal to $1$. This happens, assuming independence, with probability

$$
\epsilon = P(M[h_i(x')]=1, \forall i \in \{1, ..., k \}) = \Big (1 - \big ( 1 - \frac{1}{m} \big)^{kn} \Big)^k \approx (1 - e^{-kn/m})^k.
$$

This shows that the probability of false positives:
- Decreases as the size of the bit array increases;
- Increases as the the number of already placed elements increases.

We can also find the optimal number of hash functions $k^*$ that minimize the false positive rate.

$$
\frac{d \epsilon}{dk} = \ln(1 - e^{-kn/m}) + \frac{kn}{m}\frac{e^{-kn/m}}{1 - e^{-kn/m}} = 0 \Rightarrow k^* = \frac{m}{n}\ln 2.
$$

By plugging $k^*$ into the false positive rate, we further get the minimum array size that supports a given false positive rate $\epsilon$. We can then get the required number of hash functions only in terms of $\epsilon$ as well:

$$
m^* = -\frac{n \ln \epsilon}{(\ln 2)^2} \\
k^* = -\log_2 \epsilon.
$$

So if I want to represent a set with up to 100 elements, and a maximum false positive rate of 0.01, then I would need a bit array of approximately 959 bits (just about 120 bytes), and 7 hash functions. The suggested number of hash functions from the formula is a real number and has to be rounded in practice. However, the error incurred in doing so is generally very small, especially for large $n$ and $m$ [1].

Note that with only 1 hash function, for a missing element $x'$, a false positive happens when $M[h(x')] = 1$. The probability of this event is considerably higher than the probability that $M[h_i(x')] = 1$, when multiple hash functions are used. In that sense, having many hash functions reduces the false positive rate.

Unfortunately, Bloom filters do not provide a way to know how many elements are in the set. There are estimation formulas for that [2]. Another disadvantage is that there is no way to remove elements from the set. We cannot just hash the element $x$ we want to delete, and set the corresponding bits to 0, because this will also delete any other elements that coincidentally hash to the same bit array indices. With a classic Bloom filter, the only way to delete an element is to rebuild the whole bit array again, without that element. If we go towards supporting additional functionality, counting Bloom filters don't simply set the selected bits to 1, but actually increment the value at those indices by 1. To delete an element then, one computes the hashes and decrements all indices by 1. If any of them is equal to 0, then the element is not in the set. This counting approach, however, has its drawbacks as well - larger array size, limited scalability, and arithmetic overflow.




### References
[1] Goel, A. and Gupta, P. [Small subset queries and bloom filters using ternary associative memories, with applications](https://web.stanford.edu/~ashishg/papers/inverted.pdf) ACM SIGMETRICS Performance Evaluation Review, 38: 143, CiteSeerX 10.1.1.296.6513, doi:10.1145/1811099.1811056 (2010).  
[2] Swamidass, S. J. and Baldi, P. [Swamidass, S. Joshua; Baldi, Pierre (2007), "Mathematical correction for fingerprint similarity measures to improve chemical retrieval](https://pubmed.ncbi.nlm.nih.gov/17444629/), Journal of Chemical Information and Modeling, 47 (3): 952–964, doi:10.1021/ci600526a, PMID 17444629 (2007).  
