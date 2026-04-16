def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB position and Stochastic."""
    if prediction == "skip":
        return prediction
    
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject longs at overbought extremes (BB upper + stoch > 80)
    if prediction == "long" and bb_pct > 0.85 and stoch > 80:
        return "skip"
    
    # Reject shorts at oversold extremes (BB lower + stoch < 20)
    if prediction == "short" and bb_pct < 0.15 and stoch < 20:
        return "skip"
    
    return prediction