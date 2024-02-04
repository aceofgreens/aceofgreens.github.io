---
layout: post
title: 'Generative Models: Diffusion'
date: 2024-02-04 07:00:00 +0200
tags: [ai]
# excerpt_separator: <!--more-->
---

Diffusion models have take the world by storm. They have proved able to learn complicated distributions with impressive accuracy, enough to have real-world general-purpose utility. Their widespread use in text-to-image models is now evident and, interestingly, is spreading to many other problem settings. I have purposefully waited a quite some time for the hype to settle down. But now, when expectations are more realistic, it's time to explore these curious models and the real impact they have on the current state of deep learning.

To begin, one should realize that denoising is intrinsically tied to generation. Adding noise to the data in most cases permanently destroys parts of the sample. If the scale of the noise is too big, at some point it overwhelms the useful signal rendering the resulting noisy sample indistinguishable from randomness. But in the reverse process of denoising the sample, you still have to produce those features which have been corrupted. Basic denoising methods such as mean or median filtering do not learn and hence the quality of their results is bounded by the noise levels. But other methods do learn. And if the noise level are overwhelming, to the point where you don't see most of the clean features, the process of denoising becomes more and more like generation. This is the high-level intuition behind diffusion - we define a process which adds noise to the data, called the *forward process*, and train a parametric model to denoise it, this being the *reverse* process. At test time, we feed random noise to the model, which being trained to denoise *anything*, will transform this noise to a sample from the origin data distribution.

Suppose we have a training dataset of samples and the underlying data distribution is $\mathcal{D}$. The whole diffusion pipeline can be applied independently across all samples. For that reason, let's consider a single sample $\textbf{x} \sim \mathcal{D}$. We can define a stochastic process which, at each step, adds noise to it. For simplicity, assume we add Gaussian noise independently to each dimension of the sample. If $\textbf{x}$ is an image, we'd add independent noise to the intensity of each pixel. If $\textbf{x}$ is a point in some geometric space, then we add noise to its coordinates. If $\textbf{x}$ represents a sample with physically-meaningful dimensions, we simply add noise to their measurements.

Doing this for multiple steps, we get a discrete random walk. One commonly and highly practical example definition for the stochastic process governing it is:

$$
\begin{aligned}
\textbf{x}_{t+1} & = \sqrt{1 - \beta_{t+1}}\textbf{x}_t + \sqrt{\beta_{t+1}}\epsilon_{t+1} \\
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
\textbf{x}_{t} \sim \mathcal{N} \big (\sqrt{\bar{\alpha}_t}\textbf{x}_0, \ (1 - \bar{\alpha}_t )\textbf{I} \big),
$$

where we have set $ \alpha_t = 1 - \beta_t$ and $\bar{\alpha}\_t = \prod_{i=1}^t \alpha\_i $ for convenience. Another useful property is that under some mild conditions on the variance schedule $\beta\_i$, the distribution of $\textbf{x}\_t$ converges to an isotropic Gaussian as $t \rightarrow \infty$. More generally $\textbf{x}\_{1:T} \| \textbf{x}\_0$ is a Guassian process and hence also $\textbf{x}\_{t-1} \| \textbf{x}\_t, \textbf{x}\_0$ is also Gaussian. However, the quantity of interest $\textbf{x}\_{t-1} \| \textbf{x}_{t}$ is not Gaussian. It's approximately Gaussian if the $\beta\_i$ parameters are small. Crucially, the mean and standard deviation of this Gaussian depend on the whole dataset and this is where learning comes in.

So, we construct a neural network $p\_\theta$ that takes in $(\textbf{x}\_t, t)$ and outputs the mean and standard deviation of $\textbf{x}\_{t-1} \| \textbf{x}\_{t}$. By autoregressively calling our network, we get samples from the joint distribution $p\_\theta(\textbf{x}\_{0:T}) = p(\textbf{x}\_T) \prod_{t=1}^T p_\theta(\textbf{x}\_{t-1} \| \textbf{x}\_{t})$. Since we don't care about the intermediate samples, our only task is to learn the network parameters $\theta$ such that $p_\theta(\textbf{x}\_0) \approx p(\textbf{x}\_0)$. Similar to a VAE, one can use variational inference here.

