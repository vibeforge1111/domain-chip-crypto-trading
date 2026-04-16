def guard(features: dict, prediction: str) -> str:
    """Filter trades using stochastic crossover timing with confirmation."""
    if prediction == "skip":
        return prediction

    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    vwap_dev = features.get("vwap_deviation", 0)
    obv_slope = features.get("obv_slope", 0)
    rsi_2h = features.get("rsi_2h", 50)

    if prediction == "long":
        # Stochastic bullish alignment: K above D
        if stoch_k <= stoch_d:
            return "skip"
        # Require price above VWAP for longs
        if vwap_dev < 0:
            return "skip"
        # Reject if 2h RSI is overbought
        if rsi_2h > 70:
            return "skip"
    elif prediction == "short":
        # Stochastic bearish alignment: K below D
        if stoch_k >= stoch_d:
            return "skip"
        # Require price below VWAP for shorts
        if vwap_dev > 0:
            return "skip"
        # Reject if 2h RSI is oversold
        if rsi_2h < 30:
            return "skip"

    # Volume confirmation via OBV slope
    if obv_slope < 0 and prediction == "long":
        return "skip"
    if obv_slope > 0 and prediction == "short":
        return "skip"

    return prediction