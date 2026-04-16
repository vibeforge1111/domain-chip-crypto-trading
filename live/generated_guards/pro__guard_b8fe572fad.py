def guard(features: dict, prediction: str) -> str:
    """Filter trades when both Bollinger Band position and Stochastic show extreme overbought/oversold."""
    bb_pct = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Reject longs when overbought: BB near upper band AND stoch above 80
    if prediction == "long" and bb_pct > 0.85 and stoch > 80:
        return "skip"
    
    # Reject shorts when oversold: BB near lower band AND stoch below 20
    if prediction == "short" and bb_pct < 0.15 and stoch < 20:
        return "skip"
    
    return prediction