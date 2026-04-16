def guard(features: dict, prediction: str) -> str:
    # Skip when RSI extreme AND wick confirms reversal pressure
    if features['rsi_14'] > 70 and features['upper_wick_ratio'] > 0.3:
        return "skip"
    if features['rsi_14'] < 30 and features['lower_wick_ratio'] > 0.3:
        return "skip"
    return prediction