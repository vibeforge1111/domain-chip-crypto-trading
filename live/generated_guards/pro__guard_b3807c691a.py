def guard(features: dict, prediction: str) -> str:
    """Custom guard function for trading signal filtering."""
    obv_slope = features.get('obv_slope', 0)
    rsi_2h = features.get('rsi_2h', 50)
    vwap_deviation = features.get('vwap_deviation', 0)

    # Skip longs if OBV is declining (distribution against us)
    if prediction == "long" and obv_slope < -0.1:
        return "skip"

    # Skip shorts if OBV is rising (accumulation against us)
    if prediction == "short" and obv_slope > 0.1:
        return "skip"

    # Avoid counter-trend trades using wider RSI context
    if prediction == "long" and rsi_2h < 35:
        return "skip"
    if prediction == "short" and rsi_2h > 65:
        return "skip"

    # Filter entries too far from fair value
    if prediction == "long" and vwap_deviation < -0.02:
        return "skip"
    if prediction == "short" and vwap_deviation > 0.02:
        return "skip"

    return prediction