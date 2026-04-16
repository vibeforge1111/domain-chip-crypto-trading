def guard(features: dict, prediction: str) -> str:
    # Detect compression: low ATR volatility AND low Bollinger width
    compressed = features['atr_ratio'] < 0.55 and features['bb_width'] < 0.3
    
    if compressed:
        # False compression flags
        extreme_bb = features['bb_pct_b'] < 0.15 or features['bb_pct_b'] > 0.85
        stoch_extreme = features['stoch_k'] > 85 or features['stoch_k'] < 15
        vwap_away = abs(features['vwap_deviation']) > 0.008
        rsi_div = features['rsi_2h'] > 70 if features['rsi_14'] < 30 else features['rsi_2h'] < 30
        
        if extreme_bb or stoch_extreme or vwap_away or rsi_div:
            return "skip"
    
    return prediction