So, $p(\textbf{x}\_0)$ is the observed target distribution, $p(\textbf{x}\_{1:T} \| \textbf{x}\_0)$ is the latent distribution. We denote the trainable model as $p\_\theta$ and hence its latent distribution is $p\_\theta(\textbf{x}\_{1:T} \| \textbf{x}\_0)$. Then,

$$
\begin{align*}
\ln p_{\theta}(\textbf{x}_0) &= \ln \int p_{\theta}(\textbf{x}_{0:T}) \frac{p(\textbf{x}_{1:T} | \textbf{x}_0)}{p(\textbf{x}_{1:T} | \textbf{x}_0)} d\textbf{x}_{1:T} \\
&= \ln \mathbb{E}_{\textbf{x}_{1:T} \ \sim \ p} \Big[\frac{p_\theta (\textbf{x}_{0:T})}{p(\textbf{x}_{1:T} | \textbf{x}_0)} \Big] \\
& \ge \mathbb{E}_{\textbf{x}_{1:T} \ \sim \ p} \Big[ \ln \frac{p_\theta (\textbf{x}_{0:T})}{p(\textbf{x}_{1:T} | \textbf{x}_0)} \Big] = \mathbb{E}_{\textbf{x}_{1:T} \ \sim \ p} \Big[ \ln p_\theta(\textbf{x}_{0:T}) - \ln p(\textbf{x}_{1:T} | \textbf{x}_0) \Big] \\

& \Rightarrow \mathbb{E}_{\textbf{x}_0 \ \sim \ p} \big[ \ln p_\theta (\textbf{x}_0)\big] \ge \mathbb{E}_{\textbf{x}_{0:T} \sim p} \big[\ln p_\theta (\textbf{x}_{0:T}) - \ln p (\textbf{x}_{1:T} | \textbf{x}_0)\big].
\end{align*}
$$

Thus, instead of maximizing the likelihood of the observed data, we maximize a lower bound, the ELBO. Now from the last expression we can pick out only those terms that depend on $\theta$. Given that $p_\theta(\textbf{x}_T) = \mathcal{N}(\textbf{0}, \textbf{I})$, we formulate the following loss function:

$$
\mathcal{L}(\theta) = \sum_{t = 1}^T \mathbb{E}_{\textbf{x}_{t-1}, \textbf{x}_t \sim p} \big[ - \ln p_\theta(\textbf{x}_{t-1} | \textbf{x}_{t} )\big]
$$

Now, we need $p\_\theta(\textbf{x}\_{t-1} \| \textbf{x}\_t)$ to be something easy to evaluate, like a Gaussian. But $\textbf{x}\_{t-1} \| \textbf{x}\_t$ does not have a Gaussian distribution, $\textbf{x}_{t-1} \| \textbf{x}\_t, \textbf{x}\_0$ does. So we need to have the model estimate $\textbf{x}\_0$. In practice, since $\textbf{x}\_0$ is related to $\textbf{x}\_t$ through the noise $\epsilon_t$,

$$
\textbf{x}_t = \sqrt{\bar{\alpha}_t} \textbf{x}_0 + \sqrt{1 - \bar{\alpha}_t} \epsilon_t \Longleftrightarrow \textbf{x}_0 = \frac{\textbf{x}_t - \sqrt{1 - \bar{\alpha}_t} \epsilon_t}{\sqrt{\bar{\alpha}}_t},
$$

