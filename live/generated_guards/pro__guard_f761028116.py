def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes for high-confidence entries."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # High-confidence entry zones: extreme BB positions
    if prediction == "long" and bb_pct_b < 0.05:
        return prediction  # Oversold, allow long
    if prediction == "short" and bb_pct_b > 0.95:
        return prediction  # Overbought, allow short
    
    return "skip"