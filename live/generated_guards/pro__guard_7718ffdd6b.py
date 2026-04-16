def guard(features: dict, prediction: str) -> str:
    """Skip trades when MACD histogram shows momentum deceleration without volume confirmation."""
    macd_hist = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    if macd_hist < -0.0003 and obv_slope <= 0:
        return "skip"
    return prediction