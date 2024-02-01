---
layout: post
title: Trends in Diffusion
date: 2023-01-12 07:00:00 +0200
tags: [ai]
# excerpt_separator: <!--more-->
---

Diffusion models have take the world by storm. They have proved able to learn complicated distributions with impressive accuracy, enough to have real-world general-purpose utility. Their widespread use in text-to-image models is now evident and, interestingly, is spreading to many other problem settings. I have purposefully waited a quite some time for the hype to settle down. But now, when expectations are more realistic, it's time to explore these curious models and the real impact they have on the current state of deep learning.

To begin, one should realize that denoising is intrinsically tied to generation. Adding noise to the data in most cases permanently destroys parts of the sample. If the scale of the noise is too big, at some point it overwhelms the useful signal rendering the resulting noisy sample indistinguishable from randomness. But in the reverse process of denoising the sample, you still have to produce those features which have been corrupted. Basic denoising methods such as mean or median filtering do not learn and hence the quality of their results is bounded by the noise levels. But other methods do learn. And if the noise level are overwhelming, to the point where you don't see most of the clean features, the process of denoising becomes more and more like generation. This is the high-level intuition behind diffusion - we define a process which adds noise to the data, called the *forward process*, and train a parametric model to denoise it, this being the *reverse* process. At test time, we feed random noise to the model, which being trained to denoise *anything*, will transform this noise to a sample from the origin data distribution.

Suppose we have a training dataset of samples and the underlying data distribution is $\mathcal{D}$. The whole diffusion pipeline can be applied independently across all samples. For that reason, let's consider a single sample $\textbf{x} \sim \mathcal{D}$. We can define a stochastic process which, at each step, adds noise to it. For simplicity, assume we add Gaussian noise independently to each dimension of the sample. If $\textbf{x}$ is an image, we'd add independent noise to the intensity of each pixel. If $\textbf{x}$ is a point in some geometric space, then we add noise to its coordinates. If $\textbf{x}$ represents a sample with physically-meaningful dimensions, we simply add noise to their measurements.

Doing this for multiple steps, we get a discrete random walk. One commonly and highly practical example definition for the stochastic process governing it is:

$$
\begin{aligned}
\textbf{x}_{t+1} & = \sqrt{1 - \beta_{t+1}}\textbf{x}_t + \epsilon_{t+1} \\
\epsilon_{t+1} & \sim \mathcal{N}(0, \beta_{t+1} \textbf{I}) \\
\Rightarrow \textbf{x}_{t+1} & \sim \mathcal{N} \big(\sqrt{1 - \beta_{t+1}} \textbf{x}_t, \beta_{t+1} \textbf{I}\big).
\end{aligned}
$$

Here $\textbf{x}\_0$ is the clean sample. The index $t$ indicates the time step for the random walk, which is typically limited to some upper range $T$. The process is parameterized by a sequence $\beta\_1, ..., \beta_T$ - usually some monotone function in $[0, 1]$. The previous noisy sample $\textbf{x}\_{t-1}$ is scaled by $\sqrt{1 - \beta\_{t}}$ which pushes it towards $0$. If $\textbf{x}$ is properly scaled, the added noise is independent of its scale of values, which is convenient.

This exact process is useful because it allows for a close-form calculation for the resulting distribution of $\textbf{x}_t$ after $t$ total steps. Thus, to compute $\textbf{x}\_{t+2}$ from $\textbf{x}\_t$ one does not need to simulate the process for two steps but can use appropriate formulas to get the distribution at $t+2$ directly:

$$

\begin{aligned}

\textbf{x}_{t+2} &= \sqrt{1 - \beta_{t+2}} \textbf{x}_{t+1} + \sqrt{\beta_{t+2}} \epsilon_{t+2} \\
& = \sqrt{1 - \beta_{t+2}} \big (\sqrt{1 - \beta_{t+1}} \textbf{x}_{t} + \sqrt{\beta_{t+1}} \epsilon_{t+1} \big) + \sqrt{\beta_{t+2}} \epsilon_{t+2} \\
&= \sqrt{1 - \beta_{t+2}} \sqrt{1 - \beta_{t+1}} \textbf{x}_{t} + \sqrt{1 - \beta_{t+2}} \sqrt{\beta_{t+1}} \epsilon_{t+1} + \sqrt{\beta_{t+2}} \epsilon_{t+2} \\
& \sim \mathcal{N} \Big (\sqrt{\prod_{i = 1}^2 (1 - \beta_{t+i})}\textbf{x}_t, \ \big(1 - \prod_{i=1}^2 (1 - \beta_{t+i}) \big)\textbf{I} \Big).


\end{aligned}

$$

In general, for any $t$ the distribution is given by

$$
\textbf{x}_{t} \sim \mathcal{N} \Big (\sqrt{\prod_{i = 1}^t (1 - \beta_{i})}\textbf{x}_0, \ \big(1 - \prod_{i=1}^t (1 - \beta_{i}) \big)\textbf{I} \Big).
$$



To add:
1. Marigold
2. Stable diffusion
3. DiffusionDet and others.
4. Diffusion for 3D pose estimation.
5. Stable-diffusion XL Turbo -->



