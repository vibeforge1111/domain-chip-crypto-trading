def guard(features: dict, prediction: str) -> str:
    # False compression: BB squeezing while ATR expanding signals imminent trap
    if features['bb_width'] < 0.025 and features['atr_ratio'] > 1.4:
        return "skip"
    return prediction