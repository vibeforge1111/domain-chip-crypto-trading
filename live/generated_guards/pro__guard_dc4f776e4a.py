def guard(features: dict, prediction: str) -> str:
    """Filter trades where vwap_deviation and momentum_score disagree."""
    if prediction == "skip":
        return prediction
    
    vwap_dev = features.get("vwap_deviation", 0)
    momentum = features.get("momentum_score", 0)
    bb_pct = features.get("bb_pct_b", 0.5)
    
    # Check disagreement between momentum and VWAP position
    if prediction == "long":
        # Long requires bullish momentum but price below VWAP = disagreement
        if momentum > 0.15 and vwap_dev < -0.003:
            return "skip"
        # Also reject if at extreme BB upper area (overextended long)
        if bb_pct > 0.92:
            return "skip"
    elif prediction == "short":
        # Short requires bearish momentum but price above VWAP = disagreement
        if momentum < -0.15 and vwap_dev > 0.003:
            return "skip"
        # Also reject if at extreme BB lower area (overextended short)
        if bb_pct < 0.08:
            return "skip"
    
    return prediction