so in fact we can have the network predict the noise, obtaining $\epsilon_\theta(\textbf{x}\_t, t)$. Once we have an estimate of the noise, we essentially have an estimate of $\textbf{x}\_0$ and in turn can evaluate $\textbf{x}\_{t-1} \| \textbf{x}\_t, \textbf{x}\_0$. The variance is usually fixed to some constant as predicting it introduces instability. The formula for the estimated mean is 

$$
\mu_{\theta}(\textbf{x}_{t-1} | \textbf{x}_t) = \frac{1}{\sqrt{\bar{\alpha}_t}} \big(\textbf{x}_t - \frac{1 - \alpha_t}{\sqrt{1 - \bar{\alpha}_t} \epsilon_t} \epsilon_{\theta}(\textbf{x}_t, t) \big).
$$

This is roughly how denoising diffusion probabilistic models (DDPM) work. At training time the network learns to estimate the noise. At test time, we start with a single sample $\textbf{x}\_T$ from the prior, a Gaussian, call the model to obtain $\epsilon\_\theta(\textbf{x}\_T)$, compute $\mu\_\theta(\textbf{x}\_{T-1} \| \textbf{x}\_T)$ analytically and sample $\textbf{x}\_{T-1}$ from the estimated distribution of $\textbf{x}\_{T-1} \| \textbf{x}\_T$. Repeat autoregressively until we get to $\textbf{x}\_0$.


### Score-Based Generative Modeling

There is another diffusion formulation which is quite intuitive - that of score matching. Given a distribution $p(\textbf{x})$, the score $s(\textbf{x})$ is simply the gradient of the log-likelihood, $\nabla_\textbf{x} \ln p(\textbf{x})$. It's an attractive quantity because it doesn't require calculating any untractable normalization constants. But how is it related to sample generation?

One usage of the score is in stochastic gradient Langevin dynamics (SGLD), a curious, perhaps even beautiful, method for sampling from physics/thermodynamics. Suppose we start from a sample $\textbf{x}\_0$. To, get a sample from the target distribution $p(\textbf{x})$ we can simply do log-likelihood ascent, with added noise injection:

$$
\begin{align}
\textbf{x}_t &= \textbf{x}_{t-1} + \frac{\delta}{2} \nabla_\textbf{x} \ln p(\textbf{x}_{t-1}) + \sqrt{\delta} \epsilon_t, \\
\epsilon_t & \sim \mathcal{N}(\textbf{0}, \textbf{I}).
\end{align}
$$

Overall this resembles very closely gradient ascent. As long as $t \rightarrow \infty$ and $\epsilon \rightarrow \textbf{0}$, $\textbf{x}\_t$ will be a sample from $p(\textbf{x})$. The added noise at each step is necessary, otherwise the sequence will converge to a local minimum and will depend on starting location. So if we train a model for the score, $s\_\theta(\cdot)$, we can just plug it in the Langevin equation and iterate to get a sample. This is the inference approach of score-based sample generation.

Now, it's useful to see also the case where the diffusion time is continuous. Suppose $t$ is continuous and in $[0, T]$. The forward process adding noise to the data can now be modeled as the SDE

$$
d\textbf{x} = f(\textbf{x}, t) dt + g(t) d\textbf{w},
$$

where $f(\textbf{x}, t)$ is the drift term, $g(t)$ is a diffusion term, and $\textbf{w}$ is a Weiner process. For simplicity, the diffusion term is a scalar, not depending on $\textbf{x}$. This is a general formulation. In general, it is a known mathematical fact that there exists a reverse diffusion process, modeled by a reverse SDE:

$$
d\textbf{x} = \big[ f(\textbf{x}, t) - g(t)^2 \nabla_\textbf{x} \ln p(\textbf{x}_t) \big] dt + g(t) d\bar{\textbf{w}}.
$$

Here $dt$ is a infinitesimal negative timestep and $\bar{\textbf{w}}$ is a Wiener process where time flows backward from $T$ to $0$. As we can see, if we have the score, we can reverse the process. Thus, to learn the score, we construct a network $s\_\theta$ that takes in $(\textbf{x}(t), t)$ and is trained to solve the following *simplified* objective

