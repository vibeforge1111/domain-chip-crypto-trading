def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow entries when price is at extreme Bollinger Band positions
    if bb_pct_b < 0.05 or bb_pct_b > 0.95:
        return prediction
    return "skip"