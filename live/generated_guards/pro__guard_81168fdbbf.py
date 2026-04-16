def guard(features: dict, prediction: str) -> str:
    """Filter trades when MACD histogram shows momentum deceleration."""
    macd_hist = features.get("macd_histogram", 0)
    vwap_dev = features.get("vwap_deviation", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    # Skip longs when MACD histogram is negative (momentum turning bearish)
    if prediction == "long" and macd_hist < 0:
        return "skip"
    
    # Skip shorts when MACD histogram is positive (momentum turning bullish)
    if prediction == "short" and macd_hist > 0:
        return "skip"
    
    # Additional filter: skip longs if RSI_2h > 70 (overextended in wider context)
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    
    # Skip longs when price is far below VWAP (weakness confirmed by macd negativity)
    if prediction == "long" and vwap_dev < -0.02:
        return "skip"
    
    return prediction