def guard(features: dict, prediction: str) -> str:
    """Skip trades against volume flow direction (OBV slope)."""
    obv_slope = features.get("obv_slope", 0)
    macd_histogram = features.get("macd_histogram", 0)

    # Skip longs when OBV is declining (distribution) and MACD bearish
    if prediction == "long" and obv_slope < -0.5 and macd_histogram < 0:
        return "skip"

    # Skip shorts when OBV is rising (accumulation) and MACD bullish
    if prediction == "short" and obv_slope > 0.5 and macd_histogram > 0:
        return "skip"

    return prediction