def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Multi-indicator confirmation (require 2+ signals matching direction)
    bullish = sum([
        features.get('rsi_14', 50) < 35,
        features.get('stoch_k', 50) < 25,
        features.get('bb_pct_b', 0.5) < 0.2,
        features.get('vwap_deviation', 0) < -0.005,
        features.get('macd_histogram', 0) > 0,
        features.get('rsi_2h', 50) < 45
    ])
    
    bearish = sum([
        features.get('rsi_14', 50) > 65,
        features.get('stoch_k', 50) > 75,
        features.get('bb_pct_b', 0.5) > 0.8,
        features.get('vwap_deviation', 0) > 0.005,
        features.get('macd_histogram', 0) < 0,
        features.get('rsi_2h', 50) > 55
    ])
    
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction