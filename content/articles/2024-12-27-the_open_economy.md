---
Title: The Open Economy
Date: 2024-12-27 07:00:00 +0200
Tags: econ
slug: open_economy
---

We've previously explored the basic workings of closed economies. Now it's time to consider different national economies in relation to each other. This will lead us to topics like exchange rates, imports and exports, and currency wars. It is an important topic that provides a convenient frame of reference in which to ground current world developments and historical events. Finally, it holds curious intellectual concepts like the impossible trinity.

The openness of an economy has multiple dimensions: *openness in goods markets* refers to the ability of consumers and firms to choose between domestic and foreign goods, unencumbered by tariffs and quotas; *openness in financial markets* allows investors to choose between domestic and foreign financial assets; *openness in factor markets* allows firms to choose where to set up production and workers to choose where to work.

**Openness in goods markets**. The demand for domestic and foreign goods is determined predominantly by the real exchange rate, which represents the price of domestic goods in terms of real foreign goods. The real exchange rate is unobservable. Instead we can measure the nominal exchange rate, which is just the price of the domestic currency in terms of the foreign currency. If the exchange rate between USD and GBP is 0.79, then $E = \frac{\text{ USD}}{\text{ GBP}} = 0.79$ and $1 \text{ USD}$ buys $0.79 \text{ GBP}$. To calculate the real exchange rate, denoted $\epsilon$, one multiplies $E$ with the price index $P$ to get the price of US goods in pounds, then divides by the price of UK goods $P^\ast$:

$$
\epsilon = \frac{E P}{P^\ast}.
$$

On the macro level, absolute values of the real exchange rate are not interpretable, due to the price index $P$, but rates of change are meaningful. A real appreciation, i.e. an increase in $\epsilon$, can be caused either if $E$ increases, or if $P/P^\ast$ increases. It's also possible that the nominal exchange rate $E$ increases, while the real exchange rate $\epsilon$ decreases. An increase in $\epsilon$ makes the domestic currency (from the numerator) stronger relative to the foreign one.

**Openness in financial markets**. With free capital flows between countries, people face the decision of whether to hold domestic assets or foreign assets. Usually they have little point in holding foreign currency because it cannot be used to buy domestic goods. If we simplify and ignore the exceptions, of which there are plenty, it only matters how people choose to hold domestic versus foreign interest paying assets.

Now, an important relation holds between exchange rates and returns of financial assets. A US citizen can invest 1 USD in a 1 year US bond, and will obtain $(1 + i)$ USD at the end. Alternatively, he can convert to pounds, obtain $E$ GBP, buy a 1 year UK bond, and obtain $E(1 + i^\ast)$ GBP next year. He can then convert back to USD to obtain $E(1 + i^\ast)/E^e_{t+1}$ where $E^e_{t+1}$ is the expected nominal exchange rate for next year. Disregarding transaction costs and risk, open financial markets means that people will use arbitrage to equalize the profits from these two opportunities:

$$
(1 + i_t) = (1 + i^\ast_t) \frac{E_t}{E^e_{t+1}} = \frac{1 + i_t^\ast}{[1 + (E^e_{t+1} - E_t)/E_t]} \Rightarrow i_t \approx i_t^\ast - \frac{E^e_{t+1} - E_t}{E_t}
$$

This is called the *uncovered interest rate parity* condition. Uncovered means that the investor does not hedge, i.e. does not “cover” the foreign exchange risk using forward or futures contracts. Instead, the investor simply converts currency at the spot rate, invests in the foreign asset at the foreign interest rate, and then converts back at the (unknown) future spot rate, exposing themselves to potential currency fluctuations. The last equation shows that the domestic interest rate is approximately equal to the foreign one, adjusted according to the expected domestic appreciation. Here $i_t^\ast$ and $E^e_{t+1}$ are exogeneous and if we assume the central bank sets the interest rate, then $i_t$ is also exogeneous. $E_t$ is what adjusts so as to remove arbitrage.

**Demand for domestic goods**. In an open economy the demand for domestic goods now includes, apart from the usual components, imports $IM$ and exports $X$. The imports are converted into domestic goods by dividing by the real exchange rate:

$$
Z = C(Y - T) + I(Y, r) + G - IM(Y, \epsilon)/\epsilon + X(Y^\ast, \epsilon).
$$

- Imports depend positively on domestic income $Y$ and the real exchange rate $\epsilon$, $IM = IM(+Y, +\epsilon)$. As income increases, demand for all goods, including foreign ones, increases. As $\epsilon$ increases, the domestic currency becomes stronger and foreign goods become relatively cheaper, increasing the demand for them.
- Exports, due to similar reasons, depend positively on foreign income $Y^\ast$ and negatively on the real exchange rate $\epsilon$, $X = X(+Y^\ast, -\epsilon)$. As foreigners have more income, some of it is spent over domestic goods. As $\epsilon$ increases, domestic goods become more expensive, decreasing foreign demand for them.

