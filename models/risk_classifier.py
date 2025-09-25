# Risk level calculation
from config import Config

class RiskClassifier:
    def __init__(self):
        self.risk_weights = Config.RISK_WEIGHTS
    
    def classify_risk(self, factors):
        """Classify risk level based on extracted factors"""
        try:
            score = 0
            rationale = []
            
            # Calculate risk score
            for factor in factors:
                if factor == 'smoking':
                    score += self.risk_weights.get('smoking', 25)
                    rationale.append('smoking')
                elif factor == 'poor diet':
                    score += self.risk_weights.get('poor_diet', 20)
                    rationale.append('high sugar diet')
                elif factor == 'low exercise':
                    score += self.risk_weights.get('low_exercise', 15)
                    rationale.append('low activity')
                elif factor == 'excessive alcohol':
                    score += self.risk_weights.get('excessive_alcohol', 15)
                    rationale.append('excessive alcohol consumption')
                elif factor == 'poor sleep':
                    score += self.risk_weights.get('poor_sleep', 10)
                    rationale.append('poor sleep quality')
                elif factor == 'high stress':
                    score += self.risk_weights.get('high_stress', 10)
                    rationale.append('high stress levels')
                elif factor == 'family history':
                    score += self.risk_weights.get('family_history', 15)
                    rationale.append('family history of health issues')
            
            # Determine risk level
            if score >= 70:
                risk_level = "high"
            elif score >= 40:
                risk_level = "moderate"
            else:
                risk_level = "low"
            
            return {
                "risk_level": risk_level,
                "score": min(score, 100),  # Cap at 100
                "rationale": rationale
            }
            
        except Exception as e:
            return {"error": f"Risk classification error: {str(e)}"}
