def guard(features: dict, prediction: str) -> str:
    """Align entries with broader trend using 2h RSI."""
    if prediction == "skip":
        return prediction
    
    rsi_2h = features.get("rsi_2h", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Longs need bullish 2h context, avoid extended lower band
    if prediction == "long" and (rsi_2h < 48 or bb_pct_b < 0.25):
        return "skip"
    
    # Shorts need bearish 2h context, avoid extended upper band
    if prediction == "short" and (rsi_2h > 52 or bb_pct_b > 0.75):
        return "skip"
    
    return prediction