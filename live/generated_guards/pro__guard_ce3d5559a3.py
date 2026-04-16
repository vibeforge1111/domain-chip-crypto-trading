def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    confirmations = 0
    
    # Stochastic momentum (K > D = bullish)
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        confirmations += 1
    else:
        confirmations -= 1
    
    # RSI confirmation
    if features.get('rsi_14', 50) > 55:
        confirmations += 1
    elif features.get('rsi_14', 50) < 45:
        confirmations -= 1
    
    # VWAP deviation
    if features.get('vwap_deviation', 0) > 0:
        confirmations += 1
    elif features.get('vwap_deviation', 0) < 0:
        confirmations -= 1
    
    # MACD histogram
    if features.get('macd_histogram', 0) > 0:
        confirmations += 1
    elif features.get('macd_histogram', 0) < 0:
        confirmations -= 1
    
    # BB position
    if features.get('bb_pct_b', 0.5) > 0.6:
        confirmations += 1
    elif features.get('bb_pct_b', 0.5) < 0.4:
        confirmations -= 1
    
    # Require 2+ signals to agree with direction
    if prediction == "long" and confirmations < 2:
        return "skip"
    if prediction == "short" and confirmations > -2:
        return "skip"
    
    return prediction