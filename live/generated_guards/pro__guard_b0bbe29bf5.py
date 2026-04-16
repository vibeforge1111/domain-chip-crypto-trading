def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes and RSI confirmation."""
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    
    # Long entry: bb_pct_b < 0.05 (extreme lower band) AND RSI confirming oversold
    if prediction == "long":
        if bb_pct_b >= 0.05 or rsi_14 >= 35:
            return "skip"
    
    # Short entry: bb_pct_b > 0.95 (extreme upper band) AND RSI confirming overbought
    if prediction == "short":
        if bb_pct_b <= 0.95 or rsi_14 <= 65:
            return "skip"
    
    return prediction