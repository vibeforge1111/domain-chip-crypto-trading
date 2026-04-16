def guard(features: dict, prediction: str) -> str:
    # Detect compression: low atr_ratio and low bb_width
    is_compression = features.get('atr_ratio', 1) < 0.75 and features.get('bb_width', 1) < 0.15
    
    if is_compression and prediction != "skip":
        # False compression signals to skip
        extreme_stoch = features.get('stoch_k', 50) > 80 or features.get('stoch_k', 50) < 20
        poor_vwap = features.get('vwap_deviation', 0) < -0.01 or features.get('vwap_deviation', 0) > 0.01
        bearish_momentum = features.get('macd_histogram', 0) < 0 and features.get('obv_slope', 0) < 0
        
        if extreme_stoch and poor_vwap and bearish_momentum:
            return "skip"
    
    return prediction