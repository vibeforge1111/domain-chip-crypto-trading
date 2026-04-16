def guard(features: dict, prediction: str) -> str:
    """Filter trades using extreme bb_pct_b zones with stoch confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Lower band extreme - potential long
    if bb_pct_b < 0.05 and prediction == "long":
        if stoch_k < 10:  # Already deeply oversold, may have bounced
            return "skip"
    
    # Upper band extreme - potential short
    if bb_pct_b > 0.95 and prediction == "short":
        if stoch_k > 90:  # Already deeply overbought, may have reversed
            return "skip"
    
    return prediction