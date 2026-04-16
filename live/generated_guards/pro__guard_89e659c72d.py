def guard(features: dict, prediction: str) -> str:
    """Align entries with broader 2h trend using rsi_2h and stochastics."""
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    
    # Skip longs when broader trend extremely overbought (counter-trend risk)
    if prediction == "long" and rsi_2h > 76:
        return "skip"
    
    # Skip shorts when broader trend extremely oversold (bounce risk)
    if prediction == "short" and rsi_2h < 24:
        return "skip"
    
    # Additional filter: skip if stochastics in extreme zone opposite to prediction
    if prediction == "long" and stoch_k > 85:
        return "skip"
    if prediction == "short" and stoch_k < 15:
        return "skip"
    
    return prediction