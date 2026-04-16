def guard(features: dict, prediction: str) -> str:
    # Detect compression: both ATR and BB width are low
    is_compressed = features.get('atr_ratio', 1) < 0.7 and features.get('bb_width', 0.5) < 0.25
    
    if is_compressed:
        # Check for false compression signals (momentum building despite low volatility)
        rsi_extreme = features.get('rsi_14', 50) > 70 or features.get('rsi_14', 50) < 30
        stoch_extreme = features.get('stoch_k', 50) > 80 or features.get('stoch_k', 50) < 20
        rsi_2h_extreme = features.get('rsi_2h', 50) > 68 or features.get('rsi_2h', 50) < 32
        vwap_dev = abs(features.get('vwap_deviation', 0)) > 0.008
        
        # False compression = compressed but with overextended indicators
        false_compression = (rsi_extreme and stoch_extreme) or rsi_2h_extreme or vwap_dev
        
        if false_compression:
            return "skip"
    
    return prediction