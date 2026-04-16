def guard(features: dict, prediction: str) -> str:
    """Filter trades too close to fair value (VWAP) with momentum confirmation."""
    vwap_dev = features.get('vwap_deviation', 0)
    stoch_k = features.get('stoch_k', 50)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Reject trades too close to VWAP (fair value)
    if abs(vwap_dev) < 0.003:
        return "skip"
    
    # Reject long signals with bearish 2h context
    if prediction == "long" and rsi_2h < 45:
        return "skip"
    
    # Reject short signals with bullish 2h context
    if prediction == "short" and rsi_2h > 55:
        return "skip"
    
    # Reject extreme stochastic readings (exhaustion risk)
    if stoch_k > 90 or stoch_k < 10:
        return "skip"
    
    return prediction