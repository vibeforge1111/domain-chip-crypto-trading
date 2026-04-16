def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extremes with momentum confirmation."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    macd_histogram = features.get("macd_histogram", 0)
    stoch_k = features.get("stoch_k", 50)
    
    if prediction == "long":
        # Require price near lower band and bullish momentum
        if bb_pct_b >= 0.10:
            return "skip"
        if macd_histogram <= 0:
            return "skip"
            
    elif prediction == "short":
        # Require price near upper band and bearish momentum
        if bb_pct_b <= 0.90:
            return "skip"
        if macd_histogram >= 0:
            return "skip"
    
    return prediction