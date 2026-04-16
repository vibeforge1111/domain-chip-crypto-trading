def guard(features: dict, prediction: str) -> str:
    # True compression: narrow bands + low volatility
    in_compression = features['bb_width'] < 0.25 and features['atr_ratio'] < 0.65
    
    # Price stretched from fair value (false move warning)
    stretched_from_vwap = abs(features['vwap_deviation']) > 0.008
    
    # Stochastic exhaustion at compression boundaries
    exhaustion = features['stoch_k'] > 82 or features['stoch_k'] < 18
    
    # Momentum divergence in compression
    momentum_diverging = features['macd_histogram'] * features['ema_slope'] < 0
    
    # Skip if compression + stretched + exhaustion or divergence (false breakout)
    if in_compression and stretched_from_vwap and (exhaustion or momentum_diverging):
        return "skip"
    
    return prediction