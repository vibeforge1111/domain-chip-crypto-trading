def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    if prediction == 'skip':
        return prediction
    
    # Long: price above VWAP should have positive momentum, short: opposite
    long_disagree = prediction == 'long' and vwap_dev < -0.01 and momentum < -0.05
    short_disagree = prediction == 'short' and vwap_dev > 0.01 and momentum > 0.05
    
    # Additional filter: RSI divergence from trade direction
    rsi_diverges = (prediction == 'long' and rsi_2h < 40) or (prediction == 'short' and rsi_2h > 60)
    
    if (long_disagree or short_disagree) and rsi_diverges:
        return 'skip'
    
    return prediction