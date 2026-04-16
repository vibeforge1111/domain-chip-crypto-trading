def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    sk = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi2h = features.get("rsi_2h", 50)
    
    # Count bullish indicators for long
    long_confirm = int(vwap > 0) + int(bb > 0.6) + int(obv > 0) + int(macd > 0) + int(rsi2h > 55)
    # Count bearish indicators for short
    short_confirm = int(vwap < 0) + int(bb < 0.4) + int(obv < 0) + int(macd < 0) + int(rsi2h < 45)
    
    if prediction == "long" and long_confirm < 2:
        return "skip"
    if prediction == "short" and short_confirm < 2:
        return "skip"
    return prediction