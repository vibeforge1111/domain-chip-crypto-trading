def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi = features.get('rsi_14', 50)
    stoch_k = features.get('stoch_k', 50)
    obv_slope = features.get('obv_slope', 0)
    macd_hist = features.get('macd_histogram', 0)
    
    # Price above VWAP but momentum and trend indicators bearish (disagreement)
    if vwap_dev > 0.01:
        bearish_momentum = momentum < 0 and rsi < 45 and stoch_k < 40
        bearish_volume = obv_slope < 0 and macd_hist < 0
        if bearish_momentum and bearish_volume:
            return "skip"
    
    # Price below VWAP but momentum and trend indicators bullish (disagreement)
    if vwap_dev < -0.01:
        bullish_momentum = momentum > 0 and rsi > 55 and stoch_k > 60
        bullish_volume = obv_slope > 0 and macd_hist > 0
        if bullish_momentum and bullish_volume:
            return "skip"
    
    return prediction