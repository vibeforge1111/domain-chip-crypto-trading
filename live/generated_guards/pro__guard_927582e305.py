def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration using MACD histogram and confirm with stochastics."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if momentum is decelerating in overbought zone
    if macd_hist < -0.0003 and stoch_k > 75:
        return "skip"
    # Skip if MACD histogram is strongly negative with weak stochastics
    if macd_hist < -0.0008 and stoch_k < 30:
        return "skip"
    return prediction