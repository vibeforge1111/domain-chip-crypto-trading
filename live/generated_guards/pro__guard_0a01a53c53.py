def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with stochastic confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        if bb_pct_b >= 0.05 or stoch_k >= 20:
            return "skip"
    
    if prediction == "short":
        if bb_pct_b <= 0.95 or stoch_k <= 80:
            return "skip"
    
    return prediction