def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction
    
    bullish_count = 0
    bearish_count = 0
    
    # BB position: below 0.2 oversold (bullish), above 0.8 overbought (bearish)
    if features.get("bb_pct_b", 0.5) < 0.2:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.8:
        bearish_count += 1
    
    # VWAP deviation: below VWAP (bullish), above VWAP (bearish)
    if features.get("vwap_deviation", 0) < -0.005:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) > 0.005:
        bearish_count += 1
    
    # Stochastic: below 20 oversold (bullish), above 80 overbought (bearish)
    if features.get("stoch_k", 50) < 20 and features.get("stoch_d", 50) < 20:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 80 and features.get("stoch_d", 50) > 80:
        bearish_count += 1
    
    # OBV slope: positive = bullish accumulation
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1
    
    # MACD histogram: positive = bullish momentum
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1
    
    # RSI 2h: below 40 oversold (bullish), above 60 overbought (bearish)
    if features.get("rsi_2h", 50) < 40:
        bullish_count += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish_count += 1
    
    # Require 2+ signals to agree
    if prediction == "long" and bullish_count >= 2:
        return prediction
    elif prediction == "short" and bearish_count >= 2:
        return prediction
    
    return "skip"