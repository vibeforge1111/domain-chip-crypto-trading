def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using ATR ratio and Bollinger Band width."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_14 = features.get("rsi_14", 50)
    
    # True compression detected: both indicators show low volatility
    in_compression = atr_ratio < 0.7 and bb_width < 0.35
    
    if in_compression:
        # Price pinned to BB edge = no room for true squeeze
        if min(bb_pct_b, 1 - bb_pct_b) < 0.08:
            return "skip"
        
        # Stochastic exhaustion in compression
        if stoch_k < 15 or stoch_k > 85:
            return "skip"
        
        # Extreme RSI in compression
        if rsi_14 < 30 or rsi_14 > 70:
            return "skip"
    
    return prediction