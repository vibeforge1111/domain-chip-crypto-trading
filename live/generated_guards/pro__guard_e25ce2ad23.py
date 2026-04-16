def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression using BB width, ATR ratio, and BB position."""
    bb_width = features.get('bb_width', 1.0)
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    rsi_14 = features.get('rsi_14', 50)
    
    # True compression: low BB width AND low ATR (quiet before storm)
    is_compression = bb_width < 0.7 and atr_ratio < 0.8
    
    if is_compression and prediction != "skip":
        # False compression signals when price at extreme BB position
        if bb_pct_b > 0.92 or bb_pct_b < 0.08:
            return "skip"
        # Reject if stochastic is overbought/oversold during compression
        if stoch_k > 85 or stoch_k < 15:
            return "skip"
        # Reject if RSI divergence between timeframes (weak signal)
        if abs(rsi_2h - rsi_14) > 25:
            return "skip"
    
    return prediction