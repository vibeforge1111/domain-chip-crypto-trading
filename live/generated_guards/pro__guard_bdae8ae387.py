def guard(features: dict, prediction: str) -> str:
    """Filter trades with RSI extremes or low volatility consolidation."""
    rsi = features.get('rsi_14', 50)
    bb_w = features.get('bb_width', 0.5)
    
    # Skip long signals when overbought (potential reversal)
    if features.get('prediction') == 'long' and rsi > 65:
        return "skip"
    # Skip short signals when oversold (potential reversal)  
    if features.get('prediction') == 'short' and rsi < 35:
        return "skip"
    # Skip low volatility consolidation periods
    if bb_w < 0.25:
        return "skip"
    return prediction