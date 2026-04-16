def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long: skip if price below VWAP AND bearish momentum
    if prediction == 'long':
        if vwap_dev < -0.005 and momentum < 0:
            return 'skip'
    
    # Short: skip if price above VWAP AND bullish momentum
    if prediction == 'short':
        if vwap_dev > 0.005 and momentum > 0:
            return 'skip'
    
    # Additional: avoid longs in overbought 2h regime
    if prediction == 'long' and stoch_k > 80 and rsi_2h > 70:
        return 'skip'
    
    # Additional: avoid shorts in oversold 2h regime
    if prediction == 'short' and stoch_k < 20 and rsi_2h < 30:
        return 'skip'
    
    return prediction