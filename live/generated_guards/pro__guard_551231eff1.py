def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering.

    Args:
        features: Dict with keys like stoch_k, stoch_d, volume_ratio
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    if prediction == "long":
        # Only long on bullish %K/%D crossover in oversold zone
        if stoch_k <= stoch_d:
            return "skip"
        if stoch_d > 25:
            return "skip"
    
    elif prediction == "short":
        # Only short on bearish %K/%D crossover in overbought zone
        if stoch_k >= stoch_d:
            return "skip"
        if stoch_d < 75:
            return "skip"
    
    return prediction