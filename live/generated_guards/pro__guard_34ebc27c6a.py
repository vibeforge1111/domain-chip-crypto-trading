def guard(features: dict, prediction: str) -> str:
    """Reject trades when volatility compression lacks directional setup."""
    # True compression: low bb_width AND low atr_ratio
    is_compressed = features['bb_width'] < 0.12 and features['atr_ratio'] < 0.65
    
    # Stochastic extreme = exhausted momentum (false compression signal)
    stoch_extreme = features['stoch_k'] > 85 or features['stoch_k'] < 15
    
    # Price too far from VWAP = no clear reference point
    far_from_vwap = abs(features['vwap_deviation']) > 0.015
    
    if is_compressed and (stoch_extreme or far_from_vwap):
        return "skip"
    
    return prediction