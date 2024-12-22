---
Title: Test-time compute
Date: 2024-12-18 07:00:00 +0200
Tags: rl
slug: test_time_compute
---

Some ideas are stirring. A few days ago Ilya Sutskever said at Neurips, paraphrasing, that we are running out of high-quality human generated text data with which to train LLMs. As a result, the pre-training paradigm of scaling up model and dataset sizes cannot go on forever. Performance of pure LLMs seems to be plateauing. The scaling hypothesis, which says that given a suitable architecture, one that sufficiently mixes all the features together, it is only a matter of scaling up training data and model size in order to get arbitrarily good, even superhuman, performance. Is this the case? It's hard to say. But a more important question is: if it plateaus, at what level will it do so? People who argue against the scaling hypothesis believe that intelligence depends on a critical highly-sought algorithm that we need to find. It may not be precisely an architecture, but it is a *design* that we are currently missing.

But here's the thing. In the long run it has been empirically shown that *computation* is the main driver behind a model's performance. Not any special algorithms or designs that bring problem-specific human knowledge into the model, just computation. That's the [bitter lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html). And to quote Rich Sutton, *Search and learning are the two most important classes of techniques for utilizing massive amounts of computation in AI research*. They are the drivers of long term performance.

**Learning** is obviously needed, as it allows us to solve a new set of problems - those which are hard to verify. Suppose I give you an image of a dog and ask you if it's a Labrador. How would you verify your answer? It's unclear. If you can't even verify, is recognition NP-complete? It doesn't fit neatly into a well-defined complexity class. To verify a recognition problem, you have to rely on visual patterns *learned* from previous image-label captions. So learning can be considered fundamental.

What about **search**? Naturally, many computational tasks - e.g. travelling salesman, shortest path, knapsack, chess, Go, optimal policy - require searching. You can't get good performance unless you search. And in ML this often leads to test-time compute, the idea that you will perform additional computations at test time, in the form of search, to improve your estimate on this problem instance, all without changing the model's parameters learned at train time. MCTS and various kinds of LLM prompting are examples here. Note that this is not a new idea. People have been doing planning and test-time augmentations, which are different forms of the same approach, for a long time now.

In general, solving tasks using reasoning boils down to proposing full- or partial solutions and evaluating them. Thus, we need an actor and a critic. And we need both to be very accurate so that good solutions are generated and recognized at the same time. A common way to search is called **searching against a verifier**. The idea is quite simple: we generate a bunch of candidate partial answers and evaluate them using a verifier model. The full solution is then constructed from the partial candidates.

Consider the following special cases:

- A single *reactive* answer is produced. This is fast, often inaccurate, and doesn't need a verifier.
- Majority voting - the model generates multiple final answers and the most common one is selected. This is sometimes called self-consistency [1]. It works if you increase the number of generated answers sufficiently, but beyond a number performance saturates.
- Best-of-$N$: Generate $N$ complete answers, score them with a verifier and return the best one.

The verifier can score either a whole solution, in which case it's called an *outcome reward model* (ORM), or a partial one, which we call a *process reward model* (PRM). If we are constructing the solution iteratively, similar to chain-of-though [2], we needs to aggregate the rewards for one whole solution across all of its steps, typically by taking the minimum or the last reward. PRMs are trained on specific datasets where the solutions to various reasoning problems are broken down to individual steps, so that the model can learn which intermediate steps are good and which bad [3].

Beyond the best-of-$N$ option, one can do *beam search*, a form of tree search, to iteratively build the final solution. This is very similar to how beam search can be used in the LLM inference process, where it works as follows:

1. At the beginning, the model generates a distribution over its vocabulary, which is of size $V$. We select the top $k$ most likely next tokens and discard the rest. The selected tokens are stored along with their log probabilities, or in general their rewards, into a small datastructure representing the *beam*.
3. At the next step, for each token in the beam we generate the next $V$ candidates. Thus, there are $kV$ total candidates.
4. We compute all of their log probabilities, and again keep the top $k$ tokens.
5. Repeat steps 3-4 until a stopping criterion is reached, usually `[EOS]` or maximum depth.

Keeping only the top $k$ bounds the memory requirements while sacrificing completeness - the guarantee that the best solution will be found. Selecting the top $k$ solutions at every $n$-th step is impractical as memory scales exponentially, as $O(kV^n)$. Similar to how beam search is used for generation, it can be used for step-by-step reasoning. Here the model generates entire "partial solutions" and we keep only the top $k$ at any time. Instead of the log probability, one uses the PRM. The model is purposefully instructed to think step-by-step and to delimit the individual parts of the solution, so they can be scored by the reward model.

<figure>
    <img class='big_img' src="/images/test_time_search_strategies.png" alt="Test time search strategies" width="1200">
    <figcaption> Figure 1: Test time search strategies. Best-of-$N$ generates $N$ full solutions and uses a verifier to select the best one. Beam search does tree search with bounded memory. Lookahead search assesses each proposed step according to the verifier score of its $k$-step continuation. Image taken from [4].</figcaption>
</figure>

Now, turns out there is no search method that performs best across all problems. Accoding to Google's large scale experiments [4], beam search tends to perform best on more difficult problem, while best-of-$N$ performs best on simple ones. Thus, if one can predict problem difficulty beforehand, it would be possible to select the best search strategy given a fixed compute budget. This is called а *test-time compute optimal scaling strategy* and Google have shown that adopting it can decrease compute by a solid factor compared to baselines like best-of-$N$ while holding performance fixed. Importantly, for certain easy and medium difficulty questions, test-time compute can easily make up for a lack of pretraining. On the contrary, for very difficult or specific questions where specific *knowledge* is required, pretraining will be more useful.

### References
[1] Wang, Xuezhi, et al. [Self-consistency improves chain of thought reasoning in language models.](https://arxiv.org/abs/2203.11171) arXiv preprint arXiv:2203.11171 (2022).   
[2] Wei, Jason, et al. [Chain-of-thought prompting elicits reasoning in large language models.](https://proceedings.neurips.cc/paper_files/paper/2022/hash/9d5609613524ecf4f15af0f7b31abca4-Abstract-Conference.html) Advances in neural information processing systems 35 (2022): 24824-24837.   
[3] Lightman, Hunter, et al. [Let's verify step by step.](https://arxiv.org/abs/2305.20050) arXiv preprint arXiv:2305.20050 (2023).   
[4] Snell, Charlie, et al. [Scaling llm test-time compute optimally can be more effective than scaling model parameters.](https://arxiv.org/abs/2408.03314) arXiv preprint arXiv:2408.03314 (2024).   

