def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    obv_slope = features.get("obv_slope", 0)
    
    # High-confidence zones: bb_pct_b extremes + confirming momentum
    if prediction == "long" and (bb_pct_b > 0.05 or obv_slope <= 0):
        return "skip"
    if prediction == "short" and (bb_pct_b < 0.95 or obv_slope >= 0):
        return "skip"
    
    return prediction