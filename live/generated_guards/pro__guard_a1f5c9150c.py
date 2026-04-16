def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_dev = features.get('vwap_deviation', 0)
    
    # Only allow trades at extreme BB positions with VWAP alignment
    if bb_pct_b < 0.05 and vwap_dev < -0.005 and prediction == "short":
        return prediction
    if bb_pct_b > 0.95 and vwap_dev > 0.005 and prediction == "long":
        return prediction
    
    return "skip"