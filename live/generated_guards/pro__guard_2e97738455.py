def guard(features: dict, prediction: str) -> str:
    # Detect false compression: low bb_width + low atr_ratio + misaligned momentum
    is_compression = features['bb_width'] < 0.02 and features['atr_ratio'] < 0.8
    if is_compression:
        if prediction == 'long' and features['macd_histogram'] < -0.0001:
            return 'skip'
        if prediction == 'short' and features['macd_histogram'] > 0.0001:
            return 'skip'
    return prediction