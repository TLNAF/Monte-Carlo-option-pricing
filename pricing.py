import numpy as np
from scipy.stats import norm

def asian_crude(S0, K, r, sigma, T, M, N, seed = 42):
    """Prices an Arithmetic Asian Call Option using vectorized Crude Monte Carlo."""
    np.random.seed(seed)
    dt = T/M
    
    Z = np.random.standard_normal((N, M))
    drift = (r - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * Z
    
    log_S = np.log(S0) + np.cumsum(drift + diffusion, axis = 1)
    S = np.exp(log_S)
    payoff = np.maximum(np.mean(S, axis = 1) - K, 0.0)
    discounted = np.exp(-r*T) * payoff
    
    price = np.mean(discounted)
    err = np.std(discounted, ddof = 1)/np.sqrt(N)
    return price, err
    
def asian_anti(S0, K, r, sigma, T, M, N, seed = 42):
    """Prices an Arithmetic Asian Call Option using Antithetic Variates.
    Generates N antithetic pairs (2N total paths)."""
    
    np.random.seed(seed)
    dt = T/M
    
    Z = np.random.standard_normal((N, M))
    drift = (r - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) # Leave Z and -Z for later antithetic
    
    log_S_pos = np.log(S0) + np.cumsum(drift + diffusion * Z, axis = 1)
    S_pos = np.exp(log_S_pos)
    payoff_pos = np.maximum(np.mean(S_pos, axis = 1) - K, 0.0)
    discounted_pos = np.exp(-r*T) * payoff_pos
    
    log_S_neg = np.log(S0) + np.cumsum(drift + diffusion * (-Z), axis = 1)
    S_neg = np.exp(log_S_neg)
    payoff_neg = np.maximum(np.mean(S_neg, axis = 1) - K, 0.0)
    discounted_neg = np.exp(-r*T) * payoff_neg
    
    W = 0.5 * (discounted_pos + discounted_neg)
    price = np.mean(W)
    err = np.std(W, ddof = 1)/np.sqrt(N)
    
    return price, err

def geom_asian(S0, K, r, sigma, T, M):
    """Calculates exact analytical price E[X] for discrete Geometric Asian Call."""
    sigma_G = sigma * np.sqrt((M + 1)*(2*M + 1)/(6 * M ** 2)) # Adjusted volatility
    mu_G = sigma_G**2/2 + (r - sigma**2/2)/2 * (M + 1)/ M # Adjusted growth rate
    
    x = sigma_G*np.sqrt(T) # Denominator
    d1 = (np.log(S0/K) + (mu_G + sigma_G**2/2)*T) / x
    d2 = d1 - x
    N_d1 = norm.cdf(d1)
    N_d2 = norm.cdf(d2)
    
    # Calculate E[X]
    E_X = np.exp(-r*T) * (S0 * np.exp(mu_G * T) * N_d1 - K * N_d2)
    return E_X

    
    
    