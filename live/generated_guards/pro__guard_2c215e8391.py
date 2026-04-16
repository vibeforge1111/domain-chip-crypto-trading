def guard(features: dict, prediction: str) -> str:
    """Filter trades where compression forms but momentum fails to confirm."""
    # True compression: low BB width + elevated ATR (active tightening)
    is_compressed = features['bb_width'] < 0.1 and features['atr_ratio'] > 0.15
    
    if is_compressed:
        # Skip if stochastic is in extreme zone opposite to prediction
        if prediction == 'long' and features['stoch_k'] > 85:
            return 'skip'
        if prediction == 'short' and features['stoch_k'] < 15:
            return 'skip'
        
        # Skip if MACD histogram contradicts direction
        if prediction == 'long' and features['macd_histogram'] < -0.0001:
            return 'skip'
        if prediction == 'short' and features['macd_histogram'] > 0.0001:
            return 'skip'
        
        # Skip if OBV slope diverges (weak participation)
        if prediction == 'long' and features['obv_slope'] < 0:
            return 'skip'
        if prediction == 'short' and features['obv_slope'] > 0:
            return 'skip'
    
    return prediction