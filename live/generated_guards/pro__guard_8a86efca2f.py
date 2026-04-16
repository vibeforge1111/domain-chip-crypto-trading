def guard(features: dict, prediction: str) -> str:
    """Filter trades using Bollinger Band extreme positions with confirmations."""
    bb_pct_b = features.get("bb_pct_b", 0.5)
    stoch_k = features.get("stoch_k", 50)
    rsi_2h = features.get("rsi_2h", 50)
    vwap_deviation = features.get("vwap_deviation", 0)

    # Longs need bb_pct_b at extreme bottom
    if prediction == "long" and bb_pct_b > 0.05:
        return "skip"

    # Shorts need bb_pct_b at extreme top
    if prediction == "short" and bb_pct_b < 0.95:
        return "skip"

    # Avoid double-oversold traps on longs
    if prediction == "long" and stoch_k < 15 and rsi_2h < 35:
        return "skip"

    return prediction