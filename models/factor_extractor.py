# Extract risk factors
from config import Config

class FactorExtractor:
    def __init__(self):
        self.risk_factors = {
            'smoking': ['smoker'],
            'poor_diet': ['diet'],
            'low_exercise': ['exercise'],
            'excessive_alcohol': ['alcohol'],
            'poor_sleep': ['sleep'],
            'high_stress': ['stress'],
            'family_history': ['family_history']
        }
    
    def extract_factors(self, answers):
        """Extract risk factors from survey answers"""
        try:
            factors = []
            confidence_scores = []
            
            # Check smoking
            if answers.get('smoker') is True:
                factors.append('smoking')
                confidence_scores.append(0.95)
            
            # Check diet
            diet = answers.get('diet', '').lower()
            if any(term in diet for term in ['high sugar', 'fast food', 'processed', 'junk']):
                factors.append('poor diet')
                confidence_scores.append(0.9)
            
            # Check exercise
            exercise = answers.get('exercise', '').lower()
            if exercise in ['rarely', 'never', 'seldom']:
                factors.append('low exercise')
                confidence_scores.append(0.85)
            
            # Check alcohol
            alcohol = answers.get('alcohol', '').lower()
            if alcohol in ['heavy', 'excessive', 'daily']:
                factors.append('excessive alcohol')
                confidence_scores.append(0.9)
            
            # Check sleep
            sleep = answers.get('sleep', '').lower()
            if any(term in sleep for term in ['poor', 'insomnia', 'less than 6', '<6']):
                factors.append('poor sleep')
                confidence_scores.append(0.8)
            
            # Check stress
            stress = answers.get('stress', '').lower()
            if stress in ['high', 'severe', 'chronic']:
                factors.append('high stress')
                confidence_scores.append(0.85)
            
            # Check family history
            family_history = answers.get('family_history', '').lower()
            if family_history in ['yes', 'true', 'positive']:
                factors.append('family history')
                confidence_scores.append(0.9)
            
            # Calculate overall confidence
            if confidence_scores:
                overall_confidence = sum(confidence_scores) / len(confidence_scores)
            else:
                overall_confidence = 0.95  # High confidence when no risk factors
            
            return {
                "factors": factors,
                "confidence": round(overall_confidence, 2)
            }
            
        except Exception as e:
            return {"error": f"Factor extraction error: {str(e)}"}
