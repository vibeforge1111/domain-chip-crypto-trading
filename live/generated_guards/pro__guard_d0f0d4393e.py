def guard(features: dict, prediction: str) -> str:
    """Filter trades with VWAP/momentum disagreement or extreme stochastic conditions."""
    vwap_dev = features.get('vwap_deviation', 0)
    momentum = features.get('momentum_score', 0)
    stoch_k = features.get('stoch_k', 50)
    stoch_d = features.get('stoch_d', 50)
    
    # Sign disagreement between VWAP position and momentum direction
    vwap_momentum_disagree = (vwap_dev > 0.005 and momentum < -0.1) or (vwap_dev < -0.005 and momentum > 0.1)
    
    # Stochastic overbought/oversold extremes with directional conflict
    stoch_extreme = (stoch_k > 80 and stoch_d > 80 and vwap_dev > 0 and momentum < 0) or \
                    (stoch_k < 20 and stoch_d < 20 and vwap_dev < 0 and momentum > 0)
    
    if vwap_momentum_disagree or stoch_extreme:
        return "skip"
    
    return prediction