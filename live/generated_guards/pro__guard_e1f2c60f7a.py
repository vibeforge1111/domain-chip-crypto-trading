def guard(features: dict, prediction: str) -> str:
    # Detect false compression: tight bands + low ATR + extreme stoch + large VWAP deviation
    if features['bb_width'] < 0.18 and features['atr_ratio'] < 0.75:
        if (features['stoch_k'] > 80 or features['stoch_k'] < 20) and abs(features['vwap_deviation']) > 0.015:
            return "skip"
    return prediction