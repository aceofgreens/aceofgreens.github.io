---
title: A Tour de Force of the Economy
date: 2022-06-15 16:00:00 +0200
tags: econ
slug: a_tour_de_force_of_the_economy
---

Macroeconomics is a difficult discipline. Like any other hypothesis, we want our model of the economy to be both expressive and simple. But in the case of macro, obtaining such a model is hard because the aggregate quantities that we observe in practice are determined by thousands and thousands of decisions made by complex economic agents. The economy itself is a complex system with sophisticated information processing capabilities and feedback loops. Questions like "Why did inflation increase this year?" certainly have exact precise answers, but they are probably so long that no one can comprehend them.

This post uses the simplest macroeconomic model, the IS-LM model, to explore how a modern closed economy works, and lays the groundwork for future discussions around that topic. The IS-LM model is a purely conceptual model. It has no real predictive value and lacks any kind of dynamics. It is not concerned with technical issues like how fast equilibrium is reached or how much precisely does a given variable increase. Its main strength is its simplicity and the ability to capture fundamental relationships between macroeconomic aggregates. Most importantly, it provides precious intuition about how the economy works. All notation for this post has been borrowed from Olivier Blanchard's *Macroeconomics: A European Perspective* book.

To begin, we distinguish between three economic entities - households, firms, and the government. Each citizen can be a member of one or more of these. The households consume, save, and invest. The firms employ labour and capital, produce goods and services, and invest. The government collects taxes and spends money (among many other things). These are the main players of the game.

