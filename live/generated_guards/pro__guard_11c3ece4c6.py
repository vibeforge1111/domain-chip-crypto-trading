def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2h trend using rsi_2h."""
    rsi_2h = features.get('rsi_2h', 50)
    stoch_k = features.get('stoch_k', 50)
    
    # For longs, broader trend should not be oversold
    if prediction == "long" and rsi_2h < 42:
        return "skip"
    
    # For shorts, broader trend should not be overbought
    if prediction == "short" and rsi_2h > 58:
        return "skip"
    
    return prediction