def guard(features: dict, prediction: str) -> str:
    """Filter trades based on true vs false compression detection."""
    bb_width = features.get('bb_width', 0.2)
    atr_ratio = features.get('atr_ratio', 1.0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # True compression: tight BB + building ATR energy = valid setup
    # False compression: tight BB but dormant ATR = skip
    if bb_width < 0.12 and atr_ratio < 0.8:
        return "skip"
    
    # Stochastic extremes signal reversal risk
    if stoch_k > 85 or stoch_k < 15:
        return "skip"
    
    # Avoid fighting higher timeframe RSI direction
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"
    
    return prediction