def guard(features: dict, prediction: str) -> str:
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Detect disagreement between momentum and VWAP position
    disagreement = (momentum > 0.3 and vwap_dev < -0.005) or (momentum < -0.3 and vwap_dev > 0.005)
    
    if disagreement:
        return "skip"
    
    # Additional filter: avoid longs when 2h RSI is overbought, shorts when oversold
    if prediction == "long" and rsi_2h > 70:
        return "skip"
    if prediction == "short" and rsi_2h < 30:
        return "skip"
    
    return prediction