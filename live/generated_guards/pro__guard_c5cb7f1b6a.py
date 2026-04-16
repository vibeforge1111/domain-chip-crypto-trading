def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP-momentum disagreement and weak 2h RSI alignment."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Strong disagreement: price far from VWAP but momentum contradicts
    if vwap_dev < -0.02 and momentum > 0.6:
        # Price below VWAP but momentum positive - weak for long
        if prediction == "long" and rsi_2h < 45:
            return "skip"
    if vwap_dev > 0.02 and momentum < -0.6:
        # Price above VWAP but momentum negative - weak for short
        if prediction == "short" and rsi_2h > 55:
            return "skip"
    
    return prediction