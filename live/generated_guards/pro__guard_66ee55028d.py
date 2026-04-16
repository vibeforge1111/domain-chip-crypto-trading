def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    volume_ratio = features.get("volume_ratio", 1.0)
    
    # Focus: Only trade at extreme BB positions (< 5% or > 95%)
    in_extreme = bb_pct_b < 0.05 or bb_pct_b > 0.95
    if not in_extreme:
        return "skip"
    
    # Confirm with RSI: longs need oversold, shorts need overbought
    if prediction == "long" and rsi_14 < 35:
        return prediction
    if prediction == "short" and rsi_14 > 65:
        return prediction
    
    return "skip"