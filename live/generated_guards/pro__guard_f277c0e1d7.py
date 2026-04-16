def guard(features: dict, prediction: str) -> str:
    """Stochastic crossover timing guard - filters overextended stoch signals."""
    stoch_k = features.get("stoch_k", 50)
    stoch_d = features.get("stoch_d", 50)
    bb_pct_b = features.get("bb_pct_b", 0.5)
    rsi_14 = features.get("rsi_14", 50)
    rsi_2h = features.get("rsi_2h", 50)
    
    if prediction == "long":
        # Skip if stoch already overbought or deeply overbought
        if stoch_k > 70 or stoch_d > 80 or (stoch_k > 65 and stoch_d > 70):
            return "skip"
        # Skip if RSI extended upward (momentum fading)
        if rsi_14 > 65 and rsi_2h > 60:
            return "skip"
        # Skip if already near upper band with bearish alignment
        if stoch_k < stoch_d and bb_pct_b > 0.75:
            return "skip"
    
    elif prediction == "short":
        # Skip if stoch already oversold or deeply oversold
        if stoch_k < 30 or stoch_d < 20 or (stoch_k < 35 and stoch_d < 30):
            return "skip"
        # Skip if RSI oversold with stoch bullish (potential reversal)
        if rsi_14 < 35 and stoch_k > stoch_d:
            return "skip"
        # Skip if near lower band with bullish alignment
        if stoch_k > stoch_d and bb_pct_b < 0.25:
            return "skip"
    
    return prediction