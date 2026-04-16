def guard(features: dict, prediction: str) -> str:
    """Filters trades based on wick-body composition and volatility state."""
    # Skip if wick dominates body (weak/rejection candle)
    if features['upper_wick_ratio'] > 0.65 or features['lower_wick_ratio'] > 0.65:
        return "skip"
    
    # Skip low-volume expansions (potential fakeouts)
    if features['range_pct'] > 2.0 and features['volume_ratio'] < 0.7:
        return "skip"
    
    # Skip if RSI in extreme zone without strong trend
    if (features['rsi_14'] < 30 or features['rsi_14'] > 70) and abs(features['ema_slope']) < 0.1:
        return "skip"
    
    return prediction