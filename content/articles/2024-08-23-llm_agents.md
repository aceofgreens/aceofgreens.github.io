---
Title: LLM Agents
Date: 2024-08-23 07:00:00 +0200
Tags: ai, rl
slug: llm_agents
---

LLM agents are systems where a LLM is integrated with other components that allow it to better plan or act in a more autonomous manner. Recently, the term *agentic design patterns* has been used to describe the particular solutions that go in this direction. Given that LLMs have now been used for all kinds of things - solvers, planners, schedulers - the question of how to extend them to real-world tasks requiring more autonomy is ever more pertinent.

A core aspect of language modeling is that many things, including facts, questions, tasks, goals, and answers can be expressed as language. Thus, language provides a unified interface to all of these. And when we build a big model, trained on internet-scale datasets containing high-quality data, the model can be finetuned to respond to questions, write code, or otherwise start to generalize across tasks and responses. At inference time, LLMs are *kind of* agentic, because being autoregressive, their future outputs depend on their past outputs, in other words their predictions are consequential. Then, the appeal for using their autoregressive token processing architectures as general reasoning engines should be evident.

Agentic LLMs wrap the actual language model into a bigger software system that provides more capabilities. In typically consists of:

- A *memory* module that stores various kinds of memories, which is useful for problem solving,
- A *planning* module to iteratively refine the predictions of LLMs,
- An *action* module which allows the LLM to act in the world, for example by using tools, executing code, making choices, or calling APIs.

### Memory

**RAG**. The current dominant approach to handling factual memories is retrieval-augmented generation. Here the idea is that facts will not be stored in the model's weights, but in an external authoritative database which will be queried and referenced by the model in order to produce a response. Hooking up the LLM to a database like this is useful because it allows for the easy insertion, deletetion, and mutation of facts without retraining the model. It also largely eliminates hallucinations since the model does not have to come up with the facts, but only has to retrieve them from the database and summarize them.

The idea has been floating at least since 2017 [1]. The main system takes the user query, encodes it and passes it to a retriever module which interacts with the database. All the documents from the database have been encoded previously and the system supports an operation that finds the relevant documents given the query. Once we retrieve the relevant documents, the language model reads and summarizes them. Compared to mundane user tasks, here it's beneficial to have *very* large context, so that the model can read all the information from the retrieved documents.

**Retrieval**. For retrieving relevant documents, different schemes exist:

- $\text{tf-idf}$ [2], a classic approach uses two terms: the term-frequency $\text{tf}$, which measures how often a term occurs in a document, and inverse document frequency $\text{idf}$, which is the inverse of how common a term is across all documents. For all documents and terms, say $D$ and $T$, we compute a matrix of shape $(D, T)$ which contains the multiplication of the $\text{tf}(t, d)$ and $\text{idf}(t, D)$. This number is high for those terms and documents for which the term is specific and appears only inside them and in no other documents. Then, we compute $\text{tf}(t, \text{query})$, which is a vector, and match it with $\text{idf}(t, D)$ from which we obtain the closest neighboring documents from the database. 
- Dense vectors are more flexible because they can match by term semantics rather than exact wording, which allows for answering questions which can be potentially unspecified [3]. Here we encode the documents using some model and compute a simple cosine similarity between the query and the documents. This allows finetuning the retrieval based on downstream tasks. 
- Search engines can also be used for retrieval [4]. Their benefit is that they can use additional information such as recency, authorship, page ranks, or other metadata. 

With learnable document encodings and a learnable retriever, people have fine tuned entire RAGs in an end-to-end manner, even along with the LLMs [5, 6].

### Planning


### Actions






### References
[1] Chen, D. [Reading Wikipedia to answer open‐domain questions.](https://arxiv.org/abs/1704.00051) arXiv preprint arXiv:1704.00051 (2017).   
[2] Sparck Jones, Karen. [A statistical interpretation of term specificity and its application in retrieval.](https://www.emerald.com/insight/content/doi/10.1108/eb026526/full/html) Journal of documentation 28.1 (1972): 11-21.   
[3] Lee, Kenton, Ming-Wei Chang, and Kristina Toutanova. [Latent retrieval for weakly supervised open domain question answering.](https://arxiv.org/abs/1906.00300) arXiv preprint arXiv:1906.00300 (2019).   
[4] Lazaridou, Angeliki, et al. [Internet-augmented language models through few-shot prompting for open-domain question answering.](https://arxiv.org/abs/2203.05115) arXiv preprint arXiv:2203.05115 (2022).   
[5] Guu, Kelvin, et al. [Retrieval augmented language model pre-training.](https://proceedings.mlr.press/v119/guu20a.html?ref=https://githubhelp.com) International conference on machine learning. PMLR, 2020.   
[6] Shi, Weijia, et al. [Replug: Retrieval-augmented black-box language models.](https://arxiv.org/abs/2301.12652) arXiv preprint arXiv:2301.12652 (2023).   



 
