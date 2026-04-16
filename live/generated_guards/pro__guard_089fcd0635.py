def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return "skip"
    
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation (oversold = bullish, overbought = bearish)
    rsi = features.get("rsi_14", 50)
    if rsi < 35:
        bullish_count += 1
    elif rsi > 65:
        bearish_count += 1
    
    # Stochastic confirmation
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    if stoch_k < 20 and stoch_d < 20:
        bullish_count += 1
    elif stoch_k > 80 and stoch_d > 80:
        bearish_count += 1
    
    # VWAP deviation (above = bullish, below = bearish)
    vwap_dev = features.get("vwap_deviation", 0)
    if vwap_dev > 0.003:
        bullish_count += 1
    elif vwap_dev < -0.003:
        bearish_count += 1
    
    # OBV slope (positive = accumulation, negative = distribution)
    obv = features.get("obv_slope", 0)
    if obv > 0:
        bullish_count += 1
    elif obv < 0:
        bearish_count += 1
    
    # MACD histogram (positive = bullish, negative = bearish)
    macd = features.get("macd_histogram", 0)
    if macd > 0:
        bullish_count += 1
    elif macd < 0:
        bearish_count += 1
    
    # Bollinger Bands position (lower band = bullish, upper = bearish)
    bb_pos = features.get("bb_pct_b", 0.5)
    if bb_pos < 0.2:
        bullish_count += 1
    elif bb_pos > 0.8:
        bearish_count += 1
    
    # RSI 2h wider context
    rsi_2h = features.get("rsi_2h", 50)
    if rsi_2h < 40:
        bullish_count += 1
    elif rsi_2h > 60:
        bearish_count += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish_count >= 2:
        return "long"
    elif prediction == "short" and bearish_count >= 2:
        return "short"
    
    return "skip"