def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme overbought/oversold conditions."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Skip longs when overbought (upper BB + high stoch)
    if prediction == "long" and bb_pct > 0.88 and stoch > 78:
        return "skip"
    
    # Skip shorts when oversold (lower BB + low stoch)
    if prediction == "short" and bb_pct < 0.12 and stoch < 22:
        return "skip"
    
    return prediction