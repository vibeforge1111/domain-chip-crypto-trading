def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow trades at Bollinger Band extremes (<0.05 or >0.95)
    # These are high-confidence mean reversion zones
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction