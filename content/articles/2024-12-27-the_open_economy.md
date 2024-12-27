---
Title: The Open Economy
Date: 2024-12-27 07:00:00 +0200
Tags: econ
slug: open_economy
---

We've previously explored the basic workings of closed economies. Now it's time to consider different national economies in relation to each other. This will lead us to topics like exchange rates, imports and exports, and currency wars. It is an important topic that provides a convenient frame of reference in which to ground current world developments and historical events. Finally, it holds curious intellectual concepts like the impossible trinity.

The openness of an economy has multiple dimensions: *openness in goods markets* refers to the ability of consumers and firms to choose between domestic and foreign goods, unencumbered by tariffs and quotas; *openness in financial markets* allows investors to choose between domestic and foreign financial assets; *openness in factor markets* allows firms to choose where to set up production and workers to choose where to work.

**Openness in goods markets**. The demand for domestic and foreign goods is determined predominantly by the real exchange rate, which represents the price of domestic goods in terms of real foreign goods. The real exchange rate is unobservable. Instead we can measure the nominal exchange rate, which is just the ratio of the domestic currency to the foreign one. If the exchange rate between USD and GBP is 0.79, then $E = \frac{1 \text{ USD}}{1\text{ GBP}} = 0.79$. To calculate the real exchange rate, one multiplies $E$ with the price index $P$ to get the price of US goods in pounds, then divides by the price of UK goods $P^\ast$:

$$
\epsilon = \frac{E P}{P^\ast}
$$

On the macro level, absolute values of the real exchange rate are not interpretable, but rates of change are. A real appreciation can be caused either if $E$ increases, or if $P/P^\ast$ increases. It's also possible that the nominal exchange rate $E$ increases, while the real exchange rate $\epsilon$ decreases.

**Openness in financial markets**. With free capital flows between countries, people face the decision of whether to hold domestic assets or foreign assets. Usually they have little point in holding foreign currency because it cannot be used to buy domestic goods. If we simplify and ignore the exceptions, it only matters how people choose to hold domestic versus foreign interest paying assets.

Now, an important relation holds between exchange rates and returns of financial assets. A US citizen can invest 1 USD in a 1 year US bond, and will obtain $(1 + i)$ USD at the end. Alternatively, he can convert to pounds, obtain $E$ GBP, buy a 1 year UK bond, and obtain $E(1 + i^\ast)$ GBP next year. He can then convert back to USD to obtain $E(1 + i^\ast)/E^e_{t+1}$ where $E^e_{t+1}$ is the expected nominal exchange rate for next year. Open financial markets means that people will use arbitrage to equalize the profits from these two possibilities:

$$
(1 + i_t) = (1 + i^\ast_t) \frac{E_t}{E^e_{t+1}} = \frac{1 + i_t^\ast}{[1 + (E^e_{t+1} - E_t)/E_t]}.
$$

This is called the *uncovered interest rate parity* condition.