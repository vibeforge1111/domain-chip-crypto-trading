def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long entry: price at lower band with oversold confirmation
    if prediction == "long" and bb_pct_b < 0.05 and stoch_k < 25 and stoch_d < 25 and rsi_2h < 70:
        return prediction
    
    # Short entry: price at upper band with overbought confirmation
    if prediction == "short" and bb_pct_b > 0.95 and stoch_k > 75 and stoch_d > 75 and rsi_2h > 30:
        return prediction
    
    return "skip"