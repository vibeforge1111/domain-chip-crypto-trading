def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    # Multi-indicator confirmation: require 2+ signals to agree
    bullish = sum([
        features.get('vwap_deviation', 0) > 0.001,
        features.get('obv_slope', 0) > 0,
        features.get('macd_histogram', 0) > 0,
        features.get('bb_pct_b', 0.5) > 0.6
    ])
    bearish = sum([
        features.get('vwap_deviation', 0) < -0.001,
        features.get('obv_slope', 0) < 0,
        features.get('macd_histogram', 0) < 0,
        features.get('bb_pct_b', 0.5) < 0.4
    ])
    
    if prediction == "long" and bullish >= 2:
        return prediction
    elif prediction == "short" and bearish >= 2:
        return prediction
    
    return "skip"