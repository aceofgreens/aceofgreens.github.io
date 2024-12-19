---
Title: Test-time compute
Date: 2024-12-18 07:00:00 +0200
Tags: rl
slug: test_time_compute
---

Some ideas are stirring. A few days ago Ilya Sutskever said at Neurips that we are running out of high-quality human generated text data with which to train LLMs. As a result, the pre-training paradigm where we scale up model and dataset sizes cannot go on forever. Performance of pure LLMs seems to be plateauing. Тhe scaling hypothesis, which says that given a suitable architecture, one that sufficiently mixes all the features together, it is only a matter of scaling up training data and model size in order to get arbitrarily good, even superhuman, performance. Is this the case? No one knows. People who argue against the scaling hypothesis believe that intelligence depends on a critical highly-sought algorithm that we need to find. It may not be precisely an architecture, but it is a *design* that we are currently missing.

But here's the thing. In the long run it has been empirically proven that *computation* is the main driver behind a model's performance. Not any special algorithms or designs that bake it human knowledge into the model, just computation. That's the [bitter lesson](http://www.incompleteideas.net/IncIdeas/BitterLesson.html). And to quote Rich Sutton, *Search and learning are the two most important classes of techniques for utilizing massive amounts of computation in AI research*.

Learning is obviously needed, as it allows us to solve completely new problems, even those which are hard to verify. If I give you an image of a dog and ask you if it's a Labrador, how would you even verify your answer? It's unclear. If you can't even verify, is recognition NP-complete? Not really, it doesn't fit into these well-defined computational classes. To verify a recognition problem, you have to rely on visual patterns *learned* from previous image-label captions. So learning can be considered fundamental.

What about search? Naturally, many computational tasks - e.g. travelling salesman, shortest path, knapsack, chess, Go, optimal policy - require searching. You can't get good performance unless you search. And in ML this often leads to test-time compute, the idea that you will perform more computations at test time to improve your estimate without changing the model's parameters learned at train time. MCTS and many kinds of LLM prompting are examples here.

In general, solving tasks using reasoning boils down to proposing full- or partial solutions and evaluating them. Thus, we need an actor and a critic. And we need both to be very accurate so that good solutions are both generated and recognized to be good.