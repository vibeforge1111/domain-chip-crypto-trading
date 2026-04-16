def guard(features: dict, prediction: str) -> str:
    """Custom guard function using BB extremes as high-confidence entry zones."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    vwap_deviation = features.get('vwap_deviation', 0)
    
    # Only allow trades at extreme BB positions (<0.05 or >0.95)
    if bb_pct_b >= 0.05 and bb_pct_b <= 0.95:
        return "skip"
    
    # For long signals at lower band, price should be below VWAP
    if prediction == "long" and bb_pct_b < 0.05 and vwap_deviation >= 0:
        return "skip"
    
    # For short signals at upper band, price should be above VWAP
    if prediction == "short" and bb_pct_b > 0.95 and vwap_deviation <= 0:
        return "skip"
    
    return prediction