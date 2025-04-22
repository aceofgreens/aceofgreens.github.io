---
Title: Exogeneous Growth
Date: 2025-04-20 07:00:00 +0200
Tags: econ
slug: exogeneous_growth
---

Here we study the simplest economics growth model by Robert Solow and Trevor Swan. It is the basis over which many other models build upon and is quite easy to analyze, while providing useful insights. For example, it asserts that changes in saving only matter for the economy's transition path, not for its permanent growth rate. Yet, savings obviously determine consumption. So should we save more or less? The model also introduces key questions such as whether poor countries grow faster than richer ones, or whether physical capital can explain big differences in output across space and time. 

We are concerned with an economy's long term behaviour. This presupposes that individual macroeconomic fluctuations from year-to-year are not of interest. In fact, the main variable of focus is the output $Y(t)$ as a function of the production factors capital $K(t)$, labor $L(t)$, and technology $A(t)$. All of these depend on time $t$, but we'll often skip this notation for clarity. The mapping between inputs and outputs is given by a production function $F$, i.e. $Y = F(K, A, L)$.

If we assume that $F$ is increasing in $K$, $A$, and $L$, and they all grow exogeneously, this already implies a growth rate for $Y$. However, the generality and usefulness of the conclusions depend on the modeling setup. The assumptions of the Solow model hit a sweet spot in that regard because they are not the most unrealistic ones, but they do allow for some level of interesting insights.

We'll assume that $F$ has a [Cobb-Douglas](https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function) functional form, $Y(t) = F(K, AL) = K^\alpha (AL)^{1 - \alpha}$. The technology $A$ enters only through its multiplication with the labor $L$. The product $AL$ is called *effective labor*. This functional form also implies constant returns to scale, where e.g. doubling the inputs doubles the outputs, $F(xK, xAL) = xF(K, AL)$. Such constant returns are realistic for large economies where the gains from specialization have been exhausted.

Let's assume that $L$ and $A$ grow at constant rates $n$ and $g$ respectively. Thus, they are exogeneous and grow exponentially as time $t$ progresses:

$$
\frac{dL}{dt} = \dot{L}(t) = nL(t) \Rightarrow L(t) = L(0) e^{nt} \\
\frac{dA}{dt} = \dot{A}(t) = gA(t) \Rightarrow A(t) = A(0) e^{gt} \\
$$

A more interesting consideration is how capital changes from time to time. Suppose that households separate total income into consumption and saving and the saving gets channeled through the financial markets where it is converted to capital. Suppose also that capital depreciates at a constant rate $\delta$. Then the relationship for capital is

$$
\frac{dK}{dt} = \dot{K}(t) = Y(t) - C(t) - \delta K(t) = sY(t) - \delta K(t).
$$

Here $Y(t) - C(t)$ is the saving which in the Solow model is assumed to be a constant fraction $s$ of the total income $Y(t)$. Generally, capital increases by however much is saved and decreases according to the depreciation rate.

Now, to analyze the model more easily, we'll convert it into its *intensive* form, where the quantities of interest will now be expressed *per unit of effective labor*. Thus, output per effective labor is $Y/(AL) = y = F(K, AL)/(AL) = F(K/(AL), 1) = f(k)$ where we have introduced the variables $k=K/(AL)$ and $y=Y/AL$. For the Cobb-Douglas case we get a simple expression:

$$
\begin{align}
y &= f(k) = k^\alpha\\
y' &=  \alpha k^{\alpha - 1} > 0\\
y'' &= \alpha (\alpha - 1) k^{\alpha - 2} < 0,
\end{align}
$$

which shows diminishing marginal product of capital for the $k$ range of interest $\mathbb{R}_+$. A further important property is that the *Inada conditions* are satisfied, $\lim_{k \rightarrow 0} f'(k) = \infty$ and $\lim_{k \rightarrow \infty} f'(k) = 0$. This ensures that the dynamics have a stable point.

We know $\dot{K}$, but what is $\dot{k}$? This is the single most important equation for the Solow model because it determines the dynamics. From the quotient rule we get

$$
\dot{k}(t) = \frac{\dot{K}}{AL} - \frac{K}{(AL)^2}\left[ A\dot{L} + \dot{A}L \right] = sf\big(k(t)\big) - (n + g + \delta)k(t).
$$

