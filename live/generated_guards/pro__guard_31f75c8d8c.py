def guard(features: dict, prediction: str) -> str:
    """Candle integrity guard - reject signals with conflicting price action."""
    upper_wick = features.get('upper_wick_ratio', 0)
    lower_wick = features.get('lower_wick_ratio', 0)
    body = features.get('body_ratio', 0)
    rsi = features.get('rsi_14', 50)
    bb_width = features.get('bb_width', 0)
    
    # Reject longs with dominant upper wick (selling pressure in candle)
    if prediction == "long" and upper_wick > 0.38:
        return "skip"
    
    # Reject shorts with dominant lower wick (buying pressure in candle)
    if prediction == "short" and lower_wick > 0.38:
        return "skip"
    
    # Reject doji/indecision candles (small body, large wicks)
    if body < 0.25 and (upper_wick + lower_wick) > 0.65:
        return "skip"
    
    # Skip if extreme RSI and low volatility (choppy market)
    if bb_width < 0.02 and (rsi < 30 or rsi > 70):
        return "skip"
    
    return prediction