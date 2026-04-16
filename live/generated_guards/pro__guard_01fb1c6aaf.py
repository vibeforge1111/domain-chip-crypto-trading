def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes with stochastic confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        if not (bb_pct_b < 0.10 and stoch_k < 25):
            return "skip"
    elif prediction == "short":
        if not (bb_pct_b > 0.90 and stoch_k > 75):
            return "skip"
    
    return prediction