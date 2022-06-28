---
layout: post
title: An Overview of How The Economy Works
date: 2022-06-15 16:00:00 +0200
tags: [econ]
---

Macroeconomics is a difficult discipline. Like any other hypothesis, we want our model of the economy to be both expressive and simple. But in the case of macro, obtaining such a model is hard because the aggregate quantities that we observe in practice are determined by thousands and thousands of decisions made by complex economic agents. The economy itself is a complex system with sophisticated information processing capabilities and feedback loops. Questions like "Why did inflation increase this year?" certainly have exact precise answers, but they are probably so long that no one can comprehend them.

This post explores the simplest macroeconomic model, the IS-LM model, and lays the groundwork for future discussions around that topic. The IS-LM model is a purely conceptual model. It has no real predictive value and lacks any kind of dynamics. It is not concerned with technical issues like how fast equilibrium is reached or how much precisely does a given variable increase. Its main strength is its simplicity and the ability to capture fundamental relationships between macroeconomic aggregates. Most importantly, it provides precious intuition about how the economy works.

To begin, we distinguish between three economic entities - households, firms, and the government. Each citizen can be a member of one or more of these. The households consume, save, and invest. The firms employ labour and capital, produce goods and services, and invest. The government collects taxes and spends money (among many other things). These are the main players of the game.

In terms of economic aggregates, macro is concerned with three important variables: *output*, *unemployment*, and *inflation*. Output relates to how much is produced in a given year and measures how big the economy is. Unemployment relates to how easy it is to find a job, given that you want to work. In a capitalist society where you are paid only in exchange for the labour services that you provide, unemployment is an indicator of how well employees are matched with prospective employers. Finally, inflation relates to the general movements of the prices of goods and services. A representative price level is defined and tracked. Its up/down movements indicate that a fixed amount of money now buys you less/more goods than before.

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
    <img class='small_img' src="/goods_market.svg" alt="The goods market equilibrium" width="1000">
    <figcaption>Figure 1: The equilibrium in the goods market.</figcaption>
</figure>

To get a sense of how the equilibrium will change, one needs to understand that unexpected shocks to the exogenous variables will shift the demand curve. For example, if the public learns of a significant increase in the interest rate, then consumption and investment will decrease. As a result, for any income level, demand will be lower and the resulting equilibrium GDP will be lower than its current value. 

### The Financial Market
In the goods market, we took the interest rate as given, whereas in reality its value is determined in the money market. The money market is a very special market because what is traded in it is money today compared to money in the future. Ultimately, every economic agent has a preference over states of the world and these preferences include comparisons of present states and future states. Since money is the main medium of exchange and can be traded for real goods, the demand for real goods today compared to tomorrow depends on the demand for money today compared to tomorrow.

These relationships allows us to measure the temporal preference of people using answers to questions like "Would you deposit \\$1 today and receive \\$1.01 tomorrow, or spend the \\$1 today to receive a certain amount of instant satisfaction?". These decision are all around us and directly reflect the willingness to save, to invest, and to forgo pleasure today, compared to pleasure in the future. In fact, temporal preference can be linked to how shortsighted, in an economic sense, a person is, which can be used as possible explanations of boom-and-bust cycles.

In the money market, typical "services" sold are bank loans and deposits, because they represent an influx of money now, and a repayment of that money later, from the point of view of the borrower/lender. The price of these services offered is reflected by the interest rate for borrowing and lending. The interest rate is the single quantity establishing a price in the market of intertemporal funds. Bear in mind that many factors affect the interest rate that lenders and borrowers are willing to accept - this includes the expected inflation, the scarcity of money, the time preference of borrowers, and others.

Similarly to above, we can define a demand and supply for money. The demand for money reflects the demand for loans by households and businesses. In general, this demand depends negatively on the interest rate that banks give on deposits. This is because with higher deposit interest rates, people are more incentivized to hold their money in bank deposits, instead of currency. Likewise, with low interest rates, people are incentivized to hold more currency and the opportunity cost of doing so is smaller. The demand for money depends also on the nominal value of income, because if the general price level suddenly doubles, one will need more money on hand in order to meet the same number of previous transactions. In general, the demand for money is a decreasing function in the interest rate, and is increasing in the nominal income.

The supply of money requires us to make a distinction between currency (notes, coins, central bank reserves) and deposit accounts. The level of currency is directly supplied by the central bank through money creation, or printing of new bills. The level of bank deposits is supplied by commercial banks, but is heavily dependent on the interest rate set by the central bank (due to [fractional reserve banking](https://en.wikipedia.org/wiki/Fractional-reserve_banking) and liquidity requirement laws). The interest rate is determined through the supply and demand for money and in reality, the central bank sets the currency level so that a given interest rate is reached. Thus, we can think of the central bank as de facto setting the interest rate.

<figure>
    <img class='small_img' src="/money_market.svg" alt="The money market equilibrium" width="1000">
    <figcaption>Figure 2: The equilibrium in the money market.</figcaption>
</figure>

Figure 2 shows the money supply as a constant value determined by the central bank. The money demand is decreasing in the interest rates. The intersection of the two determines the equilibrium. This graph hides a lot of additional complexity. It is convenient to assume that the borrowing rate is equal to the lending rate which is equal to the interest rate set by the central bank. Additionally, the demand for money is assumed to contain all forms of money - currency, bank deposits, and reserves.

Controlling the money supply and hence the interest rate determines the *monetary policy* of the central bank. It is common during recessions for the central bank to perform monetary expansion, where the money supply is increased, the interest rate is lowered, and as a result the consumption and investment components of output are increased. This influx of money stimulates more spending, which can be beneficial during a recession. On the other hand, in situations where excessive spending causes prolonged inflation, the central bank can engage in contractionary monetary policy, where the effects on the economy will be exactly the opposite as described above.


<!-- In principle, the macroeconomic aggregates 

Like any other hypothesis, we want our model of the economy to be both expressive and simple (so that it can be understood by people and estimated from limited historical data). I don't think I'll exagerate by saying that macroeconomics is the field where achieving a good compromise between these requirements is the most difficult.


On the one hand, modelling an entire economy requires coming up with a theoretical framework, usually a set of logical and intuitive relationships between the entities, for how the economy behaves. These should be simple, robust, and generalizable - they should capture fundamental human behaviour. On the other hand, the model has to be computable and accurate (in terms of real-world prediction).  -->

