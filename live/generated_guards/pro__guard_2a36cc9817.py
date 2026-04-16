def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes as high-confidence entry zones."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    
    # Only allow trades at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b < 0.05:
        return prediction if prediction == "long" else "skip"
    if bb_pct_b > 0.95:
        return prediction if prediction == "short" else "skip"
    
    return "skip"