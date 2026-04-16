def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    agreements = 0
    
    # RSI 2h directional alignment
    if prediction == "long" and features["rsi_2h"] < 50:
        agreements += 1
    elif prediction == "short" and features["rsi_2h"] > 50:
        agreements += 1
    
    # Stochastic K/D crossover + not extreme
    if prediction == "long" and features["stoch_k"] > features["stoch_d"] and features["stoch_k"] < 80:
        agreements += 1
    elif prediction == "short" and features["stoch_k"] < features["stoch_d"] and features["stoch_k"] > 20:
        agreements += 1
    
    # VWAP deviation confirmation
    if prediction == "long" and features["vwap_deviation"] > 0:
        agreements += 1
    elif prediction == "short" and features["vwap_deviation"] < 0:
        agreements += 1
    
    # BB position confirmation (not at extremes)
    if prediction == "long" and 0.15 < features["bb_pct_b"] < 0.85:
        agreements += 1
    elif prediction == "short" and 0.15 < features["bb_pct_b"] < 0.85:
        agreements += 1
    
    return prediction if agreements >= 2 else "skip"