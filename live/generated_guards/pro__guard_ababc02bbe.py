def guard(features: dict, prediction: str) -> str:
    """Filter trades using bb_pct_b extremes with stochastic confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Long only at lower band extreme with oversold confirmation
    if prediction == "long" and not (bb_pct_b < 0.05 and stoch_k < 30):
        return "skip"
    
    # Short only at upper band extreme with overbought confirmation
    if prediction == "short" and not (bb_pct_b > 0.95 and stoch_k > 70):
        return "skip"
    
    return prediction