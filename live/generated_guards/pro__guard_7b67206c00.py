def guard(features: dict, prediction: str) -> str:
    """Filter trades misaligned with volatility regime and candle structure."""
    if prediction == "skip":
        return prediction
    
    vol_regime = features.get("volatility_regime", 0.5)
    bb_width = features.get("bb_width", 0.1)
    body_ratio = features.get("body_ratio", 0.5)
    rsi = features.get("rsi_14", 50)
    
    # Skip low volatility regime with weak candle structure
    if vol_regime < 0.3 and body_ratio < 0.4:
        return "skip"
    
    # Skip BB squeeze (low volatility) without strong momentum
    if bb_width < 0.05 and vol_regime < 0.4:
        return "skip"
    
    # Skip weak signals when RSI is neutral
    if 45 < rsi < 55 and body_ratio < 0.5:
        return "skip"
    
    return prediction