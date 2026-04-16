def guard(features: dict, prediction: str) -> str:
    """Reject trades when both BB position and Stochastic confirm extremes."""
    bb = features.get("bb_pct_b", 0.5)
    sk = features.get("stoch_k", 50)
    
    # Overbought: BB in upper zone + Stochastic overbought → skip longs
    if prediction == "long" and bb > 0.85 and sk > 80:
        return "skip"
    
    # Oversold: BB in lower zone + Stochastic oversold → skip shorts
    if prediction == "short" and bb < 0.15 and sk < 20:
        return "skip"
    
    return prediction