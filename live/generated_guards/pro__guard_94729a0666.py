def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using bb_pct_b and stoch_k."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject longs when overbought: price near upper BB and stoch overbought
    if prediction == "long" and bb_pct > 0.85 and stoch > 80:
        return "skip"
    
    # Reject shorts when oversold: price near lower BB and stoch oversold
    if prediction == "short" and bb_pct < 0.15 and stoch < 20:
        return "skip"
    
    return prediction