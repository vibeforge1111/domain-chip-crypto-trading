def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to filter unreliable signals."""
    # True compression: low volatility + no directional setup
    is_squeeze = features['atr_ratio'] < 0.7 and features['bb_width'] < 0.15
    bb_mid = 0.3 < features['bb_pct_b'] < 0.7
    vwap_near = abs(features['vwap_deviation']) < 0.005
    stoch_neutral = 25 < features['stoch_k'] < 75 and 25 < features['stoch_d'] < 75
    weak_momentum = abs(features['macd_histogram']) < 0.0003
    obv_flat = abs(features['obv_slope']) < 0.01
    
    if is_squeeze and bb_mid and vwap_near and stoch_neutral and weak_momentum and obv_flat:
        return "skip"
    return prediction