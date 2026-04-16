def guard(features: dict, prediction: str) -> str:
    # Detect false compression breaks using multiple signals
    in_compression = features['bb_width'] < 0.18 and features['atr_ratio'] < 0.85
    
    if in_compression:
        # False break: price extended from VWAP but momentum diverges
        price_extended = abs(features['vwap_deviation']) > 0.008
        momentum_weak = features['macd_histogram'] < 0 and features['obv_slope'] < 0
        stoch_divergent = features['stoch_k'] < 25 or features['stoch_k'] > 75
        rsi_conflict = abs(features['rsi_14'] - features['rsi_2h']) > 15
        
        if price_extended and momentum_weak and stoch_divergent and rsi_conflict:
            return "skip"
    return prediction