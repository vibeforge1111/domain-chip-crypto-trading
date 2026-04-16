def guard(features: dict, prediction: str) -> str:
    """Filter trades when Bollinger Bands and Stochastic confirm extreme overbought/oversold."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Both indicators confirm overbought zone
    overbought = bb_pct_b > 0.88 and stoch_k > 82
    
    # Both indicators confirm oversold zone
    oversold = bb_pct_b < 0.12 and stoch_k < 18
    
    # Reject longs at overbought extremes, shorts at oversold extremes
    if prediction == "long" and overbought:
        return "skip"
    if prediction == "short" and oversold:
        return "skip"
    
    return prediction