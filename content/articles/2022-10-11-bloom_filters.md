---
title: Bloom and Cuckoo
date: 2022-10-15 16:00:00 +0200
tags: cs
slug: bloom_filters
---

One of my favourite data structures is the Bloom filter, a simple yet efficient probabilistic structure for tracking membership in a set of elements. Bloom filters have nice theoretical properties with simple proofs backing them up. In that sense, they rank very highly in terms of joint usefulness and simplicity. I think this is one measure of the beauty of an idea - how impactful it is in the real world, and how simple (or *regularized*) it is to explain. While this is obviously incredibly subjective, Bloom filters are not.

A [Bloom filter](https://en.wikipedia.org/wiki/Bloom_filter) for a given set is used to answer the question "Is a given element $x$ in the set?". The two possible answers are "Maybe" and "No", and in that sense the Bloom filter is a probabilistic data structure. The answer "No" guarantees that the element $x$ is not in the set, while the answer "Maybe" means that the element might, or might not be in the set. This uncertainty in the result is something that we have to contend with. It is a trade-off from the space-efficiency of the structure.

A Bloom filter is represented as a binary array $M$ of length $m$, $M \in \{0, 1\}^m$, along with $k$ different hash functions. Each of these maps the input (of almost any type) to an integer from $0$ to $m - 1$, included. Moreover, it does so in a uniformly random way, such that similar inputs in terms of bytes $x$ and $x'$ may result in totally different hash values $h(x)$ and $h(x')$. For good hash functions it is very unlikely that $h(x) = h(x')$ for two different random inputs $x$ and $x'$. Nonetheless, this may occur, as ultimately hash functions map an infinite domain to a finite one.

So how do we represent the set membership relation? When adding an element $x$, we compute the hash values $h_1(x), h_2(x), ... h_k(x)$ which are all between $0$ and $m-1$ and flip the corresponding bits in the array $M$ to $1$. Simple as that.

<figure>
    <img class='img' src="/images/bloom.svg" alt="Bloom filter" width="1200">
    <figcaption>Figure 1: A simple Bloom filter with 3 hash functions. We have added 2 elements to the set, but there is a collision and as a result there are 5 bits flipped, instead of 6.</figcaption>
</figure>

To query an input $x'$ we compute $h_1(x'), ..., h_k(x')$ and look whether all the corresponding array bits are $1$. If even a single position is $0$, then most certainly $x'$ is not in the set. Why? Because if it's in the set, we would have set $h_1(x'), ..., h_k(x')$ all to $1$ upon adding $x'$. On the other hand, if all of $h_1(x'), ..., h_k(x')$ are $1$, then either $x'$ is really in the set, or we've modified $h_1(x'), ..., h_k(x')$ by chance when previously adding other elements. In that case, the result "Yes" *may* turn out to be a false positive.

We can calculate the probability of false positives easily. We model the set $\mathcal{S}$ with the bit array $M$. The probability that a hash function sets a given bit is $\frac{1}{m}$, where $m$ is the size of the bit array. The probability of not setting that bit is $1 - \frac{1}{m}$. Likewise, assuming the hash functions are all independent, the probability of a bit not being set by all $k$ hash functions is

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
k^* = -\log_2 \epsilon.$$

This also shows that $m^*/n \approx -1.44 \log_2 \epsilon$ - for every element I want to add, I need 44% more bits of space compared to the optimal amount [1]. So if I want to represent a set with up to 100 elements, and a maximum false positive rate of 0.01, then I would need a bit array of approximately 959 bits (just about 120 bytes), and 7 hash functions. The suggested number of hash functions from the formula is a real number and has to be rounded in practice. However, the error incurred in doing so is generally very small, especially for large $n$ and $m$ [2].

Note that with only 1 hash function, for a missing element $x'$, a false positive happens when $M[h(x')] = 1$. The probability of this event is considerably higher than the probability that $M[h_i(x')] = 1$, when multiple hash functions are used. In that sense, having many hash functions reduces the false positive rate.

Unfortunately, Bloom filters do not provide a way to know how many elements are in the set. There are estimation formulas for that [3]. Another disadvantage is that there is no way to remove elements from the set. We cannot just hash the element $x$ we want to delete, and set the corresponding bits to 0, because this will also delete any other elements that coincidentally hash to the same bit array indices. With a classic Bloom filter, the only way to delete an element is to rebuild the whole bit array again, without that element. If we go towards supporting additional functionality, counting Bloom filters don't simply set the selected bits to 1, but actually increment the value at those indices by 1. To delete an element then, one computes the hashes and decrements all indices by 1. If any of them is equal to 0, then the element is not in the set. This counting approach, however, has its drawbacks as well - larger array size, limited scalability, and arithmetic overflow.

A nice additional feature, albeit of limited practical value, is that one can compute the union of two sets by simply `OR`-ing the two respective Bloom filter arrays, assuming they have the same array size and hash functions. The resulting array will represent the union. If instead, we apply the `AND` operator, the resulting Bloom filter has a false positive rate equal to the maximum rate of the two input filters. This may be larger than the false positive rate that we get if we build the resulting Bloom filter for the set intersection from scratch.

There are various other data structures which improve over the Bloom filter by adding the ability to delete elements from the set, and reducing the space overhead. One popular such structure is the [Cuckoo filter](https://en.wikipedia.org/wiki/Cuckoo_filter), invented in 2014 [4].

The Cuckoo filter is based on cuckoo hashing, where we have two hash tables $T_1$ and $T_2$ of size $r$, and two hash functions $h_1(\cdot)$ and $h_2(\cdot)$. To lookup if an element is in, we look into both tables using $T_1[h_1(x)]$ and $T_2[h_2(x)]$. Deleting an element simply deletes it from whichever table $T_1$ or $T_2$ it's in.

Inserting an element $x$ is done by repeating the following:

1. If $T_1[h_1(x)]$ is empty, place $x$ there and return
2. If not, evict the current element $x'$ from $T_1[h_1(x)]$, and place $x$ in its place
3. If $T_2[h_2(x')]$ is empty, place $x'$ there and return
4. Otherwise, evict $x''$ from $T_2[h_2(x')]$ and place $x'$ there
5. Repeat 1-4 until an empty place is found for $x''$ or a maximum number of iterations is reached.

The worst-case time complexity of lookup and deletion is $O(1)$ and it can be proven than the time complexity of insertion is also $O(1)$, but in expectation, and only as long as the load factor (number of keys in the hash table divided by the size of the hash table) is less than 50%. Note that it's possible, though unlikely, that a loop is formed. For example, $x$ takes the place of $x'$ in $T_1$, then $x'$ takes the place of $x''$ in $T_2$, and then $x''$ takes the place of the newly-inserted $x$ in $T_1$. In this case, after a number of iterations the element without a place is just dropped.

Going from cuckoo hashing to cuckoo filters takes a bit more work but is manageable. The Cuckoo filter uses a hash tables consisting of a number of *buckets*. Each bucket consist of multiple *entries* storing fingerprints of the objects in the set that is modelled. The whole table can be considered a two-dimensional array $M$ where $M[i]$ is the $i$-th bucket and $M[i, j]$ is the $j$-th entry in the $i$-th bucket. There are two hash functions, $h_1$ and $h_2$, which map objects into buckets. The fingerprints are used mainly to reduce the table size.

To lookup an item $x$:

1. We compute the fingerprint $f$ of $x$
2. We compute two bucket indices $i_1$ and $i_2$ such that  
$i_1 = h_1(x)$ and $i_2 = i_1 \oplus h_2(f)$
3. If $M[i_1]$ or $M[i_2]$ contains $f$, return `true`, else return `false`.

Here $\oplus$ is the bitwise `XOR` operation. The use of multiple hash functions bears resemblance to the Bloom filters. The calculation with the `XOR` operation is called *partial-key cuckoo hashing* and allows one to calculate the second bucket index directly from the first and the fingerprint, bypassing the need to retrieve the original item (which may be large and stored on disk).

The deletion is very similar, we calculate the bucket indices $i_1$ and $i_2$ and if one of them has the fingerprint $f$, we delete a copy of $f$ from that bucket. Importantly, deletion is dangerous because it may delete an element whose fingerprint collides with that of the element we really want to delete. It is safe to delete only items which have been inserted in the table.

Finally, the insertion strongly resembles that of standard cuckoo hashing:

1. Compute the fingerprint $f$ of $x$
2. Compute two bucket indices $i_1$ and $i_2$ such that  
$i_1 = h_1(x)$ and $i_2 = i_1 \oplus h_2(f)$
3. If $M[i_1]$ or $M[i_2]$ has an empty entry, add $f$ in that bucket and return
4. Otherwise, select $i$ randomly from $i_1$ and $i_2$
5. Select a random entry $e$ from $M[i]$
6. Swap $f$ with $e$
7. Compute the second index $j = i \oplus h_2(f)$
8. If $M[j]$ has an empty entry, add $f$ to it and return
9. Otherwise repeat 4-8 until until an empty entry is found or a number of specified iterations have passed.

<figure>
    <img class='small_img' src="/images/cuckoo.svg" alt="Cuckoo filter" width="1200">
    <figcaption>Figure 2: A simple Cuckoo filter with 6 buckets (the rows) and 4 entries per bucket (the columns). Buckets 2 and 5 are full with previous fingerprints $f_1, ..., f_8$. When inserting a new fingerprint $f$ for item $a$ we need to randomly evict one of the previous fingerprints, place $f$ in its place and find it a new place according to the cuckoo collision resolution scheme.</figcaption>
</figure>

The Cuckoo filter's asymptotic properties depend on the load factor $\alpha$ - how filled up the hash table is, as a percentage. The inventors have analyzed various relationships and state that:

- Having more entries in each bucket requires having longer fingerprints to keep the same false positive rate. It can be derived that
the minimum fingerprint size $f$ required to retain a false positive rate $\epsilon$ is
$ f \ge \lceil {\log_2 (2b/ \epsilon)} \rceil$, where $b$ is the number of entries in a bucket.
- The average space cost $C$ is bounded by $C \le \lceil {\log_2(1/ \epsilon) + \log_2 (2b)} \rceil / \alpha$. In the recommended setting $b=2$ which shows that the cost for Cuckoo filters is approximately $1.05 \log_2(1/\epsilon)$, considerably lower than the Bloom filter's $1.44 \log_2(1/\epsilon)$.

Overall, Cuckoo filters offer various improvements to Bloom filters, the biggest of which is the ability to delete elements. They have  improved efficiency and can be further enhanced with additional tricks to save space. In terms of real-world applicability, Bloom filters have extended use-cases in the real world, owing to their simplicity and efficiency. The number of case studies where Cuckoo filters have been applied in the real world is lower, but growing.


### References
[1] Pagh, A., Pagh, R. and Rao, S. S. [An Optimal Bloom Filter Replacement](https://www.itu.dk/people/pagh/papers/bloom.pdf) Proceedings of the Sixteenth Annual ACM-SIAM Symposium on Discrete Algorithms, pp. 823–829 (2005).  
[2] Goel, A. and Gupta, P. [Small subset queries and bloom filters using ternary associative memories, with applications](https://web.stanford.edu/~ashishg/papers/inverted.pdf) ACM SIGMETRICS Performance Evaluation Review, 38: 143, CiteSeerX 10.1.1.296.6513, doi:10.1145/1811099.1811056 (2010).  
[3] Swamidass, S. J. and Baldi, P. [Swamidass, S. Joshua; Baldi, Pierre (2007), "Mathematical correction for fingerprint similarity measures to improve chemical retrieval](https://pubmed.ncbi.nlm.nih.gov/17444629/), Journal of Chemical Information and Modeling, 47 (3): 952–964, doi:10.1021/ci600526a, PMID 17444629 (2007).  
[4] Fan, B. et al. [Cuckoo filter: Practically better than Bloom](https://dl.acm.org/doi/pdf/10.1145/2674005.2674994). Proc. 10th ACM International on Conference on Emerging Networking Experiments and Technologies (CoNEXT '14). Sydney, Australia. pp. 75–88 (2014).