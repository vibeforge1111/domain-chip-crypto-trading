def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # BB position: above 0.6 = bullish, below 0.4 = bearish
    if features.get("bb_pct_b", 0.5) > 0.6:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) < 0.4:
        bearish_count += 1
    
    # VWAP: price above = bullish, below = bearish
    if features.get("vwap_deviation", 0) > 0.001:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.001:
        bearish_count += 1
    
    # Stochastic: oversold (<30) = potential long setup, overbought (>70) = potential short
    if features.get("stoch_k", 50) < 30:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 70:
        bearish_count += 1
    
    # OBV slope: positive = accumulation = bullish
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # MACD histogram: positive = bullish momentum
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # Require 2+ indicators to agree with direction
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"