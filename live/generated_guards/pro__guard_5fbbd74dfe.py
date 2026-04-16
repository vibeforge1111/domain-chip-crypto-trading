def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    macd_histogram = features.get('macd_histogram', 0)
    
    # High confidence entry zones at band extremes
    if bb_pct_b < 0.05:  # Near lower band - potential long
        if prediction == "short":
            return "skip"
        if stoch_k < 20 and macd_histogram > 0:
            return prediction
        return "skip"
    
    if bb_pct_b > 0.95:  # Near upper band - potential short
        if prediction == "long":
            return "skip"
        if stoch_k > 80 and macd_histogram < 0:
            return prediction
        return "skip"
    
    # Outside extreme zones - stricter filtering
    if abs(vwap_deviation) > 0.02:
        return "skip"
    
    return prediction