To get to the last equation we've used the fact that $\dot{L}/L = n$ and $\dot{A}/A = g$. Now, the term $sf\big(k(t)\big)$ grows very fast initially (Inada condition) and but slows down at higher $k$ due to the diminishing marginal product. It grows like $O(k^\alpha)$. The term $(n + g + \delta)k$ grows like $O(k)$ and represents *break-even* investment - the amount needed to keep $k$ at the same level. The capital-per-unit-of-effective-labor $k$ is increasing when the actual investment $sf(k)$ is greater than the break-even investment, and decreases otherwise. The quantity at which $\dot{k} = 0$ is $k^\ast$ and it is a stable point to which $k$ converges.

Once $k$ converges to $k^\ast$ the trajectory of the variables is called the *balanced growth path*. Then:

- $L$ and $A$ grow at rates $n$ and $g$ by exogeneous definion;
- $k$ is constant at $k^\ast$ but $K = ALk^\ast$ grows at rate $n + g$;
- Output $Y$ grows at rate $n + g$, per-worker output $Y/L$ and capital $K/L$ grow at rate $g$.

Thus the Solow model implies that, regardless of its starting point, the economy converges to a balanced growth path a situation where each variable of the model is growing at a constant rate. On the balanced growth path, the growth rate of output per worker is determined solely by the rate of technological progress $g$.

We now turn to exploring the implication of this model. Specifically, what happens if the savings rate $s$ goes up. Intuitively, investment into capital $sf(k)$ goes up, and therefore the convergence point $k^\ast$ increases. Assuming we start from $k^\ast$ and $s$ increases, then suddenly actual investment becomes larger than break-even investment and $k$ starts to increase. Output grows at a rate higher than $n + g$. When the new equilibrium value of $k^\ast$ is reached, the growth rate of the economy becomes constant again. Similarly, a decrease in $s$ causes a *level effect* but not a *growth effect* in the economy. The only way to increase the growth rate of output per capita, which is $O(e^{gt})$, is through improvements in the technology $A(t)$.

<figure>
    <img class='small_img' src="/images/solow_growth2.svg" alt="Solow Growth" width="1200">
    <figcaption> Figure 1. Effects of an increase of the savings rate on investment. Break-even investment is given by a straight line, while actual investment depends on the savings rate. When it is increased, the actual investment curve is rescaled and equilibrium capital per unit of effective labor increases.</figcaption>
</figure>

Let's explore the effect of a rise in savings quantitatively. We know that $y^\ast = f(k^\ast)$. Therefore

$$
\frac{\partial y^\ast}{\partial s} = f'(k^\ast) \frac{\partial k^\ast}{\partial s}.
$$

The relationship between $k^\ast$ and $s$ is implicit, $sf(k^\ast) = (n + g + \delta)k^\ast$. Using implicit differentiation we take derivatives on both sides with respect to $s$, noting that $k^\ast$ depends on $s, n, g, \delta$, and rearrange to obtain first $\partial k^\ast / \partial s$, and then $\partial y^\ast / \partial s$: 

