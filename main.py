from pricing import asian_crude, asian_anti
import numpy as np

# Model parameters
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
M, N = 252, 10000

# Benchmark:
price_crude, se_crude = asian_crude(S0, K, r, sigma, T, M, N = 2*N)
price_anti, se_anti = asian_anti(S0, K, r, sigma, T, M, N = N)
var_reduction = (se_crude/se_anti) ** 2
print(
    f"Crude MC   | Price: {price_crude:.4f} | SE:"
    f" {se_crude:.4f}\nAntithetic | Price: {price_anti:.4f} | SE: {se_anti:.4f}"
    f"\n\nVariance reduction: {var_reduction:.4f}"
) 