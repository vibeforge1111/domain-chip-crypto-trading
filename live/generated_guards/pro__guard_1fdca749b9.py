def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using ATR, BB width, and momentum confirmation."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    macd_histogram = features.get("macd_histogram", 0)
    
    # True compression: low volatility with momentum conviction
    is_compressed = atr_ratio < 0.7 and bb_width < 0.35
    
    if is_compressed:
        # Require clear directional bias to avoid false breakouts
        momentum_confirmed = (stoch_k > 65 or stoch_k < 35) or (macd_histogram > 0.001 or macd_histogram < -0.001)
        rsi_confirmed = rsi_2h > 58 or rsi_2h < 42
        if not (momentum_confirmed and rsi_confirmed):
            return "skip"
    
    return prediction