# Monte-Carlo-option-pricing
Python implementation of Asian option pricing using Geometric Brownian Motion and Monte Carlo simulation.

# Monte Carlo Pricing of an Arithmetic Asian Call Option

## 1. Introduction

Asian options are path-dependent derivatives whose payoff depends on the average price of the underlying asset over time. Since arithmetic Asian options generally do not have closed-form solutions, Monte Carlo simulation is commonly used for pricing.

This project implements two Monte Carlo approaches:
- Crude Monte Carlo simulation
- Antithetic variate variance reduction

The goal is to compare their pricing accuracy and efficiency.

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

Independent random paths are generated and the discounted payoffs are averaged. The standard error is estimated as:

$$
SE=\frac{s}{\sqrt{N}}
$$

### Antithetic Variates

For each random vector $Z$, an additional path is generated using $-Z$. The two discounted payoffs are averaged:

$$
W_i=\frac{1}{2}(X_i^+ + X_i^-)
$$

This introduces negative correlation between simulations and reduces variance.

## 4. Implementation

Parameters:

$$
S_0=100,\quad K=100,\quad r=0.05,\quad \sigma=0.2,\quad T=1
$$

with daily monitoring:

$$
M=252
$$

Simulation size:
- Crude Monte Carlo: 20,000 paths
- Antithetic Variates: 10,000 antithetic pairs

The implementation uses vectorized NumPy operations for efficient path generation.

## 5. Results

| Method | Estimated Price | Standard Error | Variance Ratio |
|---|---:|---:|---:|
| Crude Monte Carlo | 5.7495 | 0.0565 | 1.00x |
| Antithetic Variates | 5.7940 | 0.0394 | 2.06x |

The antithetic variate method achieves a lower standard error, demonstrating improved simulation efficiency through variance reduction.
