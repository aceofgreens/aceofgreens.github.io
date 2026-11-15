---
Title: Factor Models and Risk Decomposition
Date: 2026-11-13 18:30:00 +0000
Tags: econ
Slug: factor_models_risk_decomposition
---

Previously we explored [modern portfolio optimization](https://aceofgreens.github.io/portfolio_optimization_and_capm.html) from mostly a theoretical perspective, where everything started from a "known" expected future return and covariance. In the real world, producing these estimates is where most of the work happens. Equity risk managers have to estimate how thousands of stocks co-move, and separate those phenomena and patterns that affect entire sectors from those that are genuinely specific to a company. This post is a practical, real-world, step-by-step description of how institutional fundamental factor risk models, the dominant framework for this task, are built.


Suppose we have a universe of $N = 40$ stocks. The daily return of stock $i$ on day $t$ is $r_{i,t}$. We can stack the returns of the companies on a particular day into a vector $\mathbf{r}_t$ with array shape $(N, 1)$. The core idea of a factor model is that we will model the return as a linear combination of factor returns. In the language of statistics, we formulate a [multiple linear regression](https://en.wikipedia.org/wiki/Multiple_linear_regression).

$$
\mathbf{r}_t = \mathbf{B}_t \mathbf{f}_t + \mathbf{\epsilon}_t
$$

Here $\mathbf{f}_t$ is a $(K, 1)$-shaped vector of **factor returns** realized that day. It represents the daily returns of a number of *factors* (i.e. phenomena, common patterns, return drivers). Examples would be *Size*, *Country*, *Momentum*, *Sector*, *Value*, etc. These are the independent variables. $\mathbf{B}_t$ is a **loadings (exposure) matrix** of shape $(N, K)$ that shows how much company $i$ is exposed to factor $k$. Lastly, $\mathbf{\epsilon}_t$ is the $(N, 1)$ vector of **idiosyncratic returns**. They represent stock-specific events, uncorrelated with the factors.

Therefore, this approach naturally models returns as a superposition of factors, like how a wave is a superposition of smaller tides, swells, and ripples:

1. **A broad tide** that lifts or lowers all boats together (**Market factor**),
2. **Medium swells** pushing boats with similar characteristics (**Style and Industry factors** like *Size*, *Value*, and *Momentum*),
3. **Local ripples** unique to each boat (**Idiosyncratic return** $\epsilon_{i,t}$).

Why impose this structure at all? Because estimating a full $N \times N$ covariance matrix directly from sample returns requires $N(N+1)/2$ pairwise parameters. Even for $N = 40$ stocks that is $820$ covariances, and for a $2{,}000$-stock universe it explodes to over $2$ million noisy numbers. With $K = 4$ factors and $N = 40$ stocks, a factor model compresses those $820$ parameters down to $K(K+1)/2 + N = 10 + 40 = 50$ estimates.

Okay, now that we've covered the concept of a factor model, how do we estimate and use it in practice? Typically, there are essentially three steps: processing that needs to happen before the market opens, estimations that happen after the market closes, and a loop that repeats these two steps for many days.

#### Pre-Market Open: Standardizing the Loadings Matrix

Before trading begins on day $t$, we gather raw company descriptors - for example, Market Cap (in billions), Book-to-Price ratios, leverage ratios, 3- to 5-year historical growth rates, cash flows, profitability indicators, historical beta, liquidity, and trailing 12-month returns. Because raw numbers live on incompatible scales and can contain huge outliers, we preprocess each style characteristic across the universe:

1. **Transform skewed quantities**, e.g., $\ln(\text{Market Cap})$, as firm sizes span different magnitudes.
2. **Clip** extreme outliers beyond $\pm 3$ stds so a meme stock does not hijack the regression.
3. **Z-score cross-sectionally** across all $N$ stocks so every style column has mean $0$ and std $1$:

$$
B_{i,k} = \frac{x_{i,k} - \mu_k}{\sigma_k}.
$$

We then add a constant `Market` column of $1.0$s, and `0/1` country and sector indicators if we include these. In addition, many of the standardized descriptors are blended into style factors. For example, in its classic GEM3 model, MSCI Barra computes the momentum factor as the exponentially weighted cumulative log excess return over roughly two years, skipping the most recent month. Similarly, the Leverage factor is computed by blending market-implied leverage, balance-sheet debt-to-assets, and book leverage. After blending the raw descriptors, the new composite factors are orthogonalized against each other and re-standardized. It's also common to add a stock's Beta, computed with time-series regression, as another descriptor.

This entire process populates the matrix $\mathbf{B}_t$. The row $(\mathbf{B}_t)_i$ tells us stock $i$'s exact style profile before the bell rings - for instance, `Size = +0.94` and `Value = +0.73` means a larger-than-average, cheaper-than-average stock.

#### Post-Market Close: Cross-Sectional Regression

At 4:00 PM, we observe the vector of daily stock returns $\mathbf{r}_t$. We know $\mathbf{B}_t$ and $\mathbf{r}_t$, and we want to infer the $K$ hidden factor waves $\mathbf{f}_t$ and the $N$ stock-specific ripples $\mathbf{\epsilon}_t$. So we run a single **cross-sectional linear regression across all $N$ stocks**. Cross-sectional means that it's for a particular day, across all of the $N$ stocks. This is different from a time-series regression (like in [CAPM](https://en.wikipedia.org/wiki/Capital_asset_pricing_model)), where we regress the historical returns of a single stock against a benchmark.

In practice, commercial models do not use equal-weighted [Ordinary Least Squares](https://en.wikipedia.org/wiki/Ordinary_least_squares) (OLS), because small-cap stocks have much higher idiosyncratic noise $\sigma_{\epsilon, i}^2$ and would pollute the factor estimates. Instead, they use [Weighted Least Squares](https://en.wikipedia.org/wiki/Weighted_least_squares) (WLS) with a diagonal weight matrix $\mathbf{W}$ (typically $W_{ii} \propto \sqrt{\text{Market Cap}_i}$). The estimated factor returns $\hat{\mathbf{f}}_t$ and residuals $\hat{\mathbf{\epsilon}}_t$ are:

$$
\hat{\mathbf{f}}_t = (\mathbf{B}_t^\top \mathbf{W} \mathbf{B}_t)^{-1} \mathbf{B}_t^\top \mathbf{W} \mathbf{r}_t, \qquad \hat{\mathbf{\epsilon}}_t = \mathbf{r}_t - \mathbf{B}_t \hat{\mathbf{f}}_t.
$$

<figure>
<img class="theme-swap" src="/images/factor_models/wls_regression_light.svg" data-light="/images/factor_models/wls_regression_light.svg" data-dark="/images/factor_models/wls_regression_dark.svg" alt="Post-market cross-sectional WLS regression across 40 stocks showing factor slope and idiosyncratic residuals">
<figcaption>Fig. 1. Cross-sectional WLS regression along the <code>Value</code> factor across $N = 40$ simulated stocks on Day 1 (bubble area $\propto \sqrt{\text{Market Cap}}$). The slope of the fitted line gives the daily factor return ($\hat{f}_{\text{Val}} = +0.77\%$), while vertical dashed segments show individual idiosyncratic residuals $\hat{\epsilon}_i$.</figcaption>
</figure>

That's how the factor returns are calculated. Relatively simple. Now look closely at the matrix multiplying $\mathbf{r}_t$. If we reshuffle it a bit and rename it, we can get:

$$
\mathbf{V} = \mathbf{W} \mathbf{B}_t (\mathbf{B}_t^\top \mathbf{W} \mathbf{B}_t)^{-1} \quad (N \times K) \qquad \Longrightarrow \qquad \hat{\mathbf{f}}_t = \mathbf{V}^\top \mathbf{r}_t.
$$

Every column $\mathbf{v}_k$ of $\mathbf{V}$ is a vector of *$N$ stock weights* (not factor weights). In other words, each estimated factor return $\hat{f}_{k,t}$ is literally the daily return of a tradable portfolio of stocks, called a **Factor-Mimicking Portfolio (FMP)**. To get the return of factor $k$, we simply need to hold a portfolio of all stocks, with weights given by $\mathbf{v}_k$. Thus, to obtain the *Size* return, we hold all stocks in the proportions given by, say, $\mathbf{v}_4$. To obtain the *Momentum* return, hold $\mathbf{v}_7$, etc.

If we hold a portfolio of stocks $\mathbf{w}$, what is its factor exposure? Well, it's simply $\mathbf{B}^\top \mathbf{w}$. What, then, is the exposure of the factor-mimicking portfolios? We get the identity matrix:

$$
\mathbf{B}_t^\top \mathbf{V} = \mathbf{B}_t^\top \mathbf{W} \mathbf{B}_t (\mathbf{B}_t^\top \mathbf{W} \mathbf{B}_t)^{-1} = \mathbf{I}_K.
$$

Thus, each FMP is *completely pure*: the `Value` FMP has an exposure of exactly $1.0$ to `Value` and $0.0$ to `Market`, `Size`, and `Momentum`. If you want to hold only Value stocks, an initial strategy might be to hold the top 10 Value stocks and short the bottom 10, but this almost always carries accidental Size and Momentum tilts. Instead, one should compute $\mathbf{V}$ and hold the corresponding allocation from there.

<figure>
<img class="theme-swap" src="/images/factor_models/fmp_purity_light.svg" data-light="/images/factor_models/fmp_purity_light.svg" data-dark="/images/factor_models/fmp_purity_dark.svg" alt="Stock weights across 40 names comparing a naive Value sort with the pure Value Factor-Mimicking Portfolio and unintended factor spill">
<figcaption>Fig. 2. Stock weights across $N = 40$ names sorted by <code>Value</code>: isolating pure <code>Value</code> exposure ($1$ with $0$ spill onto <code>Size</code>, <code>Momentum</code>, and <code>Market</code>) requires tailored weights from $\mathbf{V}$ across every stock, whereas a flat Top-10 minus Bottom-10 sort leaks $+0.29$ <code>Size</code> and $-0.25$ <code>Momentum</code> tilts.</figcaption>
</figure>

#### Daily Loop: Obtaining a Risk Model

A single day gives one snapshot $\hat{\mathbf{f}}_t$ and $\hat{\mathbf{\epsilon}}_t$. Repeating the calculations above at the end of every trading day for $T$ days (usually 252 market days for a calendar year) produces two stacked time-series matrices: $\hat{\mathbf{F}}$, shaped $(T, K)$, containing daily factor returns and $\hat{\mathbf{E}}$, shaped $(T, N)$, of daily idiosyncratic residuals. From those histories we compute two important covariance matrices:

- **Factor Covariance Matrix** $\hat{\mathbf{\Omega}}_f$. This is the $(K, K)$-shaped covariance matrix of $\hat{\mathbf{F}}$, measuring how volatile each factor is and how factors co-move (for instance, `Value` and `Momentum` often exhibit negative correlation).
- **Idiosyncratic Variance Matrix** $\hat{\mathbf{\Omega}}_\epsilon$. This is the $(N, N)$-shaped diagonal matrix of each stock's residual variance $\text{Var}(\hat{\mathbf{E}}_{:, i})$. It is diagonal *by assumption*, because we've assumed that all co-movement between stocks comes from the factors modeled. Any remaining movement is entirely company-specific.

Together with today's loadings matrix $\mathbf{B}_{\text{today}}$, these form the full forecast covariance matrix $\hat{\mathbf{\Omega}}_r$. It contains the variance and co-movement of the stock returns, mixing factor and idiosyncratic risks:

$$
\hat{\mathbf{\Omega}}_r = \mathbf{B}_{\text{today}} \hat{\mathbf{\Omega}}_f \mathbf{B}_{\text{today}}^\top + \hat{\mathbf{\Omega}}_\epsilon.
$$

Note a few key points:

- **What is live vs. historical:** $\mathbf{B}_{\text{today}}$ reflects today's live fundamentals and prices. $\hat{\mathbf{\Omega}}_f$ and $\hat{\mathbf{\Omega}}_\epsilon$ are for the last year, estimated from past $\hat{\mathbf{f}}_t$ and $\hat{\mathbf{\epsilon}}_t$, though real production models replace the simple equal-weighted 252-day average with exponentially decayed weights that put much heavier weight on the past 1–3 months, and are tuned for a ~2-month risk horizon.
- **What is assumed about the future:** We are *not* assuming past factor returns $\mathbf{f}_t$ will repeat. Rather, we assume two milder things: (a) the channels of co-movement persist (Value stocks will still co-move with Value stocks), and (b) volatility clusters (a factor or stock that was volatile recently is likely to remain volatile in the near term).
- **The future could still be unpredictable**: Reality is not stationary. Crowded factors like Momentum or Short Interest can look deceptively calm for months before unleashing a sudden "tsunami" (such as the 2009 momentum reversal) that backward-looking $\hat{\mathbf{\Omega}}_f$ completely missed, and then take months to decay back down. Some practical guardrails: do not rely on $\hat{\mathbf{\Omega}}_f$ alone - put hard static caps on raw factor exposures, keep idiosyncratic variance at $\ge 75\%$ of total portfolio variance, and run a statistical ([PCA](https://en.wikipedia.org/wiki/Principal_component_analysis)) model as a second opinion to catch newly emerging hidden factors before they appear in $\mathbf{B}_t$.

#### Risk Attribution and Hedging

Now that we have our factor model, how do we use it? Given a portfolio weight vector $\mathbf{w}$, shaped $(N, 1)$, its factor exposures are $\mathbf{b}_p = \mathbf{B}^\top \mathbf{w}$, and its total variance splits cleanly into factor variance plus idiosyncratic variance:

$$
\sigma_p^2 = \mathbf{w}^\top \hat{\mathbf{\Omega}}_r \mathbf{w} = \underbrace{\mathbf{b}_p^\top \hat{\mathbf{\Omega}}_f \mathbf{b}_p}_{\text{Factor Variance}} + \underbrace{\mathbf{w}^\top \hat{\mathbf{\Omega}}_\epsilon \mathbf{w}}_{\text{Idio Variance}}.
$$

This is the first immediate benefit of a factor model: risk attribution. It allows you to decompose your total portfolio volatility into volatility coming from each factor, and idiosyncratic volatility for every company. This can enable strategies like risk parity rebalancing, where you upweight/downweight factors or assets with risk below/above a desired proportion.

Suppose a portfolio manager holds an equal-weighted basket of their 8 cheapest `Value` stocks. It may very well happen that this unhedged portfolio naturally carries $b_{\text{Mkt}} = 1.0$, big tilts toward `Value` and `Size`, and could even end up with 90% of its variance coming from broad factor swings rather than stock picking. In hedge funds, portfolio managers need to justify their ability to pick the right stocks. This happens by constructing a portfolio that is dominated by idiosyncratic returns and risks. All the factor risks need to be hedged out. Because $\mathbf{B}^\top \mathbf{V} = \mathbf{I}_K$, this becomes a one-line subtraction using the FMPs:

$$
\mathbf{w}_{\text{hedged}} = \mathbf{w} - \mathbf{V} \mathbf{b}_p \qquad \Longrightarrow \qquad \mathbf{B}^\top \mathbf{w}_{\text{hedged}} = \mathbf{b}_p - (\mathbf{B}^\top \mathbf{V}) \mathbf{b}_p = \mathbf{0}.
$$

Neutralizing with $\mathbf{V} \mathbf{b}_p$ drives every factor exposure to $0$ and raises the share of idiosyncratic variance to $100\%$. The portfolio $\mathbf{w}_\text{hedged}$ now reflects purely the manager's stock-picking ability. This is the same kind of logic as in simple hedging in CAPM: if you hold \$100 in a stock with a beta of $\beta=1.0$ and you short \$100 of the market, you are now exposed only to that stock's idiosyncratic returns and risks.

Note that with hedging, if you hold a portfolio that is exposed only to idio risks and returns, it's possible to construct trading strategies with very good Sharpe ratios. Better research and forecasting can help with this endeavor. The total volatility $\sigma_\text{hedged}$ will be smaller than that of the long-only portfolio. However, this is where leverage comes in. Using leverage doesn't change the Sharpe ratio, so it's very common to apply *regearing* as a final step: scaling up the leverage so that the total portfolio volatility (or mean return) reaches a desired target level.

<figure>
<img class="theme-swap big_img" src="/images/factor_models/hedging_regearing_light.svg" data-light="/images/factor_models/hedging_regearing_light.svg" data-dark="/images/factor_models/hedging_regearing_dark.svg" alt="Risk decomposition before and after factor hedging and regearing alongside 252-day simulated cumulative returns">
<figcaption>Fig. 3. Left: hedging an $8$-stock Value basket with $\mathbf{w} - \mathbf{V}\mathbf{b}_p$ strips out the factor block, dropping annualized volatility from $26.3\%$ ($10\%$ idio variance) to $5.1\%$ ($100\%$ idio); $2.9\times$ leverage restores volatility to a $15.0\%$ target. Right: over a $252$-day simulation with zero-mean factor noise, hedging raises Sharpe from $1.29$ to $1.88$, and regearing scales up that smoother idiosyncratic return stream without factor drawdowns.</figcaption>
</figure>


#### Factor Models Today

Across institutional equities and hedge funds, this framework remains the industry standard:

* **Off-the-Shelf Risk Platforms:** Most institutional equity managers rely on commercial platforms such as **MSCI Barra** and **SimCorp Axioma** (alongside Bloomberg and FactSet), all built on $\hat{\mathbf{\Omega}}_r = \mathbf{B} \hat{\mathbf{\Omega}}_f \mathbf{B}^\top + \hat{\mathbf{\Omega}}_\epsilon$. Rather than rebuilding the daily data pipeline in-house, firms use these feeds as shared infrastructure because of their **interpretability**: a risk manager can attribute losses to concrete drivers (*"excess exposure to Momentum and Software"*) instead of an abstract eigenvector.
* **The Multi-Manager Standard:** Multi-manager ("pod shop") hedge funds, such as Citadel, Millennium, and Balyasny, build their equity platforms directly around this playbook: isolating idiosyncratic stock-picking alpha, enforcing tight factor neutrality, budgeting idiosyncratic risk, and scaling leverage to steady volatility targets.
* Outside market-neutral funds, usage shifts by mandate:
    * **Traditional long-only funds** (mutual funds, pension mandates) use Barra and Axioma heavily, but stay near $\beta \approx 1.0$ and manage tracking error ($\sqrt{\text{Var}(R_p - R_b)}$) against a benchmark like the S&P 500 or MSCI World rather than hedging factors to zero.
    * **Macro, credit, options, and multi-asset desks** rely more on macroeconomic factor models, duration/[Greeks](https://en.wikipedia.org/wiki/Greeks_(finance)), [VaR/CVaR](https://en.wikipedia.org/wiki/Value_at_risk), and scenario stress tests.
    * **Retail / passive 60–40 portfolios** focus on low-cost index diversification and asset-class rebalancing rather than daily cross-sectional regressions.
* **How the Frontier Has Evolved:** Quant teams keep the fundamental model as an interpretable core and layer upgrades on top: multi-horizon fast-decaying covariances, covariance shrinkage (such as [Ledoit–Wolf](https://scikit-learn.org/stable/modules/generated/sklearn.covariance.LedoitWolf.html)), hybrid fundamental + PCA / machine-learning overlays, custom thematic factors, and real-time factor crowding monitors to flag synchronized unwinds early.

Ultimately, fundamental multi-factor models endure not because they predict tomorrow's winning factor or assume a stationary world, but because they give investors a transparent, disciplined way to measure the bets they are taking.

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
