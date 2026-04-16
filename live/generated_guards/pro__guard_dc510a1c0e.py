def guard(features: dict, prediction: str) -> str:
    # False compression: low volatility but wide bands = likely failed squeeze
    if features['atr_ratio'] < 0.75 and features['bb_width'] > 0.6:
        return "skip"
    return prediction