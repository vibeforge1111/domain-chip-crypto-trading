def guard(features: dict, prediction: str) -> str:
    """Guard using bb_pct_b extremes as high-confidence entry zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Only allow entries at extreme BB positions
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Reject longs when 2h RSI shows overbought condition
    if prediction == "long" and rsi_2h > 75:
        return "skip"
    
    # Reject shorts when 2h RSI shows oversold condition
    if prediction == "short" and rsi_2h < 25:
        return "skip"
    
    return prediction