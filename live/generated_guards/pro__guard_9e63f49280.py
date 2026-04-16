def guard(features: dict, prediction: str) -> str:
    # True compression: low BB width AND low ATR ratio
    in_compression = features['bb_width'] < 0.15 and features['atr_ratio'] < 0.8
    
    if in_compression:
        # False compression: price stretched from fair value
        if abs(features['vwap_deviation']) > 0.02:
            return "skip"
        
        # Wider timeframe overbought/oversold → false compression, skip
        if features['rsi_2h'] > 75 or features['rsi_2h'] < 25:
            return "skip"
        
        # Stoch extremes suggest exhaustion, not true compression
        if features['stoch_k'] > 80 or features['stoch_k'] < 20:
            return "skip"
    
    return prediction