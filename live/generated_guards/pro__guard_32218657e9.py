def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bb = features.get("bb_pct_b", 0.5)
    vwap = features.get("vwap_deviation", 0)
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    obv = features.get("obv_slope", 0)
    macd = features.get("macd_histogram", 0)
    rsi_2h = features.get("rsi_2h", 50)
    
    bullish_confirms = 0
    bearish_confirms = 0
    
    # BB confirmation
    if bb < 0.25:
        bullish_confirms += 1
    elif bb > 0.75:
        bearish_confirms += 1
    
    # VWAP confirmation
    if vwap < -0.005:
        bullish_confirms += 1
    elif vwap > 0.005:
        bearish_confirms += 1
    
    # Stochastic confirmation
    if stoch_k < 25 and stoch_d < 25:
        bullish_confirms += 1
    elif stoch_k > 75 and stoch_d > 75:
        bearish_confirms += 1
    
    # OBV confirmation
    if obv > 0:
        bullish_confirms += 1
    elif obv < 0:
        bearish_confirms += 1
    
    # MACD confirmation
    if macd > 0:
        bullish_confirms += 1
    elif macd < 0:
        bearish_confirms += 1
    
    # RSI 2h confirmation
    if rsi_2h < 35:
        bullish_confirms += 1
    elif rsi_2h > 65:
        bearish_confirms += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish_confirms < 2:
        return "skip"
    elif prediction == "short" and bearish_confirms < 2:
        return "skip"
    
    return prediction