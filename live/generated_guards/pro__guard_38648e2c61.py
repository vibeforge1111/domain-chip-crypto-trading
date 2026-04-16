def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    obv = features.get('obv_slope', 0)
    macd = features.get('macd_histogram', 0)
    stoch = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long setup: price below VWAP should have positive momentum signals
    if prediction == "long":
        if vwap_dev < -0.003 and obv < 0 and macd < 0:
            return "skip"
        if vwap_dev > 0.005 and rsi_2h > 70:
            return "skip"
    
    # Short setup: price above VWAP should have negative momentum signals
    if prediction == "short":
        if vwap_dev > 0.003 and obv > 0 and macd > 0:
            return "skip"
        if vwap_dev < -0.005 and rsi_2h < 30:
            return "skip"
    
    return prediction