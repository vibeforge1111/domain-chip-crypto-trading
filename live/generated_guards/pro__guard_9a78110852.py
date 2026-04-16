def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extreme positions."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    if prediction == "long" and bb_pct_b > 0.90:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.10:
        return "skip"
    
    return prediction