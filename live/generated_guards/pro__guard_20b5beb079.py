def guard(features: dict, prediction: str) -> str:
    # True compression: low bb_width + low atr_ratio indicates squeeze
    # False compression: compressed but without momentum confirmation
    is_compressed = features['bb_width'] < 0.03 and features['atr_ratio'] < 0.7
    
    if is_compressed and prediction != "skip":
        # Check momentum divergence for compression signals
        weak_momentum = features['macd_histogram'] < 0.0004
        stoch_weak = features['stoch_k'] < 35 and features['stoch_d'] < 40
        # False compression: compressed with weak momentum and OBV not confirming
        if weak_momentum and stoch_weak and features['obv_slope'] < 0:
            return "skip"
    return prediction