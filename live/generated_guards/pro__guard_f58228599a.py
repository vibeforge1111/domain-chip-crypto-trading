def guard(features: dict, prediction: str) -> str:
    # Filter volatility expansions without volume confirmation (false breakouts)
    if features['atr_ratio'] > 1.5 and features['volume_ratio'] < 0.7:
        return "skip"
    
    # Filter counter-trend trades at Bollinger extremes without trend support
    if prediction == "long" and features['bb_position'] > 0.85 and features['trend_strength'] < 0.35:
        return "skip"
    if prediction == "short" and features['bb_position'] < 0.15 and features['trend_strength'] < 0.35:
        return "skip"
    
    return prediction