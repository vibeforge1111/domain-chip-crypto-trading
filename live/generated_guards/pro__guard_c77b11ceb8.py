def guard(features: dict, prediction: str) -> str:
    # True compression: tight BB + low ATR
    is_compressed = features.get('bb_width', 1) < 0.18 and features.get('atr_ratio', 1) < 0.75
    
    if is_compressed and prediction != 'skip':
        # False compression signals
        stoch_extreme = features.get('stoch_k', 50) > 78 or features.get('stoch_k', 50) < 22
        vwap_far = abs(features.get('vwap_deviation', 0)) > 0.008
        rsi_div = abs(features.get('rsi_14', 50) - features.get('rsi_2h', 50)) > 12
        
        if stoch_extreme and (vwap_far or rsi_div):
            return "skip"
    
    return prediction