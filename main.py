from pricing import asian_crude, asian_anti, asian_control

# Model parameters
S0, K, r, sigma, T = 100.0, 100.0, 0.05, 0.2, 1.0
M, N = 252, 10000

# Benchmark:
price_crude, se_crude = asian_crude(S0, K, r, sigma, T, M, N = 2*N)
price_anti, se_anti = asian_anti(S0, K, r, sigma, T, M, N = N)
price_control, se_control = asian_control(S0, K, r, sigma, T, M, N = 2*N)
var_reduction_anti = (se_crude/se_anti) ** 2
var_reduction_ctrl = (se_crude/se_control) ** 2
print(
    f"Crude MC   | Price: {price_crude:.4f} | SE: {se_crude:.4f}"
    f"\nAntithetic | Price: {price_anti:.4f} | SE: {se_anti:.4f}"
    f"\nControl Variate | Price: {price_control:.4f} | SE: {se_control:.4f}"
    f"\n\nAntithetic variance reduction: {var_reduction_anti:.4f}"
    f"\nControl variance reduction: {var_reduction_ctrl:.4f}"
) 