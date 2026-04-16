def guard(features: dict, prediction: str) -> str:
    """Guard function using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Only trade at BB extremes
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        # Additional confirmation with stochastic
        if bb_pct_b < 0.05 and stoch_k < 25:
            return prediction  # Strong oversold + lower band
        if bb_pct_b > 0.95 and stoch_k > 75:
            return prediction  # Strong overbought + upper band
        return "skip"
    
    return "skip"