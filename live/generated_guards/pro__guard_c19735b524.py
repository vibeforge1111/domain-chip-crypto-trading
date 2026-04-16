def guard(features: dict, prediction: str) -> str:
    bb_pct = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Only allow trades at extreme bb_pct_b zones (<0.05 or >0.95)
    if bb_pct >= 0.05 and bb_pct <= 0.95:
        return "skip"
    
    # Filter longs: bb_pct < 0.05, reject if 2h RSI also oversold (weak context)
    if bb_pct < 0.05 and prediction == "long":
        if rsi_2h < 40:
            return "skip"
    
    # Filter shorts: bb_pct > 0.95, reject if 2h RSI also overbought
    if bb_pct > 0.95 and prediction == "short":
        if rsi_2h > 60:
            return "skip"
    
    return prediction