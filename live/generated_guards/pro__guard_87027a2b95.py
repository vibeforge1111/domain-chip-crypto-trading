def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    agree = 0
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    sk = features.get("stoch_k", 50)
    sd = features.get("stoch_d", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if bb < 0.4: agree += 1
        if vwap > 0: agree += 1
        if sk < 25 and sd < 25: agree += 1
        if obv > 0: agree += 1
        if macd > 0: agree += 1
        if rsi2h < 50: agree += 1
    else:
        if bb > 0.6: agree += 1
        if vwap < 0: agree += 1
        if sk > 75 and sd > 75: agree += 1
        if obv < 0: agree += 1
        if macd < 0: agree += 1
        if rsi2h > 50: agree += 1
    
    return prediction if agree >= 2 else "skip"