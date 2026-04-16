def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    long_confirms = 0
    short_confirms = 0
    
    # RSI confirmation (oversold for long, overbought for short)
    if features.get('rsi_14', 50) < 35:
        long_confirms += 1
    if features.get('rsi_14', 50) > 65:
        short_confirms += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 25:
        long_confirms += 1
    if features.get('stoch_k', 50) > 75:
        short_confirms += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) > 0:
        long_confirms += 1
    if features.get('vwap_deviation', 0) < 0:
        short_confirms += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        long_confirms += 1
    if features.get('macd_histogram', 0) < 0:
        short_confirms += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        long_confirms += 1
    if features.get('obv_slope', 0) < 0:
        short_confirms += 1
    
    # Require 2+ indicators to agree with prediction direction
    if prediction == "long" and long_confirms >= 2:
        return prediction
    if prediction == "short" and short_confirms >= 2:
        return prediction
    
    return "skip"