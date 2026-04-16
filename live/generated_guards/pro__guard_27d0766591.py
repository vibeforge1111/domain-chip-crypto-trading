def guard(features: dict, prediction: str) -> str:
    """Reject trades at extreme overbought/oversold conditions."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject long at overbought extremes
    if prediction == "long" and bb_pct > 0.9 and stoch > 80:
        return "skip"
    # Reject short at oversold extremes
    if prediction == "short" and bb_pct < 0.1 and stoch < 20:
        return "skip"
    return prediction