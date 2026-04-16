def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    if prediction == "long":
        bullish_signals = sum([
            features.get('rsi_14', 50) < 70,
            features.get('stoch_k', 50) < 80,
            features.get('vwap_deviation', 0) > 0,
            features.get('obv_slope', 0) > 0,
            features.get('macd_histogram', 0) > 0,
        ])
        return prediction if bullish_signals >= 2 else "skip"
    
    if prediction == "short":
        bearish_signals = sum([
            features.get('rsi_14', 50) > 30,
            features.get('stoch_k', 50) > 20,
            features.get('vwap_deviation', 0) < 0,
            features.get('obv_slope', 0) < 0,
            features.get('macd_histogram', 0) < 0,
        ])
        return prediction if bearish_signals >= 2 else "skip"
    
    return prediction