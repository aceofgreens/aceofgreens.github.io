---
Title: Candlestick Tasseography
Date: 2026-09-09 12:00:00 +0000
Tags: econ
Slug: candlestick_tasseography
---

Modern technical analysis has roots in [Charles Dow's studies of market trends](https://en.wikipedia.org/wiki/Dow_theory) at the turn of the twentieth century. Since then, chart reading has expanded into a large collection of numerical indicators built from prices and trading volume. Their appeal is understandable: markets aggregate news, expectations, and trading decisions into a price history, and indicators offer a compact way to describe its trends, momentum, and volatility. Traders use these descriptions to inform timing, execution, and risk decisions. But the leap from describing yesterday's pattern to predicting tomorrow's return makes the subject controversial, as the apparent regularities often end up being stories fitted to noise. That tension makes the tools worth understanding. In this fun little article we'll examine a few widely used indicators, explain their arithmetic, and connect them to the trading mechanisms behind price movements.

**Candles.** Prices are plotted using *candles*. Each one summarizes one time interval using its opening, highest, lowest, and closing prices, abbreviated *OHLC*. Its body spans the open and close; its wicks extend to the high and low. Here green means the close is above the open, and red means it is below. A green candle can still close below the previous day's close after a downward overnight gap. Volume is the quantity traded during that interval, shown as bars below the price. Beneath each candle lies [market microstructure](https://en.wikipedia.org/wiki/Market_microstructure): incoming orders, cancellations, and available liquidity. The same order imbalance can move prices further in a shallower [order book](https://en.wikipedia.org/wiki/Order_book), so a large candle need not imply stronger conviction.

<!-- All figures below use simulated data, not an actual security. The first three share the same 120 daily candles, preceded by 100 bars used to initialize the calculations. The simulation deliberately changes drift and volatility to make the indicators' responses visible. Its dates are labels on a weekday grid, not a historical exchange calendar. The final figure uses a separate simulated window of 30 daily bars. These examples illustrate arithmetic and behavior; they provide no evidence of profitable trading rules. -->

**Trend.** Trend indicators are about understanding the direction of movement. Since prices are noisy, we can average them within a temporal neighborhood of the last observed one. Let $C_t$ be the closing price of bar $t$. A simple moving average, or SMA, gives equal weight to the last $n$ closes:

$$
\operatorname{SMA}_{n,t} = \frac{1}{n}\sum_{i=0}^{n-1} C_{t-i}.
$$

It's basically a low-pass filter on the price. It can be calculated from the closing price $C$, the average high and low $(H+L)/2$, the OHLC mean $(O+H+L+C)/4$ or other similar combinations. An exponential moving average, or EMA, gives more weight to recent observations, which makes it track the prices movements more closely:

$$
\operatorname{EMA}_{n,t} = \alpha C_t + (1-\alpha)\operatorname{EMA}_{n,t-1},
\qquad \alpha = \frac{2}{n+1}.
$$

Both smooth the price history. The EMA reacts more strongly to the latest close than the same-period SMA; a longer window generally responds more slowly. The chart compares a 20-bar SMA, a 20-bar EMA, and a 50-bar SMA. Twenty daily bars are roughly a trading month. These window lengths are conventions, not special constants of markets.

<figure>
  <img class="theme-swap big_img" src="/images/trading_indicators/trend_light.svg?v=layout-4" data-light="/images/trading_indicators/trend_light.svg?v=layout-4" data-dark="/images/trading_indicators/trend_dark.svg?v=layout-4" alt="Simulated daily candlesticks with 20-period SMA, 20-period EMA, 50-period SMA, and trading volume." loading="lazy">
  <figcaption>Fig. 1. The 50-bar average turns down later than the shorter averages after the summer peak. The volume bars show simulated activity; their colors follow each candle's open-to-close direction.</figcaption>
</figure>

A rising average describes an upward trend over its chosen horizon. One famous strategy involves two movign averages: you buy when a short moving average crosses above a long-term one, and sell when it drops below it. Of course, the crossing occurs only after enough prices have moved to change the averages, so there's a delay. In a sideways market, repeated crossings can produce *whipsaws*: alternating signals followed by reversals. Smoothing reduces noise at the cost of delay. [Kaufman's adaptive moving average](https://www.tradingview.com/support/solutions/43000773012-kaufman-s-adaptive-moving-average-kama/) adjusts this tradeoff using an *efficiency ratio*: net price displacement divided by total distance traveled.

**Momentum.** Momentum refers to how "intense" a price movement is relative to its past. The [Relative Strength Index](https://www.fidelity.com/learning-center/trading-investing/technical-analysis/technical-indicator-guide/RSI) compares upward and downward close-to-close changes. Define $\Delta C_t=C_t-C_{t-1}$, gains $g_t=\max(\Delta C_t,0)$, and losses $\ell_t=\max(-\Delta C_t,0)$. For the usual 14-bar RSI, smooth gains and losses separately using Wilder's recursion:

$$
G_t = \frac{13G_{t-1}+g_t}{14}, \qquad
L_t = \frac{13L_{t-1}+\ell_t}{14}, \qquad
\operatorname{RSI}_t = 100-\frac{100}{1+G_t/L_t}.
$$

To start the computation, initialize $G_t$ with the mean of the first 14 $g_t$ terms and similarly $L_t$ with the $\ell_t$ terms. They show the mean "strength" of up and down, respectively. From the 15th change onward, update $G$ and $L$ using the recursive EMA formulas above. The ratio $G_t/L_t$ represents the "strength" of up relative to down movements. We further scale it to lie between 0 and 100; 50 means smoothed gains and losses are equal. If only losses are zero, RSI is 100; if only gains are zero, it is 0. For an entirely flat history, the accompanying code uses 50.

Above 70 is conventionally called *overbought*, and below 30 *oversold*. These describe recent momentum, not fundamental value. A strong trend can keep RSI at an extreme for a long time; crossing 70 does not imply that a reversal is due. However, a high RSI value above 70 becomes more sensitive to small price decreases than a intermediate value around 50.

**Divergence between slow and fast trends.** A classic indicator, built from EMAs is the [Moving Average Convergence/Divergence](https://en.wikipedia.org/wiki/MACD). It's the difference of a 12-bar short and a 26-bar long trends. As a formula, and with the usual settings, it is:

$$
M_t = \operatorname{EMA}_{12,t}(C)-\operatorname{EMA}_{26,t}(C),
\qquad S_t=\operatorname{EMA}_{9,t}(M),
\qquad H_t=M_t-S_t.
$$

$M$ is the MACD line. A positive $M_t$ means the fast price average is above the slow one. This could happen if the price breaks out of a downtrend, or if a slow uptrend suddenly accelerates. $S$ is the *signal line*. It simply smoothes out that information, at the cost of introducing some delay. $H$ the histogram. A positive histogram means that recent momentum is strengtening relative to its recent average. Note: the histogram can turn negative while MACD remains positive and price continues rising. So $H_t$ acts loosely like a second-order derivative, describing the acceleration of a trend. Unlike RSI, MACD is unbounded and measured in price units, so its magnitude is not directly comparable across differently priced assets.

<figure>
  <img class="theme-swap big_img" src="/images/trading_indicators/momentum_light.svg?v=layout-4" data-light="/images/trading_indicators/momentum_light.svg?v=layout-4" data-dark="/images/trading_indicators/momentum_dark.svg?v=layout-4" alt="The same simulated daily candles above an RSI panel with 30 and 70 thresholds and a MACD panel with signal line and histogram." loading="lazy">
  <figcaption>Fig. 2. RSI spends much of June and early July above 70 while prices continue rising. In October the MACD histogram turns positive while MACD remains below zero.</figcaption>
</figure>

See above how the MACD histogram is zero where the MACD and Signal lines cross. This is by design. Also, the MACD and RSI are heavily correlated. This should not be surprising, given that they're all calculated from the same closing prices. Their agreement is therefore partly mechanical. These indicators are not independent pieces of evidence about the future. Their agreement does not make the future more predictable. Even persistent buying or selling can coexist with nearly unpredictable returns, as liquidity adjusts and price impact changes.

**Volatility.** [Bollinger Bands](https://en.wikipedia.org/wiki/Bollinger_Bands) is another classic indicator that places an envelope around a moving average. With the conventional settings, the middle is a 20-bar SMA and the bands are two rolling standard deviations away:

$$
\sigma_t = \sqrt{\frac{1}{20}\sum_{i=0}^{19}(C_{t-i}-\operatorname{SMA}_{20,t})^2},
\qquad B_t^{\pm}=\operatorname{SMA}_{20,t}\pm 2\sigma_t.
$$

Here the standard deviation uses a divisor of 20. Bands widen when recent closing prices become more dispersed and narrow when they cluster together. A narrow *squeeze* identifies compression, but does not specify the direction of a subsequent move. Price can also follow the upper or lower band during a trend. Touching a band alone is not a reversal signal. However, breaking out of the bands can be (as much as anything else).

Note the limitations of the Bollinger Bands envelope. The envelope is not a 95% confidence interval for the next price. Consecutive calculations share 19 observations, and no statistical model establishes a predictive probability for the next price. This is not to say that volatility itself cannot be forecastable: turbulent periods tend to cluster, a property modeled by [ARCH/GARCH](https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity).

**Trading range.** Sometimes we care about the trading range in a period. The ordinary high-to-low range $H-L$ captures that movemen. However, if there's a jump between yesterday's close and today's open, this is not taken into account. The [Average True Range](https://en.wikipedia.org/wiki/Average_true_range) addresses this. For each candle, *true range* takes the largest of its intraday range and the distances from the previous close to its high and low; ATR then smooths this quantity over time:

$$
\operatorname{TR}_t = \max\{H_t-L_t,\ |H_t-C_{t-1}|,\ |L_t-C_{t-1}|\},
\qquad \operatorname{ATR}_t=\frac{13\operatorname{ATR}_{t-1}+\operatorname{TR}_t}{14}.
$$

ATR estimates the recent typical magnitude of a candle's range, including gaps, in price units. An ATR of $3$ says that recent candles have spanned about $3$ by this measure. It does not say that the next candle will remain within $3$, or whether it will rise or fall. A rise in ATR from $1$ to $3$ means recent ranges have expanded in either direction. To compare differently priced assets, one can express it as $100\operatorname{ATR}_t/C_t$.

<figure>
  <img class="theme-swap big_img" src="/images/trading_indicators/volatility_light.svg?v=layout-4" data-light="/images/trading_indicators/volatility_light.svg?v=layout-4" data-dark="/images/trading_indicators/volatility_dark.svg?v=layout-4" alt="Simulated daily candles inside 20-period Bollinger Bands, with a lower panel showing 14-period ATR as trading ranges change." loading="lazy">
  <figcaption>Fig. 3. Bollinger Bands describe dispersion of closing prices around their mean. ATR measures candle ranges and gaps. The two respond to different aspects of the same history.</figcaption>
</figure>

ATR therefore provides a scale for judging whether a move is small or large relative to recent activity, which can be used for setting your stop losses or limit prices. Consider the following though. Suppose you've set two stop losses, one at $2\times$ ATR, and one at $4\times$ ATR. An unexpected drop triggers your first stop loss, which leads to more selling, which increases the ATR for that day. This makes your second stop loss out of line with the new ATR. So ATR-based trading rules provide hardly any guarantees in terms of following a prescribed strategy. 

**Volume-weighting.** Volume is the total quantity traded during a bar. If three trades exchange 100, 200, and 50 shares, the volume is 350 shares; each trade is counted once, rather than once for the buyer and again for the seller. An ordinary volume chart groups trading by time, whereas a *volume profile* groups it by price, such as the number of shares traded near $50.

Suppose we fix a given time period, called a session. To find the average price paid during a trading session, such as one trading day, we should give larger trades more weight. The [Volume-Weighted Average Price](https://www.interactivebrokers.com/campus/glossary-terms/volume-weighted-average-price-vwap/) divides the total amount spent by the total quantity traded. If transaction $j$ exchanges $v_j$ shares at price $p_j$, the average up to time $t$ is:

$$
\operatorname{VWAP}_t = \frac{\sum_{j\leq t}p_jv_j}{\sum_{j\leq t}v_j}.
$$

For example, 100 shares traded at 50 dollars and 300 shares at 52 dollars give a VWAP of 51.50 dollars. It is closer to 52 because more shares traded there. Session VWAP includes all trades since the session opened and starts over at the next opening.

Traders use VWAP to judge the prices they obtained: buying below the VWAP for the comparison period means paying less than that period's average, but the price could still fall afterward. Order size also matters. An individual buying a few shares usually moves the price very little; a large fund may split its purchase into smaller orders to reduce its own impact on the price, at the cost of waiting longer. The resulting sequence of purchases can reflect the need to complete one large order, rather than repeated predictions of a rise.

The chart below treats 30 trading days as one comparison period, with one candle per day. For the volume calculations, assume all of each day's shares trade at its closing price $C_i$. The blue line is then $\operatorname{VWAP}_t=\sum_{i=1}^{t}C_iV_i/\sum_{i=1}^{t}V_i$, accumulating from day 1 without a daily reset. This is a simplifying assumption for assigning volume, while the candles still show each day's full price range. The bars below show volume by day; the profile on the right adds that same volume into 12 closing-price ranges across all 30 days. Longer horizontal bars identify the ranges where more shares traded under our assumption. The dashed line marks the final VWAP.

<figure>
  <img class="theme-swap big_img" src="/images/trading_indicators/vwap_light.svg?v=layout-4" data-light="/images/trading_indicators/vwap_light.svg?v=layout-4" data-dark="/images/trading_indicators/vwap_dark.svg?v=layout-4" alt="Thirty simulated daily candlesticks with cumulative closing-price VWAP, daily volume below, and a volume profile on the right sharing the price axis." loading="lazy">
  <figcaption>Fig. 4. Thirty simulated trading days, with all volume assigned to each day's close. The blue curve averages prices up to each day; the side profile summarizes the entire period. Its dashed line marks the final VWAP.</figcaption>
</figure>

**Conclusion**. Technical indicators summarize past trading; their formulas alone establish no reliable predictive power. In an informationally efficient market, prices already reflect available information, so an obvious, repeatable profit opportunity tends to disappear as traders exploit it. Yet shared rules can affect prices: if many traders buy after the same moving-average crossover, their orders may push the price higher and attract further buying. Similar positive feedback appears in stop-loss cascades. Such effects can make a pattern partly self-fulfilling, but they depend on other traders' behavior and available liquidity, and do not guarantee profits after costs.

<script>
(function () {
  const sheet = document.getElementById('theme-stylesheet');
  if (!sheet) return;
  const apply = () => {
    const dark = /\/dark\.css(\?|$)/.test(sheet.href);
    document.querySelectorAll('img.theme-swap').forEach(img => {
      const next = dark ? img.dataset.dark : img.dataset.light;
      if (img.getAttribute('src') !== next) img.setAttribute('src', next);
    });
  };
  apply();
  new MutationObserver(apply).observe(sheet, { attributes: true, attributeFilter: ['href'] });
})();
</script>
