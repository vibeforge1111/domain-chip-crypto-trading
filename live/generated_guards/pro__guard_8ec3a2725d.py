def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # High-confidence entry zones: bb_pct_b extreme (<0.05 or >0.95)
    # Confirm with RSI alignment
    if bb_pct_b < 0.05:
        # Lower band: confirm with RSI showing oversold conditions
        if rsi_14 > 55 or rsi_2h > 55:
            return "skip"
    
    if bb_pct_b > 0.95:
        # Upper band: confirm with RSI showing overbought conditions
        if rsi_14 < 45 or rsi_2h < 45:
            return "skip"
    
    return prediction