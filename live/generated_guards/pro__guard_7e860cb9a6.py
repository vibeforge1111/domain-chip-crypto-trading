def guard(features: dict, prediction: str) -> str:
    """Filter signals using ATR vs BB compression and momentum divergence."""
    # False compression: tight bands but high volatility (potential false breakout)
    if features['bb_width'] < 0.15 and features['atr_ratio'] > 1.5:
        return "skip"
    
    # Extreme BB position without momentum confirmation
    if (features['bb_pct_b'] > 0.92 or features['bb_pct_b'] < 0.08):
        if features['macd_histogram'] * (1 if prediction == "long" else -1) < 0:
            return "skip"
    
    # Stochastic overbought/oversold with diverging OBV slope
    if features['stoch_k'] > 85 and features['obv_slope'] < 0:
        return "skip"
    if features['stoch_k'] < 15 and features['obv_slope'] > 0:
        return "skip"
    
    return prediction