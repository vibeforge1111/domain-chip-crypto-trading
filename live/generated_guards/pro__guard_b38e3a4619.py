def guard(features: dict, prediction: str) -> str:
    """Filter trades with conflicting signals or high uncertainty candles."""
    # Reject if RSI and BB position disagree significantly
    if features['rsi_14'] > 70 and features['bb_position'] < 0.7:
        return "skip"
    if features['rsi_14'] < 30 and features['bb_position'] > 0.3:
        return "skip"
    
    # Reject low volume trades in high volatility
    if features['volatility_regime'] > 0.6 and features['volume_ratio'] < 0.7:
        return "skip"
    
    # Reject high wick candles (uncertainty)
    if features['upper_wick_ratio'] > 0.6 or features['lower_wick_ratio'] > 0.6:
        return "skip"
    
    return prediction