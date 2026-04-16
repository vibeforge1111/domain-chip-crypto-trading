def guard(features: dict, prediction: str) -> str:
    """Skip trades when momentum is decelerating (negative macd histogram)."""
    # Detect momentum deceleration via macd histogram
    if features.get('macd_histogram', 0) < -0.0003:
        return "skip"
    # Additional confirmation: weak momentum + overbought in wider context
    if features.get('macd_histogram', 0) < 0 and features.get('rsi_2h', 50) > 68:
        return "skip"
    return prediction