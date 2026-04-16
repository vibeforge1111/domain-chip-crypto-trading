def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Long with bearish vwap/momentum disagreement
    if prediction == "long" and vwap_dev < -0.01 and momentum < -0.3:
        return "skip"
    
    # Short with bullish vwap/momentum disagreement
    if prediction == "short" and vwap_dev > 0.01 and momentum > 0.3:
        return "skip"
    
    # Momentum trap: strong momentum but extreme Bollinger position
    if prediction == "long" and momentum > 0.5 and bb_pct_b > 0.85:
        return "skip"
    
    if prediction == "short" and momentum < -0.5 and bb_pct_b < 0.15:
        return "skip"
    
    # Stoch/Bollinger disagreement (overbought at lower band or vice versa)
    if prediction == "long" and stoch_k > 70 and bb_pct_b < 0.3:
        return "skip"
    
    if prediction == "short" and stoch_k < 30 and bb_pct_b > 0.7:
        return "skip"
    
    return prediction