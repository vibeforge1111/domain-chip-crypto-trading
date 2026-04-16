def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow trades at extreme Bollinger Band positions (<0.05 or >0.95)
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        return prediction
    
    return "skip"