def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # RSI confirmation (not overbought/oversold)
    rsi = features.get('rsi_14', 50)
    if rsi < 70:
        bullish += 1
    if rsi > 30:
        bearish += 1
    
    # Stochastic confirmation
    sk = features.get('stoch_k', 50)
    sd = features.get('stoch_d', 50)
    if sk < 75 and sd < 75:
        bullish += 1
    if sk > 25 and sd > 25:
        bearish += 1
    
    # VWAP deviation confirmation
    vwap_dev = features.get('vwap_deviation', 0)
    if vwap_dev > 0:
        bullish += 1
    if vwap_dev < 0:
        bearish += 1
    
    # MACD histogram confirmation
    macd = features.get('macd_histogram', 0)
    if macd > 0:
        bullish += 1
    if macd < 0:
        bearish += 1
    
    # OBV slope confirmation
    obv = features.get('obv_slope', 0)
    if obv > 0:
        bullish += 1
    if obv < 0:
        bearish += 1
    
    # Require 2+ signals to agree with prediction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction