def guard(features: dict, prediction: str) -> str:
    """Filter trades when price is too close to fair value (VWAP)."""
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    # Skip if price is within 0.5% of VWAP and wider timeframe RSI is neutral
    if abs(vwap_dev) < 0.005 and 40 <= rsi_2h <= 60:
        return "skip"
    return prediction