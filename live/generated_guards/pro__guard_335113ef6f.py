def guard(features: dict, prediction: str) -> str:
    """Guard against momentum divergence and trend weakness trades."""
    if prediction == "skip":
        return prediction
    
    vol_surge = features.get("volume_ratio", 1.0) > 1.3
    mom_weak = features.get("momentum_score", 0.5) < 0.4
    no_trend = features.get("trend_strength", 0.5) < 0.3
    
    if vol_surge and mom_weak:
        return "skip"
    if no_trend and (vol_surge or mom_weak):
        return "skip"
    
    return prediction