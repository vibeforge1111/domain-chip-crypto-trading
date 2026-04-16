def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    
    # Only allow trades at extreme bb_pct_b positions
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # Additional confirmation: stoch should align with direction
    if prediction == "long" and stoch_k > 30:
        return "skip"
    if prediction == "short" and stoch_k < 70:
        return "skip"
    
    return prediction