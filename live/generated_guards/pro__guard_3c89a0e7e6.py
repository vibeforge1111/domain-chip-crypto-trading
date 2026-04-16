def guard(features: dict, prediction: str) -> str:
    """Reject trades when overbought/oversold extremes align with BB position."""
    stoch_k = features.get("stoch_k", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Skip longs when overbought (stoch_k > 80) AND price at upper band (bb_pct_b > 0.9)
    if prediction == "long" and stoch_k > 80 and bb_pct_b > 0.9:
        return "skip"
    
    # Skip shorts when oversold (stoch_k < 20) AND price at lower band (bb_pct_b < 0.1)
    if prediction == "short" and stoch_k < 20 and bb_pct_b < 0.1:
        return "skip"
    
    return prediction