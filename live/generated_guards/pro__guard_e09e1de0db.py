def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Count bullish and bearish confirmations
    bullish_count = 0
    bearish_count = 0
    
    # RSI not overbought/oversold
    if features.get('rsi_14', 50) < 70:
        bullish_count += 1
    if features.get('rsi_14', 50) > 30:
        bearish_count += 1
    
    # Stochastic K not overbought/oversold
    if features.get('stoch_k', 50) < 80:
        bullish_count += 1
    if features.get('stoch_k', 50) > 20:
        bearish_count += 1
    
    # BB position not at extremes
    if features.get('bb_pct_b', 0.5) < 0.8:
        bullish_count += 1
    if features.get('bb_pct_b', 0.5) > 0.2:
        bearish_count += 1
    
    # VWAP deviation aligned with direction
    if features.get('vwap_deviation', 0) < 0.01:
        bullish_count += 1
    if features.get('vwap_deviation', 0) > -0.01:
        bearish_count += 1
    
    # OBV slope direction
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    if features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # MACD histogram direction
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    if features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # RSI 2h not overbought/oversold
    if features.get('rsi_2h', 50) < 70:
        bullish_count += 1
    if features.get('rsi_2h', 50) > 30:
        bearish_count += 1
    
    # Require 2+ indicators to agree with prediction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"