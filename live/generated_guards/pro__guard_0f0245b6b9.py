def guard(features: dict, prediction: str) -> str:
    bb_pct_b = features.get('bb_pct_b', 0.5)
    volume_ratio = features.get('volume_ratio', 1.0)
    
    # Only take trades at extreme BB positions
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        # Validate direction alignment with extreme
        if prediction == "long" and bb_pct_b > 0.5:
            return "skip"
        if prediction == "short" and bb_pct_b < 0.5:
            return "skip"
        # Require confirmation via volume
        if volume_ratio < 0.8:
            return "skip"
        return prediction
    
    return "skip"