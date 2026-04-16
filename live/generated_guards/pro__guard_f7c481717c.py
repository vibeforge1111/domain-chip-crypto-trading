def guard(features: dict, prediction: str) -> str:
    """Detect true vs false compression to filter bad breakouts."""
    # Compression: low volatility AND narrow bands
    is_compressed = features['bb_width'] < 0.5 and features['atr_ratio'] < 0.7
    
    # Extreme BB position signals potential false compression
    at_extreme = features['bb_pct_b'] < 0.15 or features['bb_pct_b'] > 0.85
    
    # Stochastic divergence during compression
    stoch_divergent = abs(features['stoch_k'] - features['stoch_d']) > 20
    
    # False compression: compressed but at extremes or divergent
    if is_compressed and (at_extreme or stoch_divergent):
        return "skip"
    
    return prediction