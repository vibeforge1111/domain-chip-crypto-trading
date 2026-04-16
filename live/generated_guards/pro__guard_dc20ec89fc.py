def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish = 0
    bearish = 0
    
    # Stochastic momentum
    if features.get("stoch_k", 50) < 20:
        bullish += 1
    elif features.get("stoch_k", 50) > 80:
        bearish += 1
    
    # VWAP deviation
    if features.get("vwap_deviation", 0) > 0.005:
        bullish += 1
    elif features.get("vwap_deviation", 0) < -0.005:
        bearish += 1
    
    # BB position extremes
    if features.get("bb_pct_b", 0.5) < 0.25:
        bullish += 1
    elif features.get("bb_pct_b", 0.5) > 0.75:
        bearish += 1
    
    # RSI 2h confirmation
    if features.get("rsi_2h", 50) < 40:
        bullish += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish += 1
    
    # MACD histogram direction
    if features.get("macd_histogram", 0) > 0:
        bullish += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish += 1
    
    # Require 2+ signals aligned with direction
    if prediction == "long" and bullish < 2:
        return "skip"
    if prediction == "short" and bearish < 2:
        return "skip"
    
    return prediction