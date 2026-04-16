def guard(features: dict, prediction: str) -> str:
    """Filter trades at overbought/oversold extremes using BB and Stochastic."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip longs when overbought (BB upper + Stochastic high)
    if prediction == "long" and bb_pct_b > 0.88 and stoch_k > 80:
        return "skip"
    
    # Skip shorts when oversold (BB lower + Stochastic low)
    if prediction == "short" and bb_pct_b < 0.12 and stoch_k < 20:
        return "skip"
    
    return prediction