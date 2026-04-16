def guard(features: dict, prediction: str) -> str:
    """Guard: filter trades not at extreme Bollinger Band positions."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only trade at extreme BB positions (< 5% or > 95%)
    if prediction == "long" and bb_pct_b < 0.05:
        return prediction
    if prediction == "short" and bb_pct_b > 0.95:
        return prediction
    
    return "skip"