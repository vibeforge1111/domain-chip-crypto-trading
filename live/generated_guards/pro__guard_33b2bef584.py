def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    agree = 0
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch = features.get("stoch_k", 50)
    obv = features.get("obv_slope", 0)
    rsi2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        if bb < 0.4: agree += 1
        if vwap > 0: agree += 1
        if stoch < 60: agree += 1
        if obv > 0: agree += 1
        if 30 < rsi2h < 70: agree += 1
    else:
        if bb > 0.6: agree += 1
        if vwap < 0: agree += 1
        if stoch > 40: agree += 1
        if obv < 0: agree += 1
        if 30 < rsi2h < 70: agree += 1
    
    return "skip" if agree < 2 else prediction