def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # VWAP confirmation
    vwap_dev = features.get('vwap_deviation', 0)
    if vwap_dev > 0:
        bullish_signals += 1
    elif vwap_dev < 0:
        bearish_signals += 1
    
    # Stochastic confirmation
    stoch_k = features.get('stoch_k', 50)
    if stoch_k < 30:
        bullish_signals += 1
    elif stoch_k > 70:
        bearish_signals += 1
    
    # Bollinger Band position confirmation
    bb_pos = features.get('bb_pct_b', 0.5)
    if bb_pos < 0.2:
        bullish_signals += 1
    elif bb_pos > 0.8:
        bearish_signals += 1
    
    # MACD histogram confirmation
    macd = features.get('macd_histogram', 0)
    if macd > 0:
        bullish_signals += 1
    elif macd < 0:
        bearish_signals += 1
    
    # Require 2+ confirming signals
    if prediction == "long" and bullish_signals < 2:
        return "skip"
    if prediction == "short" and bearish_signals < 2:
        return "skip"
    
    return prediction