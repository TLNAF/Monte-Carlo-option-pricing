# Monte Carlo Pricing of an Arithmetic Asian Call Option

## 1. Introduction

Asian options are path-dependent derivatives whose payoff depends on the average price of the underlying asset over time. Since arithmetic Asian options generally do not have closed-form solutions, Monte Carlo simulation is commonly used for pricing.

This project implements and compares three approaches:
- Crude Monte Carlo simulation
- Antithetic variate variance reduction
- Control variate variance reduction using a geometric Asian option

The goal is to investigate how variance reduction techniques improve the efficiency of Monte Carlo pricing.

## 2. Model

The underlying asset follows a Geometric Brownian Motion:

$$
dS_t = rS_tdt+\sigma S_tdW_t
$$

The discretized simulation is:

$$
S_{t+\Delta t}=S_t\exp\left((r-\frac12\sigma^2)\Delta t+\sigma\sqrt{\Delta t}Z\right)
$$

where $Z\sim N(0,1)$.

The arithmetic Asian call payoff is:

$$
\max\left(\frac{1}{M}\sum_{i=1}^{M}S_{t_i}-K,0\right)
$$

The option price is estimated by discounting the average simulated payoff:

$$
\hat{V}=e^{-rT}\frac{1}{N}\sum_{i=1}^{N}Payoff_i
$$

## 3. Monte Carlo Methods

### Crude Monte Carlo

Independent paths are simulated and their discounted payoffs are averaged. The standard error is estimated as:

$$
SE=\frac{s}{\sqrt{N}}
$$

### Antithetic Variates

<<<<<<< HEAD
For each random vector $Z$, an additional path is generated using $-Z$. The two discounted payoffs are averaged:
=======
For each random vector \(Z\), a second path is generated using \(-Z\). The two discounted payoffs are averaged:
>>>>>>> 009c47a (Implemented geometric control variate and benchmarked results)

$$
W_i=\frac{1}{2}(X_i^+ + X_i^-)
$$

This creates negatively correlated simulations and reduces estimator variance.

### Control Variates

The discounted payoff of a geometric Asian option is used as a control variate because its expected value has a closed-form solution.

Let \(Y\) be the arithmetic Asian payoff and \(X\) the geometric Asian payoff. The adjusted estimator is:

\[
Y_{CV}=Y-c^*(X-E[X])
\]

where the optimal coefficient is estimated by:

\[
c^*=\frac{\operatorname{Cov}(Y,X)}{\operatorname{Var}(X)}
\]

## 4. Implementation

Parameters:

$$
S_0=100,\quad K=100,\quad r=0.05,\quad \sigma=0.2,\quad T=1
$$

with daily monitoring:

$$
M=252
$$

For a fair comparison, each method uses a total of 20,000 simulated paths:

- Crude Monte Carlo: 20,000 paths
- Antithetic Variates: 10,000 antithetic pairs
- Control Variates: 20,000 paths

The implementation uses vectorized NumPy operations for efficient path generation.

## 5. Results

| Method | Estimated Price | Standard Error | Variance Reduction |
|---|---:|---:|---:|
| Crude Monte Carlo | 5.7495 | 0.0565 | 1.00x |
| Antithetic Variates | 5.7940 | 0.0394 | 2.06x |
| Control Variates | 5.7805 | 0.0015 | 1353.80x |

The antithetic variate method reduces the standard error by approximately 30% relative to crude Monte Carlo.

The control variate method produces a much larger reduction in estimator variance, benefiting from the strong relationship between arithmetic and geometric Asian option payoffs.