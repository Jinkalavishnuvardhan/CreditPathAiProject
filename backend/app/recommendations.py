
class RecommendationEngine:
    def __init__(self):
        self.actions = {
            "Low Risk": [
                "Send gentle SMS reminder",
                "Automated email nudge",
                "Offer loyalty discount for early payment"
            ],
            "Medium Risk": [
                "Offer flexible repayment plan",
                "SMS/Email Warning",
                "Schedule automated robo-call"
            ],
            "High Risk": [
                "Assign to recovery agent",
                "Offer significant settlement waiver",
                "Legal notice preparation"
            ]
        }

    def segment_borrower(self, default_prob: float) -> str:
        if default_prob < 0.2:
            return "Low Risk"
        elif default_prob < 0.6:
            return "Medium Risk"
        else:
            return "High Risk"

    def get_recommendation(self, default_prob: float) -> dict:
        segment = self.segment_borrower(default_prob)
        recommended_actions = self.actions.get(segment, [])
        return {
            "risk_segment": segment,
            "recommended_actions": recommended_actions,
            "default_probability": round(default_prob, 4)
        }
