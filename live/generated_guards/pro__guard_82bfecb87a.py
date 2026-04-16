def guard(features: dict, prediction: str) -> str:
    """Filter trades with conflicting momentum and volatility signals."""
    stoch_k = features.get('stoch_k', 50)
    rsi_14 = features.get('rsi_14', 50)
    bb_width = features.get('bb_width', 0)
    volatility_regime = features.get('volatility_regime', 0.5)
    
    # Skip if stoch extreme but RSI neutral (divergence warning)
    if (stoch_k > 80 or stoch_k < 20) and 40 < rsi_14 < 60:
        return "skip"
    
    # Skip if high volatility regime with narrow BB (chop/confusion)
    if volatility_regime > 0.7 and bb_width < 0.02:
        return "skip"
    
    return prediction