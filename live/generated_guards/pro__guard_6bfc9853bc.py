def guard(features: dict, prediction: str) -> str:
    # Filter: reject when RSI is extreme and momentum contradicts prediction
    rsi = features.get('rsi_14', 50)
    momentum = features.get('momentum_score', 0)
    if rsi > 68 and momentum < -0.15 and prediction == "long":
        return "skip"
    if rsi < 32 and momentum > 0.15 and prediction == "short":
        return "skip"
    
    # Filter: reject when price is at extreme BB position during high volatility
    bb_pos = features.get('bb_position', 0.5)
    vol_regime = features.get('volatility_regime', 0.5)
    if (bb_pos > 0.92 or bb_pos < 0.08) and vol_regime > 0.75:
        return "skip"
    
    return prediction