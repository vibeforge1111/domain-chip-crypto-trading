def guard(features: dict, prediction: str) -> str:
    """Momentum deceleration guard using MACD histogram and new features."""
    macd = features.get("macd_histogram", 0)
    vwap = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    stoch_k = features.get("stoch_k", 50)
    bb_pct = features.get("bb_pct_b", 0.5)
    
    # For longs: require positive momentum, price above VWAP, not overbought in wider context
    if prediction == "long":
        if macd < 0:
            return "skip"
        if vwap < -0.003:
            return "skip"
        if rsi_2h > 72 and stoch_k > 80:
            return "skip"
        if bb_pct > 0.92:
            return "skip"
    
    # For shorts: require negative momentum, price below VWAP, not oversold in wider context
    if prediction == "short":
        if macd > 0:
            return "skip"
        if vwap > 0.003:
            return "skip"
        if rsi_2h < 28 and stoch_k < 20:
            return "skip"
        if bb_pct < 0.08:
            return "skip"
    
    return prediction