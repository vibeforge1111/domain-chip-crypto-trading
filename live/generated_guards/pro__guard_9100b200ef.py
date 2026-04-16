def guard(features: dict, prediction: str) -> str:
    """Reject trades at Bollinger/Stochastic extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject longs at overbought extremes
    if prediction == "long" and bb_pct_b > 0.9 and stoch_k > 85:
        return "skip"
    
    # Reject shorts at oversold extremes
    if prediction == "short" and bb_pct_b < 0.1 and stoch_k < 15:
        return "skip"
    
    return prediction