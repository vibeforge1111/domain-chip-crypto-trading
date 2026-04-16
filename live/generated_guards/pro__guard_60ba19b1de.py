def guard(features: dict, prediction: str) -> str:
    """Filter trades during true vs false compression setups."""
    atr_ratio = features.get("atr_ratio", 1.0)
    bb_width = features.get("bb_width", 1.0)
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Detect true compression: both low volatility and narrow bands
    true_compression = atr_ratio < 0.75 and bb_width < 0.35
    
    if true_compression:
        # Skip if momentum is exhausted (extreme RSI on compression = false signal)
        if rsi_14 < 30 or rsi_14 > 70:
            return "skip"
        # Skip if wider timeframe disagrees with direction
        if prediction == "long" and rsi_2h < 40:
            return "skip"
        if prediction == "short" and rsi_2h > 60:
            return "skip"
    
    return prediction