$$
\theta^{*} = \underset{\theta}{\arg\min} \ \  \mathbb{E}_t \Big[ \mathbb{E}_{\textbf{x}_0} \mathbb{E}_{\textbf{x}(t) | \textbf{x}(0)} \big[ {\lVert s_\theta(\textbf{x}(t), t) - \nabla_\textbf{x} \log p(\textbf{x}(t) | \textbf{x}(0)) \rVert}_2^2 \big] \Big].
$$

Note that here, depending on the exact SDE, $p(\textbf{x}(t) \| \textbf{x}(0))$ may or may not be computable efficiently. If the drift coefficients are affine, then this probability is Gaussian and can be computed easily. For more advanced ones, one can use Kolmogorov's forward equation or simply simulate it.

Consider the benefit of adding noise for training the score network. Without adding noise the ground-truth score can be evaluated only at the samples in the dataset. But the first sample $\textbf{x}(T)$ from the prior at test time may be very far from the data distribution. Hence, if you don't have data points around the space where your prior has high density your score estimate won't be accurate at those locations. To alleviate this, the forward diffusion effectively performs *annealing*. Adding the noise allows us to learn the score over a larger and more smooth region, covering the path from the data distribution to the prior one.

The DDPM model that we discussed above can written in both its discrete and continuous versions:

$$
\begin{align}
\textbf{x}_{t+1} &= \sqrt{1 - \beta_{t+1}}\textbf{x}_{t} + \sqrt{\beta_{t+1}} \epsilon_{t+1} \\
d\textbf{x} &= -\frac{1}{2} \beta(t) \textbf{x} dt + \sqrt{\beta(t)}d \textbf{w}.
\end{align}
$$

Other discrete diffusion formulations also have similarly-looking continuous SDEs. But once we have trained the score network, how do we actually generate a sample using the reverse SDE? Well, we use a numerical SDE solver like the Euler-Maruyama or the stochastic Runge-Kutta. These solvers discretize the SDE in tiny steps and iterate in a manner similar to Langevin dynamics, adding a small amount of noise at every step.

Importantly, it can be proved that the DDPMs and the score-based methods are *equivalent*. It takes some math to see this, but at the end one can reparametrize the DDPM to produce scores. The formulas and the loss function are adjusted accordingly. This produces a unified perspective - the network can use the noisy $(\textbf{x}\_t, t)$ to predict either $\textbf{x}\_0$, or $\epsilon_t$, or $\nabla\_\textbf{x} \log p(\textbf{x}\_t)$ - all will work, but will require different denoising formulas.


### Practical Considerations

Naturally, to be able to learn $\epsilon_t$, $\textbf{x}\_0$, or $\nabla_\textbf{x} \log p(\textbf{x}\_t)$, especially when $\textbf{x}$ is very high-dimensional, one needs to have a big model. Denoising architectures with skip connections, like U-Nets, or pure transformer-based approaches, for example for non-image data, are the go-to choice. 

Apart from model size, one needs to consider also the inference speed. With DDPMs you have to iterate from $T$ to $1$, which in practice is simply too slow. One straightforward approach is to simply denoise once every $S$ steps, for a total of $\lfloor T/S \rfloor$ denoising calls. Since the model has learned to produce a meaningful output for all $(\textbf{x}\_t, t)$, we are simply calling it $S$ times less. Another similar approach is given by denoising diffusion implicit models (DDIM), which requires some effort to fully understand, but it's worth it.

To reduce the number of iterations, one needs to come up with an inference process that simply uses less steps. The objective optimized by DDPM only depends on $p(\textbf{x}\_t \| \textbf{x}\_0)$, not on $p(\textbf{x}\_{1:T})$. In principle, there are many processes that have the same $p(\textbf{x}\_t \| \textbf{x}\_0)$, but may not be Markovian. This, in turn can be used to speed up the generation of new samples. One can consider the following:

