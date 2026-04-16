def guard(features: dict, prediction: str) -> str:
    """Reject trades when momentum decelerates at extreme band positions."""
    macd_hist = features.get('macd_histogram', 0)
    bb_pct_b = features.get('bb_pct_b', 0.5)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_dev = features.get('vwap_deviation', 0)
    rsi_2h = features.get('rsi_2h', 50)
    
    # Momentum deceleration: histogram shrinking toward zero at extremes
    hist_near_zero = abs(macd_hist) < 0.0003
    at_upper_band = bb_pct_b > 0.8
    at_lower_band = bb_pct_b < 0.2
    
    if prediction == 'long':
        # Skip if bullish momentum decelerating near upper band with overbought stochastic
        if hist_near_zero and at_upper_band and stoch_k > 70:
            return 'skip'
        # Skip if price above VWAP but 2h RSI showing divergence
        if vwap_dev > 0.01 and rsi_2h < 35:
            return 'skip'
    
    elif prediction == 'short':
        # Skip if bearish momentum decelerating near lower band with oversold stochastic
        if hist_near_zero and at_lower_band and stoch_k < 30:
            return 'skip'
        # Skip if price below VWAP but 2h RSI showing divergence
        if vwap_dev < -0.01 and rsi_2h > 65:
            return 'skip'
    
    return prediction