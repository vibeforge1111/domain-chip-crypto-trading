def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions with momentum confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    stoch = features.get('stoch_k', 50)
    
    if prediction == "long":
        # Only allow longs at oversold extremes with stoch confirmation
        if bb >= 0.05 or stoch >= 20:
            return "skip"
    elif prediction == "short":
        # Only allow shorts at overbought extremes with stoch confirmation
        if bb <= 0.95 or stoch <= 80:
            return "skip"
    
    return prediction