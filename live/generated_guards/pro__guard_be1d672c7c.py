def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    vwap_deviation = features.get("vwap_deviation", 0)
    rsi_14 = features.get("rsi_14", 50)
    
    if prediction == "long":
        # Bullish crossover from oversold with confirmation
        if not (stoch_k > stoch_d and stoch_d < 25 and bb_pct_b < 0.2 and vwap_deviation > -0.005):
            return "skip"
    elif prediction == "short":
        # Bearish crossover from overbought with confirmation
        if not (stoch_k < stoch_d and stoch_d > 75 and bb_pct_b > 0.8 and vwap_deviation < 0.005):
            return "skip"
    
    return prediction