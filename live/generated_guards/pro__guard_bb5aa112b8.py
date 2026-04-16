def guard(features: dict, prediction: str) -> str:
    """Filter trades requiring extreme Bollinger Band positions with momentum confirmation."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi = features.get("rsi_14", 50)
    
    # Only trade at extreme BB positions for high-confidence entries
    if bb_pct_b >= 0.10 and bb_pct_b <= 0.90:
        return "skip"
    
    # Long: oversold BB + confirming bullish momentum
    if prediction == "long" and bb_pct_b < 0.10:
        if stoch_k < 20 and rsi < 40:
            return "skip"
    
    # Short: overbought BB + confirming bearish momentum  
    if prediction == "short" and bb_pct_b > 0.90:
        if stoch_k > 80 and rsi > 60:
            return "skip"
    
    return prediction