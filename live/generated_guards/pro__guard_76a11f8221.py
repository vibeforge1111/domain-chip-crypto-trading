def guard(features: dict, prediction: str) -> str:
    """Custom guard function using Bollinger Band extremes as high-confidence entry zones.

    Args:
        features: Dict with market features including bb_pct_b, stoch_k, stoch_d, rsi_2h
        prediction: Current prediction ("long", "short", or "skip")

    Returns:
        "skip" to reject this trade, or the original prediction to keep it.
    """
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    # High-confidence entry: extreme bb_pct_b (<0.05 lower, >0.95 upper)
    if bb_pct_b < 0.05:
        # Lower band extreme: expect bounce up
        if prediction == "long" and stoch_k < 20:
            return prediction
        return "skip"
    elif bb_pct_b > 0.95:
        # Upper band extreme: expect pullback down
        if prediction == "short" and stoch_k > 80:
            return prediction
        return "skip"
    
    return "skip"