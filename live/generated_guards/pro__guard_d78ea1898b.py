def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    score = 0
    
    # Stochastic confirmation (strong signal in extreme zones)
    if features["stoch_k"] < 20:
        score += 1
    elif features["stoch_k"] > 80:
        score -= 1
    
    # Bollinger Band position confirmation
    if features["bb_pct_b"] < 0.2:
        score += 1
    elif features["bb_pct_b"] > 0.8:
        score -= 1
    
    # VWAP deviation confirmation
    if features["vwap_deviation"] > 0.01:
        score += 1
    elif features["vwap_deviation"] < -0.01:
        score -= 1
    
    # MACD histogram momentum confirmation
    if features["macd_histogram"] > 0:
        score += 1
    elif features["macd_histogram"] < 0:
        score -= 1
    
    # OBV slope confirmation (accumulation/distribution)
    if features["obv_slope"] > 0:
        score += 1
    elif features["obv_slope"] < 0:
        score -= 1
    
    # RSI 2h context confirmation
    if features["rsi_2h"] < 40:
        score += 1
    elif features["rsi_2h"] > 60:
        score -= 1
    
    # Require 2+ signals to agree (|score| >= 2)
    if prediction == "long" and score < 2:
        return "skip"
    elif prediction == "short" and score > -2:
        return "skip"
    
    return prediction