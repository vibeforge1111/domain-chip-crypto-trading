def guard(features: dict, prediction: str) -> str:
    """Skip trades at extreme overbought/oversold conditions using BB and Stochastic."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Overbought: BB near upper band AND Stochastic confirmation
    if prediction == "long" and bb_pct_b > 0.95 and stoch_k > 80 and stoch_d > 80:
        return "skip"
    
    # Oversold: BB near lower band AND Stochastic confirmation
    if prediction == "short" and bb_pct_b < 0.05 and stoch_k < 20 and stoch_d < 20:
        return "skip"
    
    return prediction