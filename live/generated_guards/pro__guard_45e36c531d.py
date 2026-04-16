def guard(features: dict, prediction: str) -> str:
    """Filter trades based on overbought/oversold extremes using BB and Stoch."""
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Long: reject if overbought (Stoch >80) and BB at upper band (>0.85)
    if prediction == "long" and stoch_k > 80 and bb_pct_b > 0.85:
        return "skip"
    
    # Short: reject if oversold (Stoch <20) and BB at lower band (<0.15)
    if prediction == "short" and stoch_k < 20 and bb_pct_b < 0.15:
        return "skip"
    
    # Additional: reject if Stoch is diverging downward from overbought
    if prediction == "long" and stoch_k > 70 and stoch_d > 70 and stoch_k < stoch_d:
        return "skip"
    
    return prediction