def guard(features: dict, prediction: str) -> str:
    # False compression: tight BB + low ATR without momentum confirmation
    if features['bb_width'] < 0.02 and features['atr_ratio'] < 0.8:
        # Momentum divergence check via OBV
        if features['obv_slope'] < 0 and prediction == 'long':
            return 'skip'
        if features['obv_slope'] > 0 and prediction == 'short':
            return 'skip'
    return prediction