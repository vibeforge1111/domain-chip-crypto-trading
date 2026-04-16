def guard(features: dict, prediction: str) -> str:
    """Filter trades during compressed markets using ATR, BB width, and momentum validation."""
    atr_ratio = features.get('atr_ratio', 1.0)
    bb_width = features.get('bb_width', 1.0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    vwap_deviation = features.get('vwap_deviation', 0)
    macd_histogram = features.get('macd_histogram', 0)
    obv_slope = features.get('obv_slope', 0)
    
    # Detect compression: both ATR and BB width are low
    is_compressed = atr_ratio < 0.7 and bb_width < 0.4
    
    if is_compressed:
        # During compression, stochastic extremes suggest exhaustion/false moves
        stoch_extreme = stoch_k > 85 or stoch_k < 15
        stoch_divergence = abs(stoch_k - stoch_d) > 20
        
        # VWAP far from price suggests distribution/accumulation trap
        vwap_far = abs(vwap_deviation) > 0.015
        
        # Flat MACD during compression = weak momentum, likely false breakout
        macd_weak = abs(macd_histogram) < 0.0002
        
        # OBV flat with price movement = divergence
        obv_divergent = abs(obv_slope) < 0.001 and abs(vwap_deviation) > 0.01
        
        # Skip if compression with multiple conflicting signals
        if (stoch_extreme and vwap_far) or (macd_weak and obv_divergent):
            return "skip"
    
    return prediction