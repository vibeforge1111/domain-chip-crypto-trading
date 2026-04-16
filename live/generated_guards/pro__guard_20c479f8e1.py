def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with momentum confirmation."""
    bb = features.get('bb_pct_b', 0.5)
    macd = features.get('macd_histogram', 0)
    stoch_k = features.get('stoch_k', 50)
    
    # High-confidence BB extremes: <0.05 or >0.95
    if bb < 0.05 and prediction == "long" and macd > 0:
        return prediction
    if bb > 0.95 and prediction == "short" and macd < 0:
        return prediction
    
    return "skip"