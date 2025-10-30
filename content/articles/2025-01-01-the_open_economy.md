---
Title: The Open Economy
Date: 2025-01-01 07:00:00 +0200
Tags: econ
slug: open_economy
---

We've previously explored the basic workings of closed economies. Now it's time to consider different national economies in relation to each other. This will lead us to topics like exchange rates, imports and exports, and currency wars. It is an important topic that provides a convenient frame of reference in which to ground current world developments and historical events. Finally, it holds curious intellectual concepts like the impossible trinity.

The openness of an economy has multiple dimensions: *openness in goods markets* refers to the ability of consumers and firms to choose between domestic and foreign goods, unencumbered by tariffs and quotas; *openness in financial markets* allows investors to choose between domestic and foreign financial assets; *openness in factor markets* allows firms to choose where to set up production and workers to choose where to work.

**Openness in goods markets**. The demand for domestic and foreign goods is determined predominantly by the real exchange rate, which represents the price of domestic goods in terms of real foreign goods. The real exchange rate is unobservable. Instead we can measure the nominal exchange rate, which is just the *price of the domestic currency in terms of the foreign currency*. It tells us how many foreign units we need to exchange for a single domestic unit, i.e. $E = \frac{F}{D}$. One foreign unit buys $1/E$ domestic units. One domestic unit buys $E$ foreign ones. To calculate the real exchange rate, which shows *the price of domestic goods in terms of foreign goods*, denoted $\epsilon$, we proceed as follows. The domestic price level $P$ buys $E P$ units of foreign currency. At the foreign price level $P^\ast$, this is $E P / P^\ast$ foreign goods:

$$
\epsilon = \frac{E P}{P^\ast}.
$$

On the macro level, absolute values of the real exchange rate are not interpretable, due to the price index $P$, but rates of change are meaningful. A real appreciation, i.e. an increase in $\epsilon$, can be caused either if $E$ increases, or if $P/P^\ast$ increases. It's also possible that the nominal exchange rate $E$ increases, while the real exchange rate $\epsilon$ decreases. An increase in $\epsilon$ makes the domestic currency stronger relative to the foreign one, so it buys more of its units.

**Openness in financial markets**. With free capital flows between countries, people face the decision of whether to hold domestic assets or foreign assets. Usually they have little point in holding foreign currency because it cannot be used to buy domestic goods. If we simplify and ignore the exceptions, of which there are plenty, it only matters how people choose to hold domestic versus foreign interest paying assets.

Now, an important relation holds between exchange rates and returns of financial assets. A US citizen can invest 1 USD in a 1 year US bond, and will obtain $(1 + i)$ USD at the end. Alternatively, he can convert to pounds, obtain $E$ GBP, buy a 1 year UK bond, and obtain $E(1 + i^\ast)$ GBP next year. He can then convert back to USD to obtain $E(1 + i^\ast)/E^e_{t+1}$ USD where $E^e_{t+1}$ is the expected nominal exchange rate for the next year. Disregarding transaction costs and risk, open financial markets means that people will use arbitrage to equalize the profits from these two opportunities:

$$
(1 + i_t) = (1 + i^\ast_t) \frac{E_t}{E^e_{t+1}} = \frac{1 + i_t^\ast}{[1 + (E^e_{t+1} - E_t)/E_t]} \Rightarrow i_t \approx i_t^\ast - \frac{E^e_{t+1} - E_t}{E_t}
$$

This is called the *uncovered interest rate parity* condition. Uncovered means that the investor does not hedge, i.e. does not “cover” the foreign exchange risk using forward or futures contracts. Instead, the investor simply converts currency at the spot rate, invests in the foreign asset at the foreign interest rate, and then converts back at the (unknown) future spot rate, exposing themselves to potential currency fluctuations. The last equation shows that the domestic interest rate is approximately equal to the foreign one, adjusted according to the expected domestic appreciation. Here $i_t^\ast$ and $E^e_{t+1}$ are exogeneous and if we assume the central bank sets the interest rate, then $i_t$ is also exogeneous. $E_t$ is what adjusts so as to remove arbitrage.

**Demand for domestic goods**. In an open economy the demand for domestic goods now includes, apart from the usual components, imports $IM$ and exports $X$. The imports, paid in foreign currency, are converted into domestic goods by dividing by the real exchange rate:

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

where for simplicity we've assumed that the central bank sets the interest rate, inflation is 0, the expected future exchange rate is fixed, and $P/P^\ast = 1$. By setting the interest rate, an equilibrium exchange rate is determined. This then affects indirectly equilibrium output and the trade balance.

