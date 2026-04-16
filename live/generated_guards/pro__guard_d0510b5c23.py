def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration via small positive MACD histogram with stoch confirmation."""
    macd_h = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Small positive histogram + elevated stoch = momentum deceleration
    if 0 < macd_h < 0.0008 and stoch_k > 70:
        return "skip"
    return prediction