$$
\begin{align}
\frac{\partial k^\ast}{\partial s}  &= \frac{f(k^\ast)}{n + g + \delta - sf'(k^\ast)} \\
\frac{\partial y^\ast}{\partial s}  &= \frac{f'(k^\ast) f(k^\ast)}{n + g + \delta - sf'(k^\ast)}.
\end{align}
$$

In principle that's all we need. Yet, to make the last equation more interpretable, we'll derive elasticities. Remember that the elasticity of $x$ wrt $y$ is given by $\epsilon_{x,y} = dx/dy \times y/x$. We multiply $\partial y^\ast/ \partial s$ by $s/y^\ast$ and express the $s$ in terms of $k^\ast$. After some function wrangling one obtains

$$
\frac{s}{y^\ast} \frac{\partial y^\ast}{\partial s} = \frac{\alpha_K(k^\ast)}{1 - \alpha_K(k^\ast)}, \text{ where } \alpha_K(k^\ast) = k^\ast f'(k^\ast) / f(k^\ast).
$$

Here $\alpha_K(k^\ast)$ is the elasticity of the output wrt capital at $k=k^\ast$ and we've obtained an expression for the elasticity of output wrt the savings rate $s$ at $k=k^\ast$. Now, consider that if markets are perfectly competitive, firms rent capital until the marginal product of capital (MPK) becomes equal to the rental cost.

$$
Y = ALf(k) = ALf(K/AL) \Rightarrow \frac{\partial Y}{\partial K} = ALf'(K/AL)/AL = f'(k).
$$

The price of capital at $k=k^\ast$ is $f'(k)$ and the quantity is $k^\ast$. Hence, the share of money that goes to capital is given by $k^\ast f'(k^\ast)/f(k^\ast)$ which is precisely the elasticity $\alpha_K(k^\ast)$. In most countries the share of money paid to capital is about $1/3$. Hence under the assumption of perfect competition, the elasticity of output wrt savings is $1/2$. Thus if the savings rate is, say $20\%$, and it gets increased by $50\%$, to a level of $30\%$, the output per capita will increase only by about $25\%$ relative to the path it would have followed. Thus, on the balanced growth path significant changes in savings have only moderate effects on the level of output.

Another important question is how fast does $k$ converge to $k^\ast$. To address this, we take the first-order Taylor approximation of $\dot{k} = sf(k) - (n + g + \delta)k$ around $k^\ast$:

$$
\dot{k} \approx \left[\left. \frac{\partial \dot{k}}{\partial k} \right|_{k = k^\ast} \right](k - k^\ast).
$$

Of course, the rate of convergence is proportional to the distance of $k$ to $k^\ast$. Evaluating the derivative of $\dot{k}$ at $k=k^\ast$ yields $(n + g + \delta)[\alpha_K(k^\ast) - 1]$, which also involves the elasticity wrt capital. This is also the speed at which $y$ converges to $y^\ast$. The final path for $k$ is given by

$$
k(t) = k^\ast + \big(k(0) - k^\ast\big)e^{(n + g + \delta)[\alpha_K(k^\ast) - 1] t}.
$$

Usually $n + g + \delta$ is about $6\%$ per year and $\alpha_K(k^\ast)$ is about $1/3$. Hence, $k$ and $y$ move about $4\%$ of their remaining distance every year, which is very slow. Note that the Taylor approximation allows us to rely on this calculation only when $k$ is already in a small neighborhood around $k^\ast$.

Let's also consider what happens with consumption when the savings rate increases. Intuitively, if $s$ increases, households save more and consume less, so consumption should go down? Yet, a higher $s$ increases $Y$, so which may lead to altogether increased consumption. So it seems unclear. Consumption per unit of effective labor is given by $c(k) = f(k) - sf(k)$. At the balanced path, $c^\ast = f(k^\ast) - (n + g + \delta)k^\ast$. Therefore,

$$
\frac{\partial c^\ast}{\partial s} = \left[f'(k^\ast) - (n + g + \delta) \right]\frac{\partial k^\ast}{\partial s}.
$$

The change in consumption is positive if the MPK is greater than the break-even rate, $f'(k^\ast) > (n + g + \delta)$, otherwise consumption will decrease. So different values of $k^\ast$ can affect consumption differently. Yet, there is one particular value where consumption is maximal and that is when $f'(k^\ast) = (n + g + \delta)$. This is called the *golden rule* and here a small change in the savings rate does not affect consumption. At that particular point the production function and the break-even investment have equal slopes. Put another way, the golden-rule capital stock relates to the highest level of permanent consumption which can be sustained.

Finally, let's close by listing the shortcomings of the model. First, it assumes exogeneous technological progress, labour workforce, and savings rate. This is certainly convenient if we want to trace how growth changes given shocks to $s$, but if we want to understand how $s$ would change depending on some other factor, e.g. microeconomic foundations of households, we need a more powerful model. It also doesn't explain what the technological level $A(t)$ is? Is it education, property rights, quality of infrastructure, cultural attitudes?

Secondly, the model implies that differences in capital accumulation cannot account for large differences in incomes. Suppose the difference between the output per capita between two countries is $X$. Then, the differences in capital per capita has to be $X^{1/\alpha_K}$. To see this:

$$
X = \frac{y_B}{y_A} = \frac{k_B^{\alpha_K}}{k_A^{\alpha_K}} = \left(\frac{k_B}{k_A}\right)^{\alpha_K} \Rightarrow \frac{k_B}{k_A} = X^{1/\alpha_K}.
$$

In major industrialized countries output per worker is $X=10$ times larger than what it was 100 years ago, and 10 times larger than what it is in poor countries. Yet, the observed capital per capita differences are simply not in the order of $1000$ times, as would be required by $X^{1/\alpha_K}$. Is the Solow model missing something? Does capital have positive externalities? Should $K$ also encompass non-physical capital? These questions motivate more sophisticated models.