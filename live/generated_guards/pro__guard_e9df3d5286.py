def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using volatility and momentum alignment."""
    # True compression: low bb_width AND low atr_ratio
    is_compressed = features['bb_width'] < 0.12 and features['atr_ratio'] < 0.75
    
    if is_compressed:
        # False compression: price near upper band but momentum bearish
        if features['bb_pct_b'] > 0.75 and features['macd_histogram'] < -0.0002:
            return "skip"
        # False compression: volume/momentum divergence at extremes
        if features['obv_slope'] < 0 and features['stoch_k'] < 25:
            return "skip"
        # Conflicting signals: VWAP far below but stoch overbought
        if features['vwap_deviation'] < -0.01 and features['stoch_k'] > 80:
            return "skip"
    
    # Skip if wide bands but RSI 2H diverging strongly
    if features['bb_width'] > 0.2 and features['rsi_2h'] < 35:
        if features['stoch_d'] > 70:
            return "skip"
    
    return prediction