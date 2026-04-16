def guard(features: dict, prediction: str) -> str:
    rsi_14 = features.get('rsi_14', 50)
    momentum_score = features.get('momentum_score', 0)
    bb_width = features.get('bb_width', 0)
    volume_ratio = features.get('volume_ratio', 1)
    
    # Momentum divergence: skip when RSI extreme but momentum contradicts direction
    if prediction == "long" and rsi_14 > 70 and momentum_score < -0.2:
        return "skip"
    if prediction == "short" and rsi_14 < 30 and momentum_score > 0.2:
        return "skip"
    
    # Low volatility squeeze with high volume: potential false breakout, skip
    if bb_width < 0.15 and volume_ratio > 1.8:
        return "skip"
    
    return prediction