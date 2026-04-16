def guard(features: dict, prediction: str) -> str:
    """Filter trades at extreme overbought/oversold levels using BB position and Stochastic."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject longs when both BB upper band AND stochastic overbought
    if prediction == "long" and bb_pct > 0.85 and stoch > 80:
        return "skip"
    
    # Reject shorts when both BB lower band AND stochastic oversold
    if prediction == "short" and bb_pct < 0.15 and stoch < 20:
        return "skip"
    
    return prediction