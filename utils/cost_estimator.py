"""BOM Cost Estimation Tool"""

import logging
from typing import Dict, List, Any

logger = logging.getLogger(__name__)


class CostEstimator:
    def __init__(self):
        self.volume_discounts = {
            100: 1.0,
            1000: 0.75,
            10000: 0.55,
            100000: 0.40
        }
    
    def estimate_bom_cost(
        self,
        components: List[Dict],
        volume: int = 1000,
        region: str = "EU"
    ) -> Dict[str, Any]:
        """
        Estimate Bill of Materials cost
        """
        estimation = {
            "volume": volume,
            "region": region,
            "components": [],
            "total_cost": 0.0,
            "cost_per_unit": 0.0,
            "currency": "EUR" if region == "EU" else "USD"
        }
        
        discount_factor = self._get_volume_discount(volume)
        
        for component in components:
            unit_price = component.get("unit_price", 0.0)
            quantity = component.get("quantity", 1)
            
            discounted_price = unit_price * discount_factor
            line_cost = discounted_price * quantity
            
            estimation["components"].append({
                "part_number": component.get("part_number"),
                "quantity": quantity,
                "unit_price": round(unit_price, 4),
                "discounted_price": round(discounted_price, 4),
                "line_cost": round(line_cost, 4)
            })
            
            estimation["total_cost"] += line_cost
        
        estimation["total_cost"] = round(estimation["total_cost"], 2)
        estimation["cost_per_unit"] = round(estimation["total_cost"], 2)
        
        return estimation
    
    def _get_volume_discount(self, volume: int) -> float:
        """Get volume discount factor"""
        for vol_threshold in sorted(self.volume_discounts.keys(), reverse=True):
            if volume >= vol_threshold:
                return self.volume_discounts[vol_threshold]
        return 1.0
    
    def compare_alternatives(
        self,
        component_alternatives: List[List[Dict]],
        volume: int = 1000
    ) -> Dict[str, Any]:
        """
        Compare cost of alternative component choices
        """
        comparisons = []
        
        for idx, alternative in enumerate(component_alternatives):
            cost_estimate = self.estimate_bom_cost(alternative, volume)
            comparisons.append({
                "alternative": f"Option {idx + 1}",
                "total_cost": cost_estimate["total_cost"],
                "components": [c.get("part_number") for c in alternative]
            })
        
        # Sort by cost
        comparisons.sort(key=lambda x: x["total_cost"])
        
        return {
            "volume": volume,
            "alternatives": comparisons,
            "best_option": comparisons[0] if comparisons else None,
            "savings": round(comparisons[-1]["total_cost"] - comparisons[0]["total_cost"], 2) if len(comparisons) > 1 else 0
        }
