def guard(features: dict, prediction: str) -> str:
    """Filter for high-confidence Bollinger Band extreme entries with stoch confirmation."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Must be at extreme BB position
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Stochastic confirmation at extremes
    if bb_pct_b < 0.05 and stoch_k >= 80 and stoch_d >= 80:
        return prediction
    if bb_pct_b > 0.95 and stoch_k <= 20 and stoch_d <= 20:
        return prediction
    
    return "skip"