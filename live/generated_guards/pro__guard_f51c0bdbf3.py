def guard(features: dict, prediction: str) -> str:
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # VWAP: price above = bullish
    if features.get("vwap_deviation", 0) > 0:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < 0:
        bearish_count += 1
    
    # Stochastic: above 50 = bullish
    if features.get("stoch_k", 50) > 60:
        bullish_count += 1
    elif features.get("stoch_k", 50) < 40:
        bearish_count += 1
    
    # OBV slope: positive = bullish
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # MACD histogram: positive = bullish
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # RSI 2h context: above/below 50
    if features.get("rsi_2h", 50) > 52:
        bullish_count += 1
    elif features.get("rsi_2h", 50) < 48:
        bearish_count += 1
    
    # BB position: below 0.3 = bullish, above 0.7 = bearish
    if features.get("bb_pct_b", 0.5) < 0.3:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.7:
        bearish_count += 1
    
    # Require 2+ aligned signals
    if prediction == "long" and bullish_count < 2:
        return "skip"
    if prediction == "short" and bearish_count < 2:
        return "skip"
    
    return prediction