$$
\begin{align}
p_\sigma &= p_\sigma(\textbf{x}_T | \textbf{x}_0) \prod_{t=2}^T p_\sigma(\textbf{x}_{t-1} | \textbf{x}_t, \textbf{x}_0) \\
p_\sigma(\textbf{x}_T | \textbf{x}_0) &= \mathcal{N}(\sqrt{\bar{\alpha}_T} \textbf{x}_0, (1 - \bar{\alpha}_T)\textbf{I}) \\
p_\sigma(\textbf{x}_{t-1} | \textbf{x}_t, \textbf{x}_0) &= \mathcal{N}(\sqrt{\bar{\alpha}_{t-1}} \textbf{x}_0 + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \cdot \Big(\frac{\textbf{x}_t - \sqrt{\bar{\alpha}_t}\textbf{x}_0}{\sqrt{1 - \bar{\alpha}_t}}\Big), \sigma_t^2 \textbf{I} ).
\end{align}
$$

Here $p\_\sigma(\textbf{x}\_t \| \textbf{x}\_0) = \mathcal{N}(\sqrt{\bar{\alpha}_t} \textbf{x}\_0, (1 - \bar{\alpha}_t) \textbf{I})$ which still matches DDPM in that it is easy to evaluate, however the "forward" process $p\_\sigma(\textbf{x}\_t \| \textbf{x}\_{t-1}, \textbf{x}\_0)$ is no longer Markovian. The quantity $\sigma$ is an important parameter that controls the stochasticity of the forward process. For one exact $\sigma$, we get DDPM, which is Markovian. If $\sigma_t = 0, \forall t$ the process becomes *deterministic*. Thus, DDIMs are a generalization of DDPMs because they support non-Markovian and even deterministic processes.

The generative model $p\_\theta$ is constructed similarly to $p\_\sigma$. Sampling $\textbf{x}\_{t-1}$ from $\textbf{x}\_t$ is calculated as:

$$
\textbf{x}_{t-1} = \sqrt{\bar{\alpha}_{t-1}} \Big( \frac{\textbf{x}_{t} - \sqrt{1 - \bar{\alpha}_t} \epsilon_\theta(\textbf{x}_t, t)}{\sqrt{\bar{\alpha}_t}} \Big) + \sqrt{1 - \bar{\alpha}_{t-1} - \sigma_t^2} \cdot \epsilon_\theta(\textbf{x}_t, t) + \sigma_t \epsilon_t.
$$

Notice how here to generate $\textbf{x}\_{t-1}$ you need to know both $\bar{\alpha}\_t$ and $\bar{\alpha}\_{t-1}$. This means that you can have irregularly spaced $\alpha\_t$ coefficients. Thus, DDIM allows one to define a forward process on only a small subset of timesteps from $\\{1, 2, ..., T\\}$, which in turns greatly speeds up the reverse generative process. It does not require retraining, just changing the reverse process.

Apart from DDIM, one can typically get a huge inference speed improvement by doing diffusion in a latent space, as opposed to for example the high dimensional sample space of images. In a latent diffusion model one uses an encoder, like a VQ-VAE or something similar, to map the clean input to a latent space. In the latent space we add noise and pass the noisy variable to a U-Net which denoises it. Subsequently, this variable is fed to a decoder which upsamples and decodes back into the modality of interest. It is common also to have additional modality-specific encoders for any data that will condition the diffusion process. A cross-attention block in the U-Net handles the conditioning.

This idea of latent diffusion is *incredibly* powerful. It allows diffusion to be used in, realistically, all kinds of contexts. Using separate encoders and decoders allows one to build multi-modal generative models that can condition one signal on any other and can produce any signal modality from any other.




To add:
1. Marigold
2. Stable diffusion
3. DiffusionDet and others.
4. Diffusion for 3D pose estimation. PoseDiffusion, etc.
5. Stable-diffusion XL Turbo -->



