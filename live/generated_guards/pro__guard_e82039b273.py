def guard(features: dict, prediction: str) -> str:
    bullish_signals = sum([
        features['rsi_14'] > 55,
        features['rsi_2h'] > 55,
        features['stoch_k'] > 60,
        features['vwap_deviation'] > 0,
        features['macd_histogram'] > 0,
        features['obv_slope'] > 0,
        features['bb_pct_b'] > 0.5
    ])
    bearish_signals = sum([
        features['rsi_14'] < 45,
        features['rsi_2h'] < 45,
        features['stoch_k'] < 40,
        features['vwap_deviation'] < 0,
        features['macd_histogram'] < 0,
        features['obv_slope'] < 0,
        features['bb_pct_b'] < 0.5
    ])
    if prediction == "long" and bearish_signals >= 2:
        return "skip"
    if prediction == "short" and bullish_signals >= 2:
        return "skip"
    return prediction