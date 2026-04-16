def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # RSI confirmation (not overbought/oversold)
    if features.get('rsi_14', 50) < 70:
        bullish_count += 1
    if features.get('rsi_14', 50) > 30:
        bearish_count += 1
    
    # Stochastic confirmation
    if features.get('stoch_k', 50) < 80:
        bullish_count += 1
    if features.get('stoch_k', 50) > 20:
        bearish_count += 1
    
    # VWAP deviation confirmation
    if features.get('vwap_deviation', 0) > 0:
        bullish_count += 1
    if features.get('vwap_deviation', 0) < 0:
        bearish_count += 1
    
    # OBV slope confirmation (volume accumulation/distribution)
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    if features.get('obv_slope', 0) < 0:
        bearish_count += 1
    
    # MACD histogram confirmation
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    if features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    
    # Require 2+ signals aligned with direction
    if prediction == "long":
        return prediction if bullish_count >= 2 and bullish_count > bearish_count else "skip"
    if prediction == "short":
        return prediction if bearish_count >= 2 and bearish_count > bullish_count else "skip"
    
    return prediction