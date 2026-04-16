def guard(features: dict, prediction: str) -> str:
    """Filters trades at Bollinger Band extremes with RSI exhaustion."""
    rsi = features.get('rsi_14', 50)
    bb_pos = features.get('bb_position', 0.5)
    trend = features.get('trend_strength', 0)
    
    # Skip long at upper band with overbought RSI and weak trend (reversal trap)
    if prediction == "long" and bb_pos > 0.9 and rsi > 70 and trend < 0.4:
        return "skip"
    
    # Skip short at lower band with oversold RSI and weak trend (reversal trap)
    if prediction == "short" and bb_pos < 0.1 and rsi < 30 and trend < 0.4:
        return "skip"
    
    return prediction