In terms of economic aggregates, macro is concerned with three important variables: *output*, *unemployment*, and *inflation*. Output relates to how much is produced in a given year and measures how big the economy is. Unemployment relates to how easy it is to find a job, given that you want to work. In a capitalist society where you are paid only in exchange for the labour services that you provide, unemployment is an indicator of how well employees are matched with prospective employers. Finally, inflation relates to the general movements of the prices of goods and services. A [representative price level](https://en.wikipedia.org/wiki/Consumer_price_index) is defined and tracked. Its up/down movements indicate that a fixed amount of money now buys you less/more goods than before.

When determining the relationships between output, unemployment, and inflation, it is useful to distinguish between three time frames:

- the *short-run*, when information from exogenous shocks has not propagated all economic agents yet, resulting in some variables remaining fixed;
- the *medium-run*, when sufficient time has passed that those previous constant variables can be adjusted, resulting in different equilibrium configurations;
- the *long-run*, a time horizon so long that all transitory economic effects from the medium run are dwarfed by time. Here only factors which determine long-term growth matter.

The distinction between short, medium, and long-run is naturally fuzzy. If we are at time $t$, we may consider $t+1$ as the short run and $t+30$ as the long-run. But if we are at $t+29$, then $t+30$ from our new perspective becomes the short-run. This perspective change is similar to a Markov chain converging to an equilibrium distribution - it's not that it actually converges step-by-step, it's that the distribution many steps from now converges.

The concept of equilibrium permeates economics. A market for a given product is said to be in equilibrium if the supply and demand for that product are equal. The **supply** is a function representing the price at which a seller is willing to supply an additional unit of the good. This can also be interpreted as how much quantity is supplied at any given price. Similarly, **demand** is a function representing the maximum price a customer is willing to pay for an additional unit of the good. This is, likewise, interpeted as the total quantity demanded at any given price.

### The Goods Market
Let's look at the goods market first. We can represent the total demand for goods and services, $Z$, as the combined demand from households, businesses, and the government:

$$ Z = C + I + G. $$

$C$ represents the consumption on a regular basis from households. If $Y$ is the monetary value of income and $T$ is the value of taxes paid (net, because each person is both a contributor and a receiver of government taxes), then in a simplified setting, consumption can be thought of as having an autonomous component $c_0$ and an increasing component in disposable income $C = c_0 + c_1 (Y - T)$. As the disposable income $Y_D = Y - T$ increases, households consumer more. As it decreases, households consume less, up to a minimum amount $c_0$.

More realistically, consumption is believed to depend on the expected total wealth of the household. In order to decide how much to spend on consumption today, a household forms an expectation over its future housing (from real estate), financial (from financial markets) and human (from labour markets) wealth. Then the household decides to consume today a fraction of its wealth such that consumption is smoothed over future periods (this is called the [permanent income hypothesis](https://en.wikipedia.org/wiki/Permanent_income_hypothesis)).

The factors which affect consumption are those that affect the expected wealth. A future increase in the interest rate is inversely proportional to the net present value of that wealth. If the perceived interest rate increase is deemed to be non-transient the consumer may reduce his consumption significantly more than if it's perceived as a one-time shock.

The investment, $I$, represents the value that households and businesses want to spend today, in order to increase profit or value in the future. The demand for investment depends, similarly to consumption, on the expected net present value of all cash flows that the investment will yield. Any factor that affects this NPV calculation affects investment. This includes changes in perceived real interest rates (taking inflation into account), changes in the cash flow estimates, changes in capital depreciation rates, and changes in the long-term risk attitude of businesses and households.

There is a uncanny similarity between the factors that affect stock prices and those that affect investment. Both require coming up with a NPV estimate of the cashflows from the asset under consideration. In fact, [Tobin's q](https://en.wikipedia.org/wiki/Tobin%27s_q) is the value of a unit of capital in place relative to its current purchase price. The underlying idea is that the information in the NPV calculation is already included in the market price of the capital in place, which can be obtained from the market value of the firm using some accounting adjustments. The higher Tobin's q is, the more profits a firm expects per unit of capital. Based on this, this measure is a common predictor often used in dynamic investment models.

The third component of the demand is that coming from the government, $G$. The factors which influence how much governments want to spend are numerous and different in nature. Forms of government, relationships with neighboring states, upcoming elections, and economic systems are just some of the things which can shift the demand. However, in most models government demand for goods and services is treated as an exogenous variable, i.e. it is taken as given, and not something that the model itself outputs.

Now, the supply of new goods and services, or the output, is roughly speaking, the gross domestic product (GDP) for that year. With a further assumption that businesses hold no inventories, this means that in equilibrium, when supply equals demand, the demand for goods and services $Z$ is equal to the total output. Moreover, since every unit produced is met by a unit demanded, the value of all goods produced is equal to the total income $Y$. So the equilibrium condition becomes

$$Y = C + I + G,$$

where $C$, $I$, and possibly $G$ all depend on $Y$. Figure 1 shows the equilibrium demand and supply with assumed linear functional forms. The blue line shows that with no inventories production is equal to income. The orange line shows that the demand is increasing in the income. The equilibrium, given everything else constant, occurs where the supply and demand are equal - [the Keynesian cross](https://en.wikipedia.org/wiki/Keynesian_cross).

<figure>
    <img class='small_img' src="/images/goods_market.svg" alt="The goods market equilibrium" width="1000">
    <figcaption>Figure 1: The equilibrium in the goods market.</figcaption>
</figure>

To get a sense of how the equilibrium will change, one needs to understand that unexpected shocks to the exogenous variables will shift the demand curve. For example, if the public learns of a significant increase in the interest rate, then consumption and investment will decrease. As a result, for any income level, demand will be lower and the resulting equilibrium GDP will be lower than its current value.

The $Y = C + I + G$ is called the "investment-saving" (IS) relation, because it can be similarly derived with investment being equal to savings in equilibrium. We let $S = Y_D - C$ be the private saving by consumers and rearrange $Y = C + I + G$ to obtain 

$$I = S + (T - G),$$

which suggests that in equilibrium, investment is equal to private saving $S$ plus public saving $T - G$. So in equilibrium any disposable income that is not consumed by households is invested, along with any collected taxes above government spending.

### The Financial Markets
Financial markets contain risk-free assets like money, and risky assets like bonds and loans. Money does not pay interest and can be used in transactions, while bonds do pay interest. Our central objective is to understand the relationships between risk-free and risky assets and how these relationships determine the interest rate.

In the goods market, we took the interest rate as given, whereas in reality its value is determined in the money market. The money market is a very special market because what is traded in it is money today compared to money in the future. Ultimately, every economic agent has a preference over states of the world and these preferences include comparisons of present states and future states. Since money is the main medium of exchange and can be traded for real goods, the demand for real goods today compared to tomorrow depends on the demand for money today compared to tomorrow.

These relationships allows us to measure the temporal preference of people using answers to questions like "Would you deposit \\$1 today and receive \\$1.01 tomorrow, or spend the \\$1 today to receive a certain amount of instant satisfaction?". These decision are all around us and directly reflect the willingness to save, to invest, and to forgo pleasure today, compared to pleasure in the future. In fact, temporal preference can be linked to how shortsighted, in an economic sense, a person is, which can be used as possible explanations of boom-and-bust cycles.

In the money market, typical "services" sold are bank loans, bonds, and deposits, because they represent an influx of money now, and a repayment of that money later, from the point of view of the borrower/lender. The price of these services offered is reflected by the interest rate for borrowing and lending. The interest rate is the single quantity establishing a price in the market of intertemporal funds. Bear in mind that many factors affect the interest rate that lenders and borrowers are willing to accept - this includes the expected inflation, the scarcity of money, the time preference of borrowers, and others.

Similarly to above, we can define a demand and supply for money. The demand for money reflects the demand for loans by households and businesses. In general, this demand depends negatively on the interest rate that banks give on deposits. This is because with higher deposit interest rates, people are more incentivized to hold their money in bank deposits, instead of currency. Likewise, with low interest rates, people are incentivized to hold more currency and the opportunity cost of doing so is smaller. The demand for money depends also on the nominal value of income, because if the general price level suddenly doubles, one will need more money on hand in order to meet the same number of previous transactions. In general, the demand for money $M^d$ is a decreasing function in the interest rate $i$, and is increasing in the nominal income $PY$

$$
\frac{M^d}{P} = Y L(i).
$$

The supply of money $M^s$ requires us to make a distinction between currency (notes, coins, central bank reserves) and deposit accounts. The level of currency is directly supplied by the central bank through money creation, or printing of new bills. The level of bank deposits is supplied by commercial banks, but is heavily dependent on the interest rate set by the central bank (due to [fractional reserve banking](https://en.wikipedia.org/wiki/Fractional-reserve_banking) and liquidity requirement laws). The interest rate is determined through the supply and demand for money and in reality, the central bank sets the currency level so that a given interest rate is reached. Thus, we can think of the central bank as de facto setting the interest rate.

<figure>
    <img class='small_img' src="/images/money_market.svg" alt="The money market equilibrium" width="1000">
    <figcaption>Figure 2: The equilibrium in the money market.</figcaption>
</figure>

Figure 2 shows the money supply as a constant value determined by the central bank. The money demand is decreasing in the interest rates. The intersection of the two determines the equilibrium. This graph hides a lot of additional complexity. It is convenient to assume that the borrowing rate is equal to the lending rate which is equal to the interest rate set by the central bank. Additionally, the demand for money is assumed to contain all forms of money - currency, bank deposits, and reserves. These assumptions do not change the results qualitatively.

Note that the equilibrium interest is determined by the central bank, through the money supplied by it. The combinations of values for which the money market is in equilibrium constitutes the "Liquidity preference - Money" (LM) curve. It has the standard form $M/P = Y L(i)$, however here $M$ is fixed, as decided by the central bank.

Controlling the money supply and hence the interest rate determines the *monetary policy* of the central bank. It is common during recessions for the central bank to perform monetary expansion, where the money supply is increased, the interest rate is lowered, and as a result the consumption and investment components of output are increased. This influx of money stimulates more spending, which can be beneficial during a recession. On the other hand, in situations where excessive spending causes prolonged inflation, the central bank can engage in contractionary monetary policy, where the effects on the economy will be exactly the opposite as described above.

However, the central bank cannot exert monetary policy without limits. In particular, the nominal interest rates cannot become 0, because that would make people indifferent from holding money or risky interest-paying assets. In effect, the money demand becomes flat at an interest rate of 0. If the central bank increases the money supply such that nominal interest rates are 0, any further increase in the money supply will have to effect. This is called a [liquidity trap](https://en.wikipedia.org/wiki/Liquidity_trap) and was a big problem for governments wanting to reduce the interest rate even further during the crisis between 2007 and 2009.

### The Labour Market
The labour market consists of workers willing to work in exchange for monetary compensation. The workers represent the supply of labour and the employers - the demand for labour. A central quantity of interest that determines how easy it is for a worker to find a job is the *unemployment rate* - it is the proportion of all people in the labour force who want to work, but are currently unemployed. The unemployment rate represents (roughly) the quantity of labour supplied at any given wage.

Before stating equilibrium conditions, we first explore how are wages determined. In general, two regularities can be observed:

- The wages paid to workers typically exceed the worker's *reservation wage*, which is the wage that makes them indifferent to being employed or not. In that sense, continuing to stay employed is a purposeful "action" for the worker and the [efficiency wage](https://en.wikipedia.org/wiki/Efficiency_wage) is a factor in the worker's decision.
- Wages typically depend on current market conditions like the unemployment rate, and the price level. Most wages are therefore correlated to the general availability of workers and the expectations for future key economic variables.

Ultimately, wages are determined by the bargaining power of workers and employers. A worker has more bargaining power if it is easy for him to find a different job of sufficient quality, and if it is difficult and costly for the firm to find different workers.

We can describe how the wages depend using the equation

$$
W = P^e F(u, z),
$$

where $W$ is the nominal wage, $P^e$ is the expected price level for the future, and $F(u, z)$ is a function decreasing in the unemployment rate $u$ and increasing in the catch-all variable $z$, which can represent any other factors like unemployment insurance, or employment protection. This shows that wages are higher if:

- unemployment is low, as there is less workers available
- expected prices are higher, as wage contracts are typically set in advance, and in nominal terms. If workers are expecting higher prices, and firms are expecting to sell their products at a higher price, it is logical that wages will also increase proportionally.

In terms of production, firms use both labour and capital in order to produce goods. However, in the short run, it may be easier for the firm to change the labour configuration rather than the capital configuration. If this is the case, we can model the ouput simply as 

$$ Y = AN, $$

where $A$ is the labour productivity rate and $N$ is the number of workers per unit of time. Even simpler, we can renormalize the units of output so that one worker produces one unit of ouput, leaving just $Y = N$. What is the cost of producing one more unit of ouput? Well, it's the cost of hiring one more worker - their wage $W$. Now, microeconomics tells us that in perfect competition the price set by firms is equal to their marginal cost. Here, however, since not all markets are perfectly competitive, we let the price be proportional to a *markup* factor $\mu$, indicating how far we are from perfect competition,

$$ P = (1 + \mu)W
$$

This equation suggests that the price set by firms is proportional to the wages paid to workers, and the markup amount, showing how much the firm can charge above perfect equilibrium prices. In reality, the markup amount depends on factors like antitrust regulation, or barriers of entry.

Figure 3 shows the equilibrium in the labour market, resulting from the wage-setting relation from the bargaining power of workers and the price-setting relation from the labour productivity. Importantly, increases in the markup reduce the equilibrium real wages and increase the unemployment rate. An increase in the unemployment benefits increases the wage-setting relation through $z$, and as a result, equilibrium unemployment increases.
<figure>
    <img class='small_img' src="/images/labour_market.svg" alt="The labour market equilibrium" width="1000">
    <figcaption>Figure 3: The equilibrium in the labour market, for fixed markup, and expected price levels.</figcaption>
</figure>

We see that, ceteris paribus, the equilibrium in the labour market determines the unemployment rate and the general wage levels. Importantly, in the special case where current price levels $P$ are equal to the the expected price levels $P^e$, the resulting unemployment rate is called the **natural rate of unemployment**, or the **structural rate of unemployment**. The requirement that $P = P^e$ means that the current prices have stabilized towards the expectated ones and the economy has reached a "stationary" state in terms of expectations. In other words, the effects of any shocks have passed and the prices have adjusted (or equivalently, expectations have adjusted to current prices).


### Additional Relationships

The wage-setting and price-setting relations can be used to derive a relationship between actual and future expected inflation, this being the famous [Phillips curve](https://en.wikipedia.org/wiki/Phillips_curve). Since $W = P^e F(u, z)$ and $P = (1 + \mu)W$, we can substitute one in the other to get

$$
P = P^e (1 + \mu) F(u, z).
$$

This is already pretty close to the desired result because it relates current and future expected prices. What is typically done next is to assume a linear relationship for $F(u, z)$, for example $F(u, z) = 1 - \alpha u + z$, and modify the above equation to yield the following approximation for the inflation $\pi$

$$ \pi = \pi^e + (\mu + z) - \alpha u $$

or even better

$$ \pi_t = \pi_t^e + (\mu + z) - \alpha u_t .$$

This equation is called the Phillips curve and suggests that the actual inflation in period $t$ depends on the expected inflation for period $t$. This happens because a higher expected price level $P^e$ leads to higher current prices $P$, which compared a given value of past prices, is inflation. Similarly, an increase in the markup or a decrease in the unemployment rate also lead to higher inflation.

The Phillips curve represents a fairly complicated process governing the inflation rate, mainly due to the different possibilities for the formation of the expectation $\pi_t^e$. Before 1970, it was believed that the expectation was constant $\pi_t^e = \bar{\pi}$, but after that models were adapted to handle autoregressive expectations like $\pi_t^e = \theta \bar{\pi} + (1 - \theta) \pi_{t-1}$. The accuracy of the Phillips curve now depends on the accuracy of the expectation model for $\pi_t^e$ and care should be taken when choosing its functional form in order to keep the process stationary (unless one wants to model rare scenarios like hyperinflation).

In light of the Phillips curve, the natural rate of unemployment has a new meaning. Since it is equal to the unemployment at equilibrium when the expected price level is equal to the actual one, the above relations suggest that this is equivalent to the unemployment at equilibrium when the expected inflation equals the actual one. That is, if $\pi_t = \pi_t^e$, then

$$
0 = (\mu + z) - \alpha u_n \Rightarrow u_n = \frac{\mu + z}{\alpha}.
$$

After that, it is easy to see that

$$
\pi_t - \pi_t^e = -\alpha (u_t - u_n).
$$

This is, again, a very important relationship. It shows that if the actual unemployment $u_t$ is greater than the natural one $u_n$, then the actual inflation $\pi_t$ will be smaller than the expected one. Likewise, if the actual unemployment is less than the natural one, the actual inflation will be greater than the expected one. 

A common autoregreesive model for $\pi_t^e$ is just the previous value $\pi_{t - 1}$. This gives a model relating the changes in inflation with whether the unemployment rate is above or below its natural level:

$$
\pi_t - \pi_{t - 1} = -\alpha (u_t - u_n).
$$

If expectations are autoregressive, as they are here, then the natural rate of unemployment is the rate that keeps the inflation constant.

We can also relate the unemployment rates to output, a useful relation called [Okun's law](https://en.wikipedia.org/wiki/Okun%27s_law). The unemployment rate is equal to $u = 1 - \frac{N}{L}$, the fraction of all unemployed people $L - N$ in the labour force $L$. Rearranging the terms gives $N = L(1 - u)$ which can now be plugged into the assumed labour productivity relation discussed previously $Y = N$, giving $Y = L(1 - u)$. The natural rate of unemployment $u_n$ is associated with a natural rate of output $Y_n$, also called **potential output**. Consequently, we can measure deviations from potential output, also called the output gap, as

$$
Y - Y_n = L((1 - u) - (1 - u_n)) = -L(u - u_n).
$$

This also yields a relationship between inflation and the output gap

$$
\pi - \pi^e = \frac{\alpha}{L}(Y - Y_n).
$$

The results gained from the previous equations can be summarized as follows:

- When the unemployment rate is smaller than the natural rate of unemployment, then the actual output is greater than the potential output and inflation is higher than expected.
- When the unemployment rate is larger than the natural rate of unemployment, then the actual output is smaller than the potential output and inflation is smaller than expected (may even be negative).


### General Equilibrium
Given all of the relationships derived for the goods, money, and labour markets, one can now describe how general equilibrium is reached.

In the **short run** it is generally believed that prices, wages, and capital are all sticky and held constant. This implies that what output really depends on is the demand from the goods market and the money market. Thus, we are interested in finding the combination of values for which both the goods and the money market are in equilibrium. This results in the [IS-LM model](https://en.wikipedia.org/wiki/IS%E2%80%93LM_model), where the IS and LM relations give the equilibrium conditions for the goods and the money markets, respectively.

<figure>
    <img class='small_img' src="/images/is_lm.svg" alt="The IS-LM equilibrium" width="1000">
    <figcaption>Figure 4: The joint equilibrium in the goods and money market. The IS relation shows all points where the goods market is in equilibrium, and the LM relation shows all points where the money market is in equilibrium.</figcaption>
</figure>

Figure 4 shows the IS-LM equilibrium as the point where the IS and LM relations intersect, with all other variables that affect them being fixed. 

<!-- The IS-LM graph shows the equilibrium interest rate and output, but in reality one can trace how this equilibrium depends on other variables, like the price level. Plotting the IS-LM equilibrium with prices on the $y$-axis, instead of interest rates, yields the famous [aggregate demand - aggregate supply (AD-AS)](https://en.wikipedia.org/wiki/AD%E2%80%93AS_model) curve, which gives a more "microeconomic" feel, since it shows prices and quantities on the $y$ and $x$ axes. We don't show it here, because it  -->

Thus in the short run, output and interest rates are determined by changes in demand, and fiscal & monetary policy. The resulting short-run equilibrium output, where the IS and LM relations intersect, may be above or below the potential output $Y_n$, which would trigger inflation or deflation, respectively.

For example, if the short-run IS-LM equilibrium output is above $Y_n$, and inflation expectations are formed as $\pi_t^e = \pi_{t-1}$, then the current inflation $\pi_t$ will be larger than the previous period's, proportionally to how different is $Y_t$ to $Y_n$. Holding everything else constant, the resulting inflationary process will continue and the price level will be increasing at an ever-accelerating rate. At some point, it is likely that the central bank will intervene and increase the interest rate, causing consumption and investment to be reduced, leading to a lower equilibrium output $Y$, possibly below the potential output $Y_n$. This would result in reduced inflation or even deflation.

The **medium-run** equilibrium is defined as that point where $Y = Y_n$. The corresponding interest rate is called the *natural*, *neutral*, or *Wicksellian* rate of interest. At this equilibrium point any expansionary fiscal or monetary policy causes increased inflation beyond what is expected. Likewise, any contractionary policy causes inflation below what is expected. One can say that roughly, if the populace expects a constant inflation rate of 2%, and the actual inflation is 2%, then the economy is at or near its medium-run equilibrium. Finally, any factor that affects the natural rate of unemployment $u_n$, like the markup, or the bargaining power of workers, causes a shift in $u_n$, and $Y_n$, changing the medium-run equilibrium altogether.

One important dangerous scenario is the case of a *deflationary trap*. Suppose that the short-run equilibrium output is below its potential level $Y_n$ and that the nominal interest rate set by the central bank is already at 0%. If inflation expectations are adaptive and are formed as $\pi_t^e = \pi_{t - 1}$, then since $Y$ is below $Y_n$, inflation rates are decreasing. Once they become negative, prices start falling. What the central bank should do is decrease the interest rate, but the zero lower bound is preventing it from doing that. Since inflation is negative, real interest rates are positive, causing people to hoard, instead of spend, thereby reducing output even further. In the next period, the difference between $Y$ and $Y_n$ is even larger, causing even more deflation. This soon becomes a vicious circle... In such cases, one approach, according to Keynesians is to increase the fiscal spending $G$, so as to bring the demand back to its previous levels.

Let's now switch our attention to the **long-run**, where we are concerned with how economies grow over time.

A central measure of growth is the output per worker $Y/N$. In the medium-run it is assumed that firms only change the number of workers employed, that is why we used a simple production function like $Y = N$. In that case the output per capita is a constant $Y/N = N/N = 1$ and the economy doesn't grow. Here, however, we acknowledge that over extended periods of time both labour $N$ and capital $K$ are control variables that firms optimize over. Hence, in the long-run output depends both on labour and capital. We can represent this using a production function like $Y = F(K, N)$.

It is convenient to assume the following properties for the production function:

- It has constant returns to scale. If we multiply all labour and capital inputs by $x$, then the output is multiplied by $x$, $xY = F(xK, xN)$
- It has decreasing returns to capital, i.e. $\frac{\partial^2 Y}{\partial K^2} < 0$,
- It has decreasing returns to labour, i.e. $\frac{\partial^2 Y}{\partial N^2} < 0$.

One candidate for such a function is the [Cobb-Douglas](https://en.wikipedia.org/wiki/Cobb%E2%80%93Douglas_production_function) one, with proper parameters. Given these assumptions, the output per capita is given by 

$$Y/N = F(K, N)/N = F(K/N, 1) = f(K/N).$$

This shows that output per person depends on the level of capital per person and the *technological progress*, roughly accounting for the functional form of $F$ or its simplification $f$.

Let's first look at how the capital per worker affects output per worker. Ultimately, the capital stock depreciates with time, and is increased each year by the investment for that year

$$K_{t+1} = (1 - \delta)K_t + I_t,$$

where $\delta$ is the depreciation rate. For simplicity, assume that there is no public saving, so that investment equals only private spending, the employment $N$ is constant, and that public saving is a fraction of the income $I_t = S_t = sY_t$. Then the capital stock per capita becomes

$$\frac{K_{t + 1}}{N} = (1 - \delta)\frac{K_t}{N} + s\frac{Y_t}{N}.$$

The difference between two consecutive capital per capita values is

$$
\frac{K_{t+1}}{N} - \frac{K_t}{N} = s\frac{Y_t}{N} - \delta \frac{K_t}{N} = s f \Big (\frac{K_t}{N} \Big) - \delta \Big(\frac{K_t}{N} \Big).
$$

This suggests that if savings per worker is greater than the depreciation per worker, the capital stock increases. Otherwise, capital decreases. Thus, if we let the economy evolve, the capital will increase up to the point $K^*$ where savings per capita equals depreciation per capita, where it will converge.

$$
s f \Big (\frac{K^*}{N} \Big) = \delta \Big(\frac{K^*}{N} \Big)
$$

This is the long-run equilibrium, also called the *steady state*, because of capital converging to it. The steady state value of output is given by 

$$\frac{Y^*}{N} = f \Big ( \frac{K^*}{N} \Big ).$$

<figure>
    <img class='small_img' src="/images/growth.svg" alt="The long-run equilibrium" width="1000">
    <figcaption>Figure 5: The long-run, steady state equilibrium.</figcaption>
</figure>

From the steady state equilibrium, we can observe the following:

- The saving rate $s$ has no effect on the long-run growth rate of output per worker,
- The long-run growth rate of output per worker converges to 0,
- The saving rate $s$ determines the level of output per worker in the steady state.
- An increase in the savings rate will increase the outper per worker growth rate initially, but this effect is transient and will disappear.

Note that since the saving affects the steady state output, asking how much should the savings rate be is a valid question. If the savings rate is 0, you get no capital and no output. On the other hand, if the savings rate is 1, you get an extraordinary amount of capital and output, but no consumption. From the point of view of consumers, what matters to them is not the steady-state level of output, but the steady-state level of consumption. This observation motivates many governments to pursue policies targeting the *golden-rule level of capital* - the capital level which maximizes the steady state level of consumption. It is believed that most countries, including advanced ones, have capital levels far below the golden rule. As a result increasing the saving rate will hurt consumption in the short-run but will ultimately increase consumption in the long-run.

So this is how capital affects the long-run equilibrium output. But what about technological progress? To model technological progress, it's common to assume the following production function

$$
Y = F(K, N, A) = F(K, AN),
$$

where the new variable $A$ represents the state of technology in the economy. It is assumed that it interacts only with the number of employed workers. The product $AN$ then represents the *effective labour* in the economy. Similarly to before, we can measure the output per effective worker as

$$
\frac{Y}{AN} = F \Big (\frac{K}{AN}, 1 \Big ) = f \Big (\frac{K}{AN} \Big ) .
$$

Since the technology level $A$ increases with time, the effective labour $AN$ also increases. If $A$ grows with rate $g_A$ and the employment $N$ grows with $G_N$, then $AN$ grows with rate approximately $g_A + g_N$. Thus, to sustain a constant level of capital per effective worker we need the investment to grow as $\delta + g_A + g_N$, where $\delta$ is the depreciation rate. The steady state equilibrium condition in this case becomes

$$ s f \Big ( \big (\frac{K}{AN} \big )^* \Big) = (\delta + g_A + g_N) \big (\frac{K}{AN} \big)^*. $$

We note about the steady state equilibrium that:

- Effective labour, and as a result the output, grow at the rate $g_A$ + $g_N$,
- Capital per effective worker and output per effective worker are constant,
- Capital per worker and output per worker (not effective) grow at the rate $g_A$,
- The growth rate of output is independent of the saving rate,
- The steady state level of output depends on the saving rate. 

Ultimately, the long-term level of output depends on the capital stock and the state of technology in the economy. Convergence to the long-run steady-state implies that to increase the quality of life, measured as output per capita, technological progress should be prioritized. This includes more well-established property rights, spending on firms' R&D projects, and better mechanisms for the appropriability of the result from these projects.