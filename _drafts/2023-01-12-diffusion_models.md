---
layout: post
title: Text-to-Image Diffusion
date: 2023-01-12 07:00:00 +0200
tags: [ai]
# excerpt_separator: <!--more-->
---

Diffusion models have take the world by storm. They have proved able to learn complicated distributions in sufficient details, enough to have real-world general-purpose utility. Their widespread use in text-to-image models is now evident. I have purposefully waited a few months for the hype to settle down. Now when expectations are more realistic, it's useful to delineate the real impact they will have on society. To anticipate, I believe text-to-imagemodels regardless of whether they operate with diffusion or not, have brought about a change toward more democratic, and less elitist visual art. This post explores the inner workings of diffusion models and makes an opinionated claim on their societal benefits.

Suppose we have a training dataset of $N$ samples, $\textbf{x}_1, ..., \textbf{x}_N$ and the underlying data distribution is $\mathcal{D}$. We can define a stochastic process which, at each step, adds noise to the samples. For simplicity, assume we add Gaussian noise independently to each dimension of the samples. If $\textbf{x}$ is an image, we'd add independent noise to the intensity of each pixel. If $\textbf{x}$ is a point in some geometric space, then we add noise to its coordinates. If $\textbf{x}$ represents a sample with physically-meaningful dimensions, we simply add noise to their measurements.

Doing this for multiple steps, we get a random walk, defined for a single sample $\textbf{x}$ as:

$$
\begin{aligned}
\tilde{\textbf{x}}_{t+1} & = \sqrt{1 - \beta_{t+1}}\tilde{\textbf{x}}_t + \epsilon_{t+1} \\
\epsilon_{t+1} & \sim \mathcal{N}(0, \beta_{t+1} \textbf{I}) \\
\tilde{\textbf{x}}_0 &= \textbf{x}_0 \\
\Rightarrow \tilde{\textbf{x}}_{t+1} & \sim \mathcal{N}(\sqrt{1 - \beta_{t+1}} \tilde{\textbf{x}}_t, \beta_{t+1} \textbf{I}).
\end{aligned}
$$

Note that the index $t$ indicates the time step for the random walk. We purposefully scale the previous value by $\sqrt{1 - \beta_{t+1}}$ and the unit covariance matrix by $\beta_{t+1}$ to make the noise independent of the scale of values of $\textbf{x}$.

As it turns out, this setup is useful because it allows for a close-form calculation for the resulting distribution of $\tilde{\textbf{x}}_T$ after $T$ total steps.

$$

\begin{aligned}

\tilde{\textbf{x}}_{t+2} &= \sqrt{1 - \beta_{t+2}} \tilde{\textbf{x}}_{t+1} + \sqrt{\beta_{t+2}} \epsilon_{t+2} \\
& = \sqrt{1 - \beta_{t+2}} \big (\sqrt{1 - \beta_{t+1}} \tilde{\textbf{x}}_{t} + \sqrt{\beta_{t+1}} \epsilon_{t+1} \big) + \sqrt{\beta_{t+2}} \epsilon_{t+2} \\
&= \sqrt{1 - \beta_{t+2}} \sqrt{1 - \beta_{t+1}} \tilde{\textbf{x}}_{t} + \sqrt{1 - \beta_{t+2}} \sqrt{\beta_{t+1}} \epsilon_{t+1} + \sqrt{\beta_{t+2}} \epsilon_{t+2} \\
& \sim \mathcal{N} \Big (\sqrt{\prod_{i = 1}^2 (1 - \beta_{t+i})}\tilde{\textbf{x}}_t, \ \big(1 - \prod_{i=1}^2 (1 - \beta_{t+i}) \big)\textbf{I} \Big)


\end{aligned}

$$

