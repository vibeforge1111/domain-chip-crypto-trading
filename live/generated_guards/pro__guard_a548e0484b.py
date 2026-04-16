def guard(features: dict, prediction: str) -> str:
    """Filter trades based on Bollinger Band position extremes."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    
    # Only allow long near lower band, short near upper band
    if prediction == "long" and bb_pct_b > 0.05:
        return "skip"
    if prediction == "short" and bb_pct_b < 0.95:
        return "skip"
    
    return prediction