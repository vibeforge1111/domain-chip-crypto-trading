def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bull_count = 0
    bear_count = 0
    
    # Bullish confirmations
    if 0.2 < features.get('bb_pct_b', 0.5) < 0.8:
        bull_count += 1
    if features.get('vwap_deviation', 0) > 0:
        bull_count += 1
    if features.get('stoch_k', 50) > features.get('stoch_d', 50):
        bull_count += 1
    if features.get('obv_slope', 0) > 0:
        bull_count += 1
    if features.get('macd_histogram', 0) > 0:
        bull_count += 1
    if features.get('rsi_2h', 50) > 55:
        bull_count += 1
    
    # Bearish confirmations
    if 0.2 < features.get('bb_pct_b', 0.5) < 0.8:
        bear_count += 1
    if features.get('vwap_deviation', 0) < 0:
        bear_count += 1
    if features.get('stoch_k', 50) < features.get('stoch_d', 50):
        bear_count += 1
    if features.get('obv_slope', 0) < 0:
        bear_count += 1
    if features.get('macd_histogram', 0) < 0:
        bear_count += 1
    if features.get('rsi_2h', 50) < 45:
        bear_count += 1
    
    if prediction == "long" and bull_count >= 2:
        return prediction
    if prediction == "short" and bear_count >= 2:
        return prediction
    
    return "skip"