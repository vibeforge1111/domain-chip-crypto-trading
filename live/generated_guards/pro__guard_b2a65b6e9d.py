def guard(features: dict, prediction: str) -> str:
    """Detect momentum deceleration via MACD histogram with confirmations."""
    macd_histogram = features.get('macd_histogram', 0)
    
    # Momentum deceleration: histogram near zero indicates weakening momentum
    # Positive hist near 0 = losing bullish momentum
    # Negative hist near 0 = losing bearish momentum
    momentum_weak = abs(macd_histogram) < 0.00015
    
    # Additional confirmations
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    
    # Reject longs when momentum weakens at upper BB with overbought stochastic
    if prediction == "long" and momentum_weak and bb_pct_b > 0.75 and stoch_k > 75:
        return "skip"
    
    # Reject shorts when momentum weakens at lower BB with oversold stochastic
    if prediction == "short" and momentum_weak and bb_pct_b < 0.25 and stoch_k < 25:
        return "skip"
    
    return prediction