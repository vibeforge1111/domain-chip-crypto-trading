def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum is decelerating (weak macd_histogram)."""
    macd_hist = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # Skip if momentum is weak (histogram near zero) and stochastic at extreme
    if abs(macd_hist) < 0.0003 and (stoch_k > 80 or stoch_k < 20):
        return "skip"
    return prediction