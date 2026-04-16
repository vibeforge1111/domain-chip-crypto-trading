def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Skip longs: positive momentum but price too far below VWAP (momentum-price disagreement)
    if prediction == 'long' and momentum > 0.2 and vwap_dev < -0.015:
        return 'skip'
    
    # Skip longs: positive momentum but both stochastics deeply oversold (weak confirmation)
    if prediction == 'long' and momentum > 0.2 and stoch_k < 20 and stoch_d < 20:
        return 'skip'
    
    # Skip shorts: negative momentum but price too far above VWAP (momentum-price disagreement)
    if prediction == 'short' and momentum < -0.2 and vwap_dev > 0.015:
        return 'skip'
    
    # Skip shorts: negative momentum but both stochastics deeply overbought (weak confirmation)
    if prediction == 'short' and momentum < -0.2 and stoch_k > 80 and stoch_d > 80:
        return 'skip'
    
    return prediction