def guard(features: dict, prediction: str) -> str:
    """Momentum divergence and confirmation guard.
    Filters trades where RSI and Stochastic disagree or volume lacks conviction.
    """
    rsi = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Skip if RSI-Stochastic divergence > 30 points (they disagree)
    if abs(rsi - stoch_k) > 30:
        return "skip"
    
    # Skip if stoch_k and stoch_d cross is recent (inconsistent signals)
    if abs(stoch_k - stoch_d) > 20:
        return "skip"
    
    # Skip if volume confirmation is weak on a potential move
    if volume_ratio < 0.5:
        return "skip"
    
    return prediction