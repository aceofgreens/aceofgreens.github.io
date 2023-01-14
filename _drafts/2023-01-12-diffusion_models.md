---
layout: post
title: Text-to-Image Diffusion
date: 2023-01-12 07:00:00 +0200
tags: [ai]
# excerpt_separator: <!--more-->
---

Diffusion models have take the world by storm. They have proved able to learn complicated distributions in sufficient details, enough to have real-world general-purpose utility. Their widespread use in text-to-image models is now evident. I have purposefully waited a few months for the hype to settle down. Now when expectations are more realistic, it's useful to delineate the real impact they will have on society. To anticipate, I believe text-to-imagemodels regardless of whether they operate with diffusion or not, have brought about a change toward more democratic, and less elitist visual art. This post explores the inner workings of diffusion models and makes an opinionated claim on their societal benefits.

Suppose we have a training dataset of $N$ samples, $\textbf{x}_1, ..., \textbf{x}_N$ and the underlying data distribution is $\mathcal{D}$. We can define a stochastic process which, at each step, adds noise to the samples. For simplicy, assume we add Gaussian noise independently to each dimension of the samples. If $\textbf{x}_i$ is an image, we'd add independent samples from $\mathcal{N}(0, \sigma)$ to the intensity of each pixel. If $\textbf{x}_i$ is a point in some geometric space, then we add noise to its coordinates. If $x_i$ represents a sample with physically-meaningful dimensions, we simply add noise to their measurements.

If we do this for multiple steps, we get a random walk, defined for a single sample $\textbf{x}_i$ as:

$$
\begin{aligned}
\tilde{x}_{t+1} & = \tilde{x}_t + \epsilon \\
\epsilon & \sim N(0, \sigma_t) \\
\tilde{x}_0 &= \textbf{x}_0.
\end{aligned}
$$
