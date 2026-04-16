def guard(features: dict, prediction: str) -> str:
    """Multi-indicator confirmation guard requiring 2+ signals to agree."""
    if prediction == "skip":
        return prediction

    bullish_count = 0
    bearish_count = 0

    # Stochastic oversold (<20) = bullish, overbought (>80) = bearish
    if features.get("stoch_k", 50) < 20:
        bullish_count += 1
    elif features.get("stoch_k", 50) > 80:
        bearish_count += 1

    # Stochastic D confirmation
    if features.get("stoch_d", 50) < 20:
        bullish_count += 1
    elif features.get("stoch_d", 50) > 80:
        bearish_count += 1

    # Bollinger Band position: near lower band = bullish, near upper = bearish
    if features.get("bb_pct_b", 0.5) < 0.2:
        bullish_count += 1
    elif features.get("bb_pct_b", 0.5) > 0.8:
        bearish_count += 1

    # VWAP deviation: above = bullish, below = bearish
    if features.get("vwap_deviation", 0) > 0.001:
        bullish_count += 1
    elif features.get("vwap_deviation", 0) < -0.001:
        bearish_count += 1

    # OBV slope: positive = bullish accumulation
    if features.get("obv_slope", 0) > 0:
        bullish_count += 1
    elif features.get("obv_slope", 0) < 0:
        bearish_count += 1

    # MACD histogram: positive = bullish, negative = bearish
    if features.get("macd_histogram", 0) > 0:
        bullish_count += 1
    elif features.get("macd_histogram", 0) < 0:
        bearish_count += 1

    # RSI 2h oversold/overbought in wider context
    if features.get("rsi_2h", 50) < 40:
        bullish_count += 1
    elif features.get("rsi_2h", 50) > 60:
        bearish_count += 1

    # Require at least 2 signals to agree with prediction
    if prediction == "long" and bearish_count >= 2:
        return "skip"
    if prediction == "short" and bullish_count >= 2:
        return "skip"

    return prediction