Now, as in the standard Keynesian cross, the goods market is in equilibrium when $Y = Z$. The foreign income $Y^\ast$ and the real exchange rate $\epsilon$ affect the equilibrium domestic output, denoted $\hat{Y}$. Note that this value itself affects the net trade deficit $NX = X - IM/\epsilon$. In general, if $Y$ increases, $NX$ decreases. This is problematic for policymakers, because if you increase demand $Z$ by increasing, say, government spending $G$, then output increases $Y$, but this worsens the trade balance $NX$, which is generally bad, because the domestic country becomes indebted to the other countries and has to pay increasing amounts of interest.

Hence, an increase in domestic demand increases output but deteriorates the trade balance $NX$. An increase in foreign demand improves domestic output and on the contrary improves trade balance by boosting exports. Note that under a *policy coordination* scheme it may be the case that multiple countries rely on fiscal policy to boost their own domestic demand without worsening their trade balances vis-a-vis each other. Such a regime of correlated fiscal policies is not easy to achieve. One method to do so is by undertaking military actions, even war. As an example, in the early 19th century, British demand for Chinese goods like tea, silk, and porcelain was high, while Chinese demand for British products was low. This led to a significant trade deficit for Britain, as silver flowed from Britain to China to pay for Chinese goods. To balance trade, the British East India Company began exporting opium from India to China. Opium use became widespread in China and caused social and economic issues, leading the Chinese government to ban the opium trade. The British then began a series of [military actions](https://en.wikipedia.org/wiki/Opium_Wars) to protect British commercial interests and ensure the continuation of the opium trade.

How does currency depreciation affect the equilibrium? If $\epsilon$ decreases, $IM$ decreases, but $1/\epsilon$ increases, so the effect is ambiguous. A technical condition on the demand elasticities called [Marshall-Lerner](https://en.wikipedia.org/wiki/Marshall%E2%80%93Lerner_condition) allows us to specify when exactly will $NX$ increase. In general, this assumption holds empirically and thus we can say that a real depreciation of $\epsilon$ increases $NX$. For the end consumer, a real depreciation is painful as it makes imported goods relatively more expensive.

**Exchange rates and interest rates**. Assuming floating currencies, the nominal exchange rate $E$ is determined in the free markets. People bid and ask different amounts for each unit of foreign currency, leading to an often volatile and fast changing exchange rate. The uncovered interest parity can be reformulated as

$$
E_t = \frac{1 + i_t}{1 + i^\ast_t} E^e_{t+1},
$$

and from here it becomes evident that if $i_t$, $i^\ast_t$, and $E^e_{t+1}$ are fixed, then a change in any of them will visibly affect $E_t$. For example, an increase in $E^e_{t+1}$ will cause investors to believe that the domestic currency, suppose dollars, will become stronger. As a result, they will look to acquire more of it, bidding its price up and therefore the exchange rate. Similarly, and very important, an increase in the domestic interest rate leads to a proportional increase in the exchange rate.

To solve the IS-LM model in an open economy, again we intersect the IS and LM curves.

$$
\begin{align}
\text{IS:  }  &Y = C(Y - T) + I(Y, i) + G + NX(Y, Y^\ast, \frac{1 + i}{1 + i^\ast}\bar{E}^e)\\
\text{LM:  }  &i = \bar{i},
\end{align}
$$

where for simplicity we've assumed that the central sets the interest rate, inflation is 0, the expected future exchange rate is fixed, and $P/P^\ast = 1$. By setting the interest rate, an equilibrium exchange rate is determined. This then affects indirectly equilibrium output and the trade balance.

**Impossible trinity**. The model presented so far is called [Mundell-Fleming](https://en.wikipedia.org/wiki/Mundell%E2%80%93Fleming_model). And from it comes an important result, called the policy trilemma. In short, it states that a country cannot have at the same time a *fixed foreign exchange rate*, *free capital movement*, and *independent monetary policy*. To see why, conside the following:

1. Fixed exchange rate + free capital movement: here free capital movement implies that the covered interest parity holds. Hence to keep the exchange rate $E_t = E^e_{t+1} = \bar{E}$, the central bank needs to set the interest rate $i_t$ to match $i^\ast$. Doing so, it loses monetary autonomy. As an example, we have most EU countries prior to the adoption of the Euro.
2. Independent monetary policy + free capital movement: here, again due to the uncovered interest parity, setting $i_t$ implies that the exchange rate will be adjusted. Therefore, the country will be forced to adopt a floating currency value. Example: the United States.
3. Fixed exchange rate + independent monetary policy: to achieve this you would need to disable the effects of the interest parity. To do so, you need a closed economy or heavy regulation of the capital flowing in and out of the country. Example: China prior to 2005.