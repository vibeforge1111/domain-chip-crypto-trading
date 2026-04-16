def guard(features: dict, prediction: str) -> str:
    """Guard against momentum deceleration entries using macd_histogram."""
    macd = features.get('macd_histogram', 0)
    bb_pct = features.get('bb_pct_b', 0.5)
    
    # Skip long if macd shows bearish deceleration near upper band
    if prediction == 'long' and macd < -0.0003 and bb_pct > 0.7:
        return "skip"
    
    # Skip short if macd shows bullish deceleration near lower band
    if prediction == 'short' and macd > 0.0003 and bb_pct < 0.3:
        return "skip"
    
    return prediction