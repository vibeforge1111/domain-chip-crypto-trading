def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band position extremes and momentum confirmation."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_14 = features.get("rsi_14", 50)
    
    # Only allow trades at extreme BB positions (high confidence zones)
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        # Additional confirmation: stochastic not in extreme zone that contradicts
        if bb_pct_b < 0.05 and stoch_k < 20:
            return prediction
        if bb_pct_b > 0.95 and stoch_k > 80:
            return prediction
        return "skip"
    
    return "skip"