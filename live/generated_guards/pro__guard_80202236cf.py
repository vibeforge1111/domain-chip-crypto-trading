def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extreme positions."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Long signals should occur near lower band (bb_pct_b < 0.05)
    if prediction == "long" and bb_pct_b >= 0.05:
        return "skip"
    
    # Short signals should occur near upper band (bb_pct_b > 0.95)
    if prediction == "short" and bb_pct_b <= 0.95:
        return "skip"
    
    return prediction