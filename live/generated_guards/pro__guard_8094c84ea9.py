def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme zones with confirmation."""
    bb_pct = features.get("bb_pct_b", 0.5)
    rsi = features.get("rsi_14", 50)
    stoch_k = features.get("stoch_k", 50)
    
    # Long: bb_pct_b < 0.05 (oversold) + RSI confirmation
    if prediction == "long":
        if bb_pct >= 0.05 or rsi >= 35:
            return "skip"
    
    # Short: bb_pct_b > 0.95 (overbought) + RSI confirmation
    if prediction == "short":
        if bb_pct <= 0.95 or rsi <= 65:
            return "skip"
    
    return prediction