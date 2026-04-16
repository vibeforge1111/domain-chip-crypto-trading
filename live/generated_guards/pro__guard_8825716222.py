def guard(features: dict, prediction: str) -> str:
    """Reject signals where wick imbalance contradicts price at BB extremes."""
    upper_wick = features.get("upper_wick_ratio", 0)
    lower_wick = features.get("lower_wick_ratio", 0)
    bb_pos = features.get("bb_position", 0.5)
    volatility = features.get("volatility_regime", 0.5)
    
    # Long at top of BBs with large upper wick = rejection, not continuation
    if upper_wick > 0.3 and bb_pos > 0.75 and prediction == "long":
        return "skip"
    
    # Short at bottom of BBs with large lower wick = rejection, not continuation
    if lower_wick > 0.3 and bb_pos < 0.25 and prediction == "short":
        return "skip"
    
    # Skip in low volatility with weak momentum
    if volatility < 0.4 and features.get("momentum_score", 0.5) < 0.35:
        return "skip"
    
    return prediction