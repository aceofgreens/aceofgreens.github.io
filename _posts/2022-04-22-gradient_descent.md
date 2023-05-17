---
layout: post
title: Run Away From the Gradient!
date: 2023-04-22 07:00:00 +0200
tags: [cs, ai]
# excerpt_separator: <!--more-->
---

Gradient descent is by far the most dominant optimization algorithm in AI. It has proven itself capable of training even the biggest and baddest models out there - multi-billion parameter LLMs, small networks with complicated forward passes, and anything in between. It's the best optimization algorithm we have right now. It's not very biologically realistic, but it compensates by being able to train those models which can simulate biological realism. And the idea of simply following the steepest direction is as beautiful as it gets. Here we'll explore some of the most widely used deep learning optimizers.

Gradient descent works by calculating the gradient (partial derivatives) of the loss function with respect to each parameter. The gradient gives the direction of the steepest increase in the function, and the algorithm updates the parameters by taking steps in the opposite direction of the gradient, which represents the steepest decrease in the function. This process is repeated iteratively until convergence is reached, such as when the absolute difference of the parameters from two sequential updates falls below some small value, or a stopping criterion is met, typically a maximum number of iterations.

Consider the following two-dimensional [Rosenbrock function](https://en.wikipedia.org/wiki/Rosenbrock_function) which can be considered as a testing example:

$$
F(x, y) = (a - x)^2 + b(y - x^2)^2. \\ 
$$

It is common to set $a=1$ and $b=100$, after which the single global minimum is found at $(1, 1)$. The contour plot is shown in Figure 1. This function is useful for testing optimization algorithms because the global minimum is found in a very flat and long valley. Reaching this valley, but moving along it is difficult because the gradient is very weak there.
<figure>
    <img class='img' src="/resources/rosenbrock.png" alt="Rosenbrock" width="1200">
    <figcaption>Figure 1: The Rosenbrock function for testing optimization algorithms. The left plot shows the contour of the function for various levels. The orange star shows the minimum of the function. The right plot shows the function's corresponding 3D surface plot.</figcaption>
</figure>

**Gradient descent.** Let's rename $(x, y)$ with $\theta = (\theta_1, \theta_2)$ to better indicate that $(x, y)$ are the parameters $\theta$ that we are optimizing over. We write the gradient evaluated at $\theta_t$ as $\nabla_\theta F(\theta_t)$. Then, standard gradient descent updates $\theta$ by taking a small step in the direction of the negative gradient:

$$
\theta_{t+1} = \theta_t - \eta \nabla_\theta F(\theta_t)
$$

Here $\theta_t$ are the parameters at iteration $t$, which for the Rosenbrock function includes both $x$ and $y$. We can refer to them individually using the notation $\theta_{t, i}$ where $i \in \\{ 1, 2 \\}$. $\eta$ is the *learning rate*, also called the *step size*, and contributes to how big the change in the parameters is. The other thing which determines the change is the gradient $\nabla_\theta F(\theta_t)$ which causes large updates in regions where the loss landscape is steep and small updates otherwise. If the learning rate is sufficiently small, following the negative gradient will eventually converge to a local minimum. If the learning rate is large, the parameters may diverge to infinity or may start oscillating in a limit cycle.

In standard gradient descent the learning rate is constant both across iterations $t$ and across individual parameters $i$. This setup is very simple but unfortunately has significant drawbacks. For functions which are steep along one direction, but flat along another, gradient descent will typically lead to very slow movement along the flat direction. This is the case with the Rosenbrock function. Our estimates reach the valley within just a few steps but after that the updates become tiny. Mathematically, the Hessian, the matrix of second derivatives, which shows the curvature in the neighborhood of the current point, has very different eigenvalues. One of them is very small, showing that the curvature of the loss landscape changes very slowly along the first eigenvector, in the direction of the minimum. And the other eigenvalue is very large (even hundreds of times larger), showing that the curvature changes rapidly in the transverse direction, along its corresponding eigenvector.

**Adagrad.** From this it seems that we need a method which can adapt the individual learning rate depending on the parameter. [Adagrad](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#AdaGrad) was the first to propose such a modification.


$$
\begin{cases}
\begin{align}
\theta_{t+1, i} & = \theta_{t,i} - \frac{\eta}{\sigma_{t,i}} g_{t, i} \\

\sigma_{t,i} &= \sqrt{\frac{1}{t+1} \sum_{\tau = 0}^{t} g_{t,i}^2} \\
g_{t,i} &= \nabla_{\theta_{t,i}} F(\theta_t)
\end{align}
\end{cases}
$$

Here the idea is to divide the learning rate $\eta$ by a parameter- and time-dependent variable $\sigma_{t,i}$ which scales the updates applied to each parameter. We keep the cumulative sum of the squared derivative of each parameter as the number of iterations grows. For parameters whose gradient is large or dense (frequently non-zero) this sum will increase and hence the learning rate for that parameter, after dividing by the square root of the cumulative sum, will be decreased. On the other hand, for parameters whose gradients are sparse (contain mostly zeros), the cumulative sum will not increase by relatively less, and hence the learning rate will be larger.

Empirically, it has been noted that Adagrad works particularly well for problems where there are sparse gradients. This may occur when the inputs are sparse, when we are using sparsity-inducing [activations](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) or [losses](https://en.wikipedia.org/wiki/Lasso_(statistics)), or when the outputs are sparse. 

**RMSProp.** That being said, one problem is that in a non-convex function the learning rate may decay too rapidly due to the accumulation of the gradients. If we are in one basin of attraction in the loss landscape, it is reasonable to want to forget the gradients collected from different regions. One improvement proposed in 2012, is Hinton's *Root Mean Squared Propogation* ([RMSProp](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#RMSProp)) optimizer:

$$
\begin{cases}
\begin{align}
\theta_{t+1, i} & = \theta_{t,i} - \frac{\eta}{\sigma_{t,i}} g_{t, i} \\

\sigma_{t,i} &= \sqrt{ \alpha \sigma_{t-1, i}^2 + (1 - \alpha) g_{t,i}^2} \\
g_{t,i} &= \nabla_{\theta_{t,i}} F(\theta_t)  \\
\sigma_{0, i} &= | g_{0, i} |
\end{align}
\end{cases}
$$

In this variation $\sigma_{t,i}$ is updated using a weighted average of the past learning rate modifiers $\sigma_{t-1,i}$ and the current derivative $g_{t,i}$, i.e. $\sigma_{t} = \sqrt{\alpha \sigma_{t-1}^2 + (1 - \alpha) g_t^2}$ (note that $g_t$ is a vector, while $g_{t,i}$ is a scalar). Since $\alpha \in (0,1)$, the weighted average ensures that some part of the previous gradients is forgotten, which also prevents the fast learning rate decay problem that Adagrad has.

Consider what happens with RMSProp when we enter the flat valley in our test function. At some point, when the previous gradients outside of the valley are forgotten, the current gradients will be $g_{t} = (a, b)$ and the previous sigma will be $\sigma_{t-1} = (\| a \|, \|b \|)$. Then, as a result, the current sigma will be $\sigma_{t} = (\|a\|, \|b\|)$ and the update will be $-\eta (a, b)/(\|a\|, \|b\|) = -\eta (\text{sgn}(a), \text{sgn}(b))$. If the valley is symmetric in the direction perpendicular to the gradient, it may happen that at the next iteration the update is the same, except the signs will be reversed. This causes oscillation in the parameter trajectory. The parameters will still move in the right direction, but they will oscillate from side to side, reducing the rate of convergence.

**Momentum.** A separate improvement which is somewhat orthogonal to the discussion of the adaptive learning rate to different parameters is that of momentum, also known as the heavy ball method, by analogy with a ball which accelerates when it rolls downhill. The idea is that the parameters will now have a kind of velocity $\Delta \theta_t = \theta_t - \theta_{t-1}$, dampened by a parameter $0 < \alpha < 1$, which also acts as an exponential decay when it comes to forgetting previous velocities. The update is given by:

$$
\begin{cases}
\begin{align}
\theta_{t+1} &= \theta_t + v_t \\
v_t &= \alpha v_{t-1} - \eta \nabla_\theta F(\theta_t) \\
v_0 &= 0. 
\end{align}
\end{cases}
$$

In practice, momentum can speed up convergence significantly. In cases where the gradient is first steep and then flattens out, like in the Rosenbrock function, the parameters will continue to update by a lot after entering the flat region, and thus will cover a lot of distance in just a few steps. Of course, if the loss landscape is highly non-convex or jagged having too much momentum can cause the parameters to overshoot, similar to having a learning rate which is too large.

A further improvement is what's called *Nesterov momentum*. Here the entire update consists of two parts: first we make a big jump using the momentum $\alpha v_t$ and then perform a correction in the direction of the gradient $-\eta \nabla_\theta F(\theta_t + \alpha v_t)$ evaluated at the new location. Summing these two terms yields the full update:

$$
\begin{cases}
\begin{align}
\theta_{t+1} &= \theta_t + v_t \\
v_t &= \alpha v_{t-1} - \eta \nabla_\theta F(\theta_t + \alpha v_{t-1}) \\
v_0 &= 0.
\end{align}
\end{cases}
$$

Applying the gradient step after the momentum step acts as a kind of lookahead and works very well in practice. However, computing the gradient in a shifted position is a bit inconvenient. We can reparametrize in the following way. Let $u_t = \theta_t + \alpha v_t$. Then $u_t - \alpha v_t = \theta_t$ and $u_t - \alpha v_t + v_{t+1} = \theta_t + v_{t+1} = \theta_t + \alpha v_t - \eta \nabla_\theta F(u_t) = \theta_{t+1} = u_{t+1} - \alpha v_{t+1}$. After some simplification we get

$$
\begin{cases}
\begin{align}
u_{t+1} &= u_t - \alpha v_t + (1 + \alpha) v_{t+1} \\
v_{t+1} &= \alpha v_t - \eta \nabla_\theta F(u_t) \\
v_0 &= 0.
\end{align}
\end{cases}
$$

At this point $u_t$ can be simply renamed to $\theta_t$ again and we now have a version of the Nesterov momentum that does not require computing a shifted gradient. Compared to standard momentum, the Nesterov variant is can alleviate the overshooting that would result from setting the momentum parameter or the learning rate too large. By using information about the "future" gradient it can deal with oscillations somewhat better, converging faster to a minimum.

**Adam.** Combining adaptive gradients with momentum yields the most popular and widely used optimizer in AI right now - adaptive moment estimation, or Adam. Here, we'll keep a running estimate for the first and the second moment for the derivative of every single parameter. The running estimates are updated using an exponential decay, similar to RMSProp - $m_t = \beta_1 m_{t-1} + (1 - \beta_1) g_t$ for the first moment and $v_t = \beta_2 v_{t-1} + (1 - \beta_2) g_t^2$ for the second one.

The first thing to do is to unroll the estimates for $m_t$ and $g_t$ and obtain a closed form for them:

$$
\begin{align}
v_t &= \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \\ 
&= \beta_2^2 v_{t-2} + \beta_2(1 - \beta_2) g_{t-1}^2 + (1 - \beta_2) g_t^2 \\
&= \beta_2^3 v_{t-3} + \beta_2^2(1-\beta_2) g_{t-2}^2 + \beta_2(1 - \beta_2) g_{t-1}^2 + (1 - \beta_2)g_t^2 \\
&= (1 - \beta_2) \sum_{i = 0}^{t-1} \beta_2^i g_{t - i}^2.
\end{align}
$$

A similar expression holds also for $v_t$. Now, it can happen, and most often does, that the gradients $g_t$ are random. This occurs if one is using stochastic gradient descent or if the task itself is stochastic - for example optimizing the policy parameters of an agent operating in a stochastic environment. In that case we are interested in the expectation of our moments. If we assume that the gradients have a stationary distribution so that $\mathbb{E}[g_{t-1}^2] = \mathbb{E}[g_{t-2}^2] = ... \mathbb{E}[g_0^2]$, then for the expectation of the exponential moving average we get:

$$
\mathbb{E}[v_t] = (1 - \beta_2^t) \mathbb{E}[g_t^2].
$$

It's clear that by dividing $\hat{v}_t = v_t/(1 - \beta_2^t)$ is an unbiased estimator for $g_t^2$. The analogously bias-corrected $\hat{m_t} = m_t/(1 - \beta_1^t)$ acts as the momentum term which will add modify the behaviour of the parameters. Dividing the parameters by $\sqrt{\hat{v_t}}$ ensures that in steep regions of the loss landscape the step size will be decreased. Adam is then given by:

$$
\begin{cases}
\begin{align}
g_t &= \nabla_\theta F(\theta_t) \\
m_t &= \beta_1 m_{t-1} + (1 - \beta_1) g_t \\
v_t &= \beta_2 v_{t-1} + (1 - \beta_2) g_t^2 \\
\hat{m}_t &= m_t / (1 - \beta_1^t) \\
\hat{v}_t &= v_t / (1 - \beta_2^t) \\
\theta_{t + 1} &= \theta_t - \eta \frac{\hat{m}_t}{\sqrt{\hat{v}_t}}.
\end{align}
\end{cases}
$$

In practice the default hyperparameter values are $\beta_1 = 0.9$ and $\beta_2 = 0.999$. $\beta_1$ increases the effect that the acceleration from an initial steep gradient will have on the learning and it's a very useful parameter to tweak for loss landscapes which have wide flat regions. $\beta_2$ *roughly* controls how fast the step sizes of individual parameters are scaled with respect to changes in the curvature of the loss landscape.

It is common to use regularization alongside the original objective function - for example weight decay $\lambda {\lVert \theta_t \rVert}^2_2$. If we add the regularization term naively in the total loss function, then the regularization will enter the $m_t$ and $v_t$ terms and they will start interacting in strange ways. Instead, the gradient of the regularization term should be added separately as another additive component to the updates of $\theta_t$ directly. This prompts the AdamW (adaptive moment estimation with weight decay) algorithm which is quite popular as well.

**Radam.** Let's do some quick statistical analysis on the properties of Adam. In what follows it's useful to know that if $X \sim N(0, 1)$, then $X^2$ has a Chi-squared distribution with $1$ degree of freedom, $X^2 \sim \chi^2(1)$. Similarly, $1/X \sim \text{Inv}$-$\chi^2(1)$ - the inverse chi squared distribution.

Let's assume that the gradients have a normal distribution, i.e. $g_1, g_2, ..., g_t \sim N(0, \sigma^2)$. Then the inverse square of each gradient comes from the [scaled inverse chi squared distribution](https://en.wikipedia.org/wiki/Scaled_inverse_chi-squared_distribution), which is quite similar to the standard inverse chi squared distribution, $1/g_i^2 \sim \text{Scale-Inv}$-$\chi^2(1, 1/\sigma^2)$. And here is the problem, depending on some parameters, this distribution may have infinitely large variance. As a result, averaging the gradients may not really converge to the true gradients of the whole dataset and the steps we take initially may be in the wrong direction. We need to find a way to reduce the variance in the early stages of the training. This is the problem that the Radam optimizer tackles.

The adaptive learning rate in Adam comes from the $\frac{1}{\sqrt{\hat{v_t}}}$ term. Let's denote the square root of its inverse with $\psi(g_1, ..., g_t)$:

$$
\psi(g_1, ..., g_t) =  \sqrt{\frac{1 - \beta_2^t}{(1 - \beta_2) \sum_{i=0}^{t-1}\beta_2^i g_{t-i}^2}}.
$$ 

We can assume that this exponential moving average (EMA) is well approximated, at least early on, by a simple average (SMA). As a result, the distribution of the EMA will be approximately that of the SMA:

$$
p \Bigg (\sqrt{\frac{1 - \beta_2^t}{(1 - \beta_2) \sum_{i=0}^{t-1}\beta_2^i g_{t-i}^2}} \Bigg) = p \Bigg(\sqrt{\frac{t}{\sum_{i=1}^t g_i^2}} \Bigg).
$$

Since  $\frac{t}{\sum_{i=1}^t g_i^2} \sim \text{Scale-Inv}$-$\chi^2(t, 1/\sigma^2)$, we can also claim that $\psi^2 \sim \text{Scale-Inv}$-$\chi^2(\rho, 1/\sigma^2)$, for some parameter $\rho$. Now, the EMA is a good approximation of the SMA for some particular length $f(t, \beta_2)$ that makes the SMA have the same "center of mass" as the EMA. The degrees of freedom $\rho$ can be taken to be an estimate for the length $f(t, \beta_2)$. We can find $\rho$ as follows:

$$
\frac{(1 - \beta_2) \sum_{i=0}^{t-1}\beta_2^i g_{t-i}^2}{1 - \beta_2^t} = \frac{\sum_{i=1}^{f(t, \beta_2)} g_{t+1-i}^2}{f(t, \beta_2)} \Rightarrow f(t, \beta_2) = \rho_t = \frac{2}{1 - \beta_2} - 1 - \frac{2t\beta_2^2}{1 - \beta_2^t}.
$$

From now on, let's set $r_\infty = \frac{2}{1 - \beta_2} - 1$ as it's the highest value that $\rho_t$ can take. Now, it can be proved (here we take it for granted) that the variance of $\psi$ is minimal when $\rho_t = \rho_\infty$.

Since $\psi^2$ is distributed as a scaled inverse chi-square, we can actually compute the variance of $\psi$. To enforce consistent variance of $\psi$ throughout the training, we can multiply $\psi$ by some rectification term $r_t$ such that $\text{Var}(r_t \psi)$ is minimal - which occurs when $\rho_t = \rho_\infty$. Skipping the derivation, we have

$$
r_t = \sqrt{\frac{(\rho_t - 4)(\rho_t - 2) \rho_\infty}{(\rho_\infty - 4)(\rho_\infty - 2)\rho_t}}.
$$

So here's how Radam works. We approximate the EMA for the second moment of the gradients with a sufficiently long SMA that has a familiar distribution. At the beginning, $r_\infty$ is computed. Then, in step $t$ of the optimization process, Radam computes $\rho_t$ from which the variance of $\psi$ can be determined. If it's tractable, we multiply the learning rate by $r_t$ to obtain a small and consistent variance over the course of the training. If it's intractable, which happens when $\beta_2 < 0.6$, tough luck.

It's worth mentioning that this kind of enhanced optimizers is not the only way to deal with large variance early on. One can also start updating the parameters after a number of steps, so that $\psi$ has been computed from a sufficiently large number of samples. Additionally, one could adopt a *warmup* schedule on the learning rate, starting from a very small value and gradually increasing it to the desired level.






