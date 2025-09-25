# Generate recommendations
class Recommender:
    def __init__(self):
        self.recommendations_db = {
            'smoking': [
                "Quit smoking immediately - consult a healthcare provider for cessation programs",
                "Consider nicotine replacement therapy",
                "Join a smoking cessation support group"
            ],
            'poor diet': [
                "Reduce sugar intake and processed foods",
                "Increase consumption of fruits and vegetables",
                "Consult a nutritionist for a personalized meal plan"
            ],
            'low exercise': [
                "Walk 30 minutes daily",
                "Start with light exercises and gradually increase intensity",
                "Consider joining a gym or fitness class"
            ],
            'excessive alcohol': [
                "Limit alcohol consumption to recommended guidelines",
                "Seek professional help if needed",
                "Replace alcohol with healthier beverages"
            ],
            'poor sleep': [
                "Maintain a regular sleep schedule",
                "Create a comfortable sleep environment",
                "Avoid caffeine and screens before bedtime"
            ],
            'high stress': [
                "Practice stress management techniques like meditation",
                "Consider counseling or therapy",
                "Engage in relaxing activities like yoga"
            ],
            'family history': [
                "Schedule regular health checkups",
                "Discuss family history with your healthcare provider",
                "Consider preventive screening tests"
            ]
        }
    
    def generate_recommendations(self, risk_level, factors):
        """Generate actionable health recommendations"""
        try:
            recommendations = []
            
            # Get specific recommendations for each factor
            for factor in factors:
                if factor in self.recommendations_db:
                    recommendations.extend(self.recommendations_db[factor])
            
            # Add general recommendations based on risk level
            if risk_level == "high":
                recommendations.insert(0, "Consult a healthcare provider immediately")
                recommendations.append("Consider comprehensive health screening")
            elif risk_level == "moderate":
                recommendations.append("Schedule a routine health checkup")
                recommendations.append("Monitor your health metrics regularly")
            else:
                recommendations.append("Maintain current healthy lifestyle")
                recommendations.append("Continue regular health monitoring")
            
            # Remove duplicates while preserving order
            unique_recommendations = []
            seen = set()
            for rec in recommendations:
                if rec not in seen:
                    unique_recommendations.append(rec)
                    seen.add(rec)
            
            return {
                "risk_level": risk_level,
                "factors": factors,
                "recommendations": unique_recommendations[:10],  # Limit to top 10
                "status": "ok"
            }
            
        except Exception as e:
            return {"error": f"Recommendation generation error: {str(e)}"}
