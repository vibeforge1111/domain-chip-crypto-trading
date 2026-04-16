def guard(features: dict, prediction: str) -> str:
    # Skip if compression + extreme stochastic (false breakout setup)
    if features['bb_width'] < 0.025 and features['atr_ratio'] < 0.75:
        if features['stoch_k'] > 80 or features['stoch_k'] < 20:
            return "skip"
    
    # Skip if extended from VWAP in direction of prediction
    if abs(features['vwap_deviation']) > 0.012:
        return "skip"
    
    # Skip if momentum diverges from Bollinger position
    if features['bb_pct_b'] > 0.8 and features['macd_histogram'] < -0.0001:
        return "skip"
    if features['bb_pct_b'] < 0.2 and features['macd_histogram'] > 0.0001:
        return "skip"
    
    return prediction