def guard(features: dict, prediction: str) -> str:
    # True compression detection: both ATR and BB compressed
    is_compressed = features['atr_ratio'] < 0.8 and features['bb_width'] < 0.9
    
    # False compression indicator: compressed but no directional confirmation
    has_neutral_momentum = abs(features['momentum_score']) < 0.15
    has_neutral_stoch = 40 < features['stoch_k'] < 60 and 40 < features['stoch_d'] < 60
    has_low_vwap_dev = abs(features['vwap_deviation']) < 0.005
    
    if is_compressed and has_neutral_momentum and has_neutral_stoch and has_low_vwap_dev:
        return "skip"
    
    return prediction