**Impossible trinity**. The model presented so far is called [Mundell-Fleming](https://en.wikipedia.org/wiki/Mundell%E2%80%93Fleming_model). And from it comes an important result, called the policy trilemma. In short, it states that a country cannot have at the same time a *fixed foreign exchange rate*, *free capital movement*, and *independent monetary policy*. To see why, conside the following:

1. Fixed exchange rate + free capital movement: here free capital movement implies that the uncovered interest parity holds. Hence to keep the exchange rate $E_t = E^e_{t+1} = \bar{E}$, the central bank needs to set the interest rate $i_t$ to match $i^\ast$. Doing so, it loses monetary autonomy. As an example, we have most EU countries prior to the adoption of the Euro.
2. Independent monetary policy + free capital movement: here, again due to the uncovered interest parity, setting $i_t$ implies that the exchange rate will be adjusted. Therefore, the country will be forced to adopt a floating currency value. Example: the United States.
3. Fixed exchange rate + independent monetary policy: to achieve this you would need to disable the effects of the interest parity. To do so, you need a closed economy or heavy regulation of the capital flowing in and out of the country. Example: China prior to 2005.

**Short run vs medium run**. In the short run, when prices $P$ and $P^\ast$ are fixed, the real exchange rate $\epsilon$ is determined only by the nominal one $E$. Furthermore, under a flexible exchange rate, $i_t$, together with $i^\ast_t$ and $E^e_{t+1}$, determine $E_t$. Therefore the country can rely on expansionary monetary policy to reduce the real exchange rate and boost output and improve the trade balance. However, if the exchange rate is fixed (pegged), then the country loses its ability to use monetary policy. So, in the short run, it seems flexible exchange rates are more favourable.

In the medium run the real exchange rate can change even with a fixed currency. This is because the prices $P$ and $P^\ast$ can change. Let's express the real interest rate as $r = i - \pi^e$. With a fixed currency rate $\bar{E}$ and when $i = i^\ast$, the IS relation becomes:

$$
Y = C(Y - T) + I(Y, i^\ast - \pi^e) + G + NX(Y, Y^\ast, \frac{EP}{P^\ast}).
$$

The Philips curve relation $\pi - \pi^e = (\alpha/L)(Y - Y_n)$ states that when $Y$ is greater than $Y_n$, prices start to rise. And so does the real exchange rate. The main conclusion is that *in the medium run under a currency peg, the real exchange rate increases if and only if the domestic country inflates faster than the foreign one*. If country A inflates more slowly than country B, its real exchange rate decreases, which makes its goods cheaper and more competitive. The increased exports eventually push the country to equilibrium at potential output. To speed up this process, it is possible to do manual *devaluations* and *revaluations* of the fixed nominal exchange rate.

Now, again under fixed exchange rates, consider the following situation. We start with $E_t = \bar{E}$, pegged to a country with lower inflation. This means that $\epsilon$ is increasing and the domestic country has a slowly worsening trade balance. Investors become anxious and they start expecting a devaluation, $\Delta^e E = (E^e_{t+1} - E_t)/E_t$. Now, to maintain the peg, the domestic central bank has a few options. It can try to convince the market that it will not devalue, but usually talk is cheap. It can also increase the interest rate to $i_t = i^\ast + \Delta^e E$, which in principle could be devastating for the economy.

What happens if the CB decides to increase rates but by less than $\Delta^e E$? Investors are not convinced, they will sell their domestic bonds, convert to foreign currency and buy foreign bonds, triggering a huge capital outflow and even a nominal depreciation. To maintain the peg, the CB has to stand ready to buy domestic currency and sell foreign currency. In doing so, it loses most of its reserves of foreign currency. That's roughly how exchange rate crises work.

**Flexible exchange rates**. In reality the uncovered interest parity condition is as not as simple as described so far. We derived it only for 1 future year, but it should be valid for any number of future years. A more realistic version, for $n$ years ahead is:

$$
E_t = \frac{(1+i_t) \prod_{i=1}^n (1 + i^e_{t+i})}{(1 + i^\ast_t) \prod_{i=1}^n (1 + i^\ast_{t+i})} E^e_{t+n+1}
$$

This shows that the current exchange rate depends on both the expected exchange rate many years ahead, and the expected interest rate many years ahead. Accurate prediction is *very* difficult. As a result, countries that decide to operate under flexible exchange rates must accept the fact that they will be exposed to substantial exchange rate fluctuations over time.

**Different exchange rate regimes**. Given all of the reasoning above, what exchange rate regime is best? Apart from floating and fixed exchange rates other options are:

- Optimal currency areas - when countries adopt the same currency. By doing so, they adopt a fixed exchange rate among each other. It is believed this makes sense if the countries face similar shocks so that they would have acted similarly from the start. If they don't face similar shocks, they should have high price and wage flexibility, so that they can change $\epsilon$ through $P$ and not through $E$.
- Hard pegs, currency boards. If the CB is inflating to fund a budget deficit, it may be useful to *prevent* it from expanding the money supply in certain situations. A currency board is a monetary authority that issues domestic currency only when it is fully backed by a foreign reserve currency, maintaining a fixed exchange rate. Alternatively, dollarization is the process of a country adopting a foreign currency (typically the US dollar) as its official legal tender, entirely replacing its domestic currency.

**Historic context**. The current exchange rate situation is chaotic - floating exchange rates, volatility, exchange controls, competitive devaluations, warring currency blocs, crises. How did we get here? What happened to the gold standard? We'll close off with a historic analysis from Rothbard:

1. Classical gold standard, 1815-1914. Currencies were defined in terms of gold, implying fixed exchange rates. There was effectively one *money*, which facilitated trade, investment, and international division of labor. Currencies were redeemable in gold and this acted as a limit to inflation. If a country inflated its paper currency, $\epsilon$ would increase and its trade balance would worsen. Foreign countries would then redeem their reserves for gold, causing a steady outflow of gold from the inflating country.
2. World War 1 and after. To fund the catastrophic WW1, many governments inflated heavily and went off the gold standard (though the US did not), effectively declaring their own bankruptcy. People started recognizing this as the threshold to international disaster.
3. The gold exchange standard (Britain and US), 1926-1931. Britain wanted to return to the gold standard at the pre-war parity for reasons of national prestige. This meant fixing the pound at a strong nominal value relative to gold and other currencies, i.e. it wanted wanted $\text{X}/\text{GBP}$ and $\text{GOLD}/\text{GBP}$ to be high, where $\text{X}$ was any foreign currency. But given that it had inflated more than other countries, $\epsilon = EP/P^\ast$ was too high and the pound was overvalued. In order to avoid its goods being overpriced, it had to deflate ($P\downarrow$). It didn't want to, as countries generally want to keep inflating. So the idea was to force other countries to redefine at very weak currencies, so that 
$\text{GOLD}/\text{X}$ was low. The system established was one where the US kept the gold standard, Britain redeemed pounds not only in gold, but also in dollars, while other countries redeemed in pounds. Hence, when Britain was inflating and its trade balance was worsening, other countries could not redeem their piling up pounds for gold. The US was induced to also inflate so that Britain does not lose its gold reserves to the US. Eventually, countries got swamped with pounds and expectations deteriorated. The system collapsed in 1931 with Britain and the other countries going off the gold standard again.
4. Fluctuating fiat currencies, 1931-1945. General chaos abounded with trade barriers and monetary warfare between currency blocs. International trade and investment came to a virtual standstill. In 1933-34 the US went off the gold standard in a vain attempt to get out of the depression. Yet a small tie to gold remained: the dollar was redeemable in gold not to citizens, but only to foreign governments and central banks. Overall a disastrous period.
5. [Bretton Woods](https://en.wikipedia.org/wiki/Bretton_Woods_system), 1945-1968. After WW2, the US held the majority of the world's gold. A new system was established where the dollar was fixed in terms of gold and was redeemable only to foreign governments and central banks. Other currencies were pegged to the dollar and were redeemable only in dollars. The dollar was in high demand because countries needed to maintain their pegs and also because currency rates were fixed at their pre-WW2 values. Being in shortage, foreign governments did not rush to convert their dollar reserves into gold, which allowed the US to inflate steadily for many years. Eventually, because of massive amounts of inflation, foreign governments were becoming more skeptical and wanting to redeem.
6. Bretton Woods unraveling, 1968-1971. The US had promised to convert gold at \$35 per troy ounce. Yet European citizens could sell their dollars for gold in the free gold exchanges, for example at London and Zurich, and there the price was much higher. In order to keep the dollar at \$35 an ounce, the US had to support that price by leaking out gold from its dwindling stock. A specially-designed two-tiered gold system did not improve the situation.
7. End of Bretton Woods. On August 15, 1971 the US went totally off gold. For the first time in history, the dollar was completely fiat, without being backed by gold.
8. The [Smithsonian agreement](https://en.wikipedia.org/wiki/Smithsonian_Agreement), 1971-1973. Another system of fixed exchange rates was designed with the price of gold revalued to \$38, all while the dollar was itself unbacked. This also failed, as foreign countries one by one decided not to keep holding dollars to maintain their pegs.
9. Floating fiat currencies. Since the failure of the Smithsonian agreement international relations have been plagued by currency wars, competitive devaluations, capital controls, tariffs and quotas. Most exchange rates float according to market forces rather than being fixed to gold or to each other. Central banks still hold gold as part of their reserves, but its price is market-driven, not set by governments.