def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vol = features.get("volume_ratio", 1.0)
    
    # High-confidence entries at Bollinger Band extremes with volume confirmation
    if prediction == "long" and (bb >= 0.10 or vol < 0.8):
        return "skip"
    if prediction == "short" and (bb <= 0.90 or vol < 0.8):
        return "skip"
    
    return prediction