def guard(features: dict, prediction: str) -> str:
    """Filter false compression signals using ATR ratio, BB width, and momentum indicators."""
    # Detect low volatility compression
    is_compressed = features.get('bb_width', 1) < 0.4 and features.get('atr_ratio', 1) < 0.7
    
    if is_compressed and prediction != "skip":
        # False compression: stochastics extended AND price far from VWAP
        stoch_extreme = features.get('stoch_k', 50) > 80 or features.get('stoch_k', 50) < 20
        vwap_extended = abs(features.get('vwap_deviation', 0)) > 0.004
        
        if stoch_extreme and vwap_extended:
            return "skip"
        
        # False compression: OBV diverging from MACD direction
        obv_slope = features.get('obv_slope', 0)
        macd = features.get('macd_histogram', 0)
        if prediction == "long" and obv_slope < 0 and macd < 0:
            return "skip"
        if prediction == "short" and obv_slope > 0 and macd > 0:
            return "skip"
    
    return prediction