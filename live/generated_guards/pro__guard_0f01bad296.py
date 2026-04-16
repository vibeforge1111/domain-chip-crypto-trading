def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    vwap_ok = (prediction == "long" and features["vwap_deviation"] > 0) or \
              (prediction == "short" and features["vwap_deviation"] < 0)
    
    stoch_ok = (prediction == "long" and features["stoch_k"] < 80) or \
               (prediction == "short" and features["stoch_k"] > 20)
    
    momentum_ok = (prediction == "long" and features["macd_histogram"] > 0 and features["obv_slope"] > 0) or \
                  (prediction == "short" and features["macd_histogram"] < 0 and features["obv_slope"] < 0)
    
    bb_ok = (prediction == "long" and features["bb_pct_b"] > 0.3) or \
            (prediction == "short" and features["bb_pct_b"] < 0.7)
    
    rsi_ok = (prediction == "long" and features["rsi_2h"] > 40) or \
             (prediction == "short" and features["rsi_2h"] < 60)
    
    confirm_count = sum([vwap_ok, stoch_ok, momentum_ok, bb_ok, rsi_ok])
    
    if confirm_count < 2:
        return "skip"
    
    return prediction