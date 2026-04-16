def guard(features: dict, prediction: str) -> str:
    """Reject longs at upper BB + overbought Stoch, reject shorts at lower BB + oversold Stoch."""
    bb = features.get("bb_pct_b", 0.5)
    sk = features.get("stoch_k", 50)
    
    # Long signals at extreme overbought: reject
    if prediction == "long" and bb > 0.85 and sk > 80:
        return "skip"
    
    # Short signals at extreme oversold: reject
    if prediction == "short" and bb < 0.15 and sk < 20:
        return "skip"
    
    return prediction