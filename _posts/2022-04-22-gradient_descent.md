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

Let's rename $(x, y)$ with $\theta = (\theta_1, \theta_2)$ to better indicate that $(x, y)$ are the parameters $\theta$ that we are optimizing over. Then, standard gradient descent updates $\theta$ by taking a small step in the direction of the negative gradient:

$$
\theta_{t+1} = \theta_t - \eta \nabla_\theta F
$$

Here $\theta_t$ are the parameters at iteration $t$, which for the Rosenbrock function includes both $x$ and $y$. We can refer to them individually using the notation $\theta_{t, i}$ where $i \in \\{ 1, 2 \\}$. $\eta$ is the *learning rate*, also called the *step size*, and contributes to how big the change in the parameters is. The other thing which determines the change is the gradient $\nabla_\theta F$ which causes large updates in regions where the loss landscape is steep and small updates otherwise. If the learning rate is sufficiently small, following the negative gradient will eventually converge to a local minimum. If the learning rate is large, the parameters may diverge to infinity or may start oscillating in a limit cycle.

In standard gradient descent the learning rate is constant both across iterations $t$ and across individual parameters $i$. This setup is very simple but unfortunately has significant drawbacks. For functions which are steep along one direction, but flat along another, gradient descent will typically lead to very slow movement along the flat direction. This is the case with the Rosenbrock function. Our estimates reach the valley within just a few steps but after that the updates become tiny. Mathematically, the Hessian, the matrix of second derivatives, which shows the curvature in the neighborhood of the current point, has very different eigenvalues. One of them is very small, showing that the curvature of the loss landscape changes very slowly along the first eigenvector, in the direction of the minimum. And the other eigenvalue is very large (even hundreds of times larger), showing that the curvature changes rapidly in the transverse direction, along its corresponding eigenvector.

From this it seems that we need a method which can adapt the individual learning rate depending on the parameter. [Adagrad](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#AdaGrad) was the first to propose such a modification.


$$
\begin{align}
\theta_{t+1, i} & = \theta_{t,i} - \frac{\eta}{\sigma_{t,i}} \nabla_{\theta_i} F \\

\sigma_{t,i} &= \sqrt{\frac{1}{t+1} \sum_{\tau = t}^{t} g_{t,i}^2} \\
g_{t,i} &= \nabla_{\theta_{t,i}} F
\end{align}
$$

Here the idea is to divide the learning rate $\eta$ by a parameter- and time-dependent variable $\sigma_{t,i}$ which scales the updates applied to each parameter. We keep the cumulative sum of the squared derivative of each parameter as the number of iterations grows. For parameters whose gradient is large or dense (frequently non-zero) this sum will increase and hence the learning rate for that parameter, after dividing by the square root of the cumulative sum, will be decreased. On the other hand, for parameters whose gradients are sparse (contain mostly zeros), the cumulative sum will not increase by relatively less, and hence the learning rate will be larger.

Empirically, it has been noted that Adagrad works particularly well for problems where there are sparse gradients. This may occur when the inputs are sparse, when we are using sparsity-inducing [activations](https://en.wikipedia.org/wiki/Rectifier_(neural_networks)) or [losses](https://en.wikipedia.org/wiki/Lasso_(statistics)), or when the outputs are sparse. 

That being said, one problem is that in a non-convex function the learning rate may decay too rapidly due to the accumulation of the gradients. If we are in one basin of attraction in the loss landscape, it is reasonable to want to forget the gradients collected from different regions. One improvement proposed in 2012, is Hinton's *Root Mean Squared Propogation* ([RMSProp](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#RMSProp)) optimizer:

$$
\begin{align}
\theta_{t+1, i} & = \theta_{t,i} - \frac{\eta}{\sigma_{t,i}} \nabla_{\theta_i} F \\

\sigma_{t,i} &= \sqrt{ \alpha \sigma_{t-1, i}^2 + (1 - \alpha) g_{t,i}^2} \\
g_{t,i} &= \nabla_{\theta_{t,i}} F
\end{align}
$$

In this variation $\sigma_{t,i}$ is updated using a weighted average of the past learning rate modifiers $\sigma_{t-1,i}$ and the current derivative $g_{t,i}$, i.e. $\sigma_{t} = \sqrt{\alpha \sigma_{t-1}^2 + (1 - \alpha) g_t}$ (note that $g_t$ is a vector, while $g_{t,i}$ is a scalar). Since $\alpha \in (0,1)$, the weighted average ensures that some part of the previous gradients are forgotten, which also prevents the fast learning rate decay problem that Adagrad has.








