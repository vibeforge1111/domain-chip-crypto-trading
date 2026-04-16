def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_signals = 0
    bearish_signals = 0
    
    # Stochastic confirmation (not extreme)
    if features.get('stoch_k', 50) < 80 and features.get('stoch_d', 50) < 80:
        bullish_signals += 1
    if features.get('stoch_k', 50) > 20 and features.get('stoch_d', 50) > 20:
        bearish_signals += 1
    
    # Bollinger Band position
    if features.get('bb_pct_b', 0.5) > 0.5:
        bullish_signals += 1
    if features.get('bb_pct_b', 0.5) < 0.5:
        bearish_signals += 1
    
    # VWAP deviation (positive = bullish)
    if features.get('vwap_deviation', 0) >= 0:
        bullish_signals += 1
    if features.get('vwap_deviation', 0) <= 0:
        bearish_signals += 1
    
    # MACD histogram direction
    if features.get('macd_histogram', 0) > 0:
        bullish_signals += 1
    if features.get('macd_histogram', 0) < 0:
        bearish_signals += 1
    
    # OBV slope confirmation
    if features.get('obv_slope', 0) > 0:
        bullish_signals += 1
    if features.get('obv_slope', 0) < 0:
        bearish_signals += 1
    
    # RSI 2h confirmation (not extreme)
    if features.get('rsi_2h', 50) < 70:
        bullish_signals += 1
    if features.get('rsi_2h', 50) > 30:
        bearish_signals += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish_signals >= 2:
        return prediction
    if prediction == "short" and bearish_signals >= 2:
        return prediction
    
    return "skip"