def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Count bullish signals for long
    bullish_count = 0
    if features.get('rsi_14', 50) < 70:
        bullish_count += 1
    if features.get('stoch_k', 50) < 80:
        bullish_count += 1
    if features.get('macd_histogram', 0) > 0:
        bullish_count += 1
    if features.get('obv_slope', 0) > 0:
        bullish_count += 1
    if features.get('bb_pct_b', 0.5) > 0.5:
        bullish_count += 1
    if features.get('rsi_2h', 50) < 70:
        bullish_count += 1
    
    # Count bearish signals for short
    bearish_count = 0
    if features.get('rsi_14', 50) > 30:
        bearish_count += 1
    if features.get('stoch_k', 50) > 20:
        bearish_count += 1
    if features.get('macd_histogram', 0) < 0:
        bearish_count += 1
    if features.get('obv_slope', 0) < 0:
        bearish_count += 1
    if features.get('bb_pct_b', 0.5) < 0.5:
        bearish_count += 1
    if features.get('rsi_2h', 50) > 30:
        bearish_count += 1
    
    # Require 2+ signals to agree with prediction direction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    if prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"