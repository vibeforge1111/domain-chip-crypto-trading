def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB position and Stochastic."""
    bb = features.get("bb_pct_b", 0.5)
    stoch = features.get("stoch_k", 50)
    
    # Skip long signals at extreme overbought (BB upper + stoch overbought)
    if prediction == "long" and bb > 0.85 and stoch > 80:
        return "skip"
    
    # Skip short signals at extreme oversold (BB lower + stoch oversold)
    if prediction == "short" and bb < 0.15 and stoch < 20:
        return "skip"
    
    return prediction