def guard(features: dict, prediction: str) -> str:
    bb_position = features.get('bb_position', 0.5)
    rsi_14 = features.get('rsi_14', 50)
    volatility_regime = features.get('volatility_regime', 0.5)
    trend_strength = features.get('trend_strength', 0)
    
    # Skip if price is in middle of BB range (no clear direction)
    if 0.35 <= bb_position <= 0.65:
        return "skip"
    
    # Skip if market is low volatility and RSI is neutral
    if volatility_regime < 0.4 and 40 <= rsi_14 <= 60:
        return "skip"
    
    # Skip if trend is weak regardless of other signals
    if trend_strength < 0.3:
        return "skip"
    
    return prediction