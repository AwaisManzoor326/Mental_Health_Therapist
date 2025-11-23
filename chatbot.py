import requests
import json

class MentalHealthChatbot:
    def __init__(self, groq_api_key):
        self.api_key = groq_api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def ask(self, prompt, session_history=[]):

        # Messages format required by Groq
        messages = [{"role": "user", "content": prompt}]

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 500
        }

        try:
            response = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers=self.headers,
                data=json.dumps(payload)
            )

            if response.status_code == 200:
                res = response.json()
                return res["choices"][0]["message"]["content"]
            else:
                return f"Error {response.status_code}: {response.text}"

        except Exception as e:
            return f"Error connecting to AI: {str(e)}"


    def assess_risk(self, text):
        prompt = f"Assess mental health risk from this text (low, moderate, high): {text}"
        risk = self.ask(prompt)
        if "high" in risk.lower():
            return "high"
        elif "moderate" in risk.lower():
            return "moderate"
        else:
            return "low"

    def recommend_hospital(self, risk_level, country="Pakistan", city=None):
        """
        Returns hospital recommendations based on risk level.
        Optionally, country and city can be provided.
        """
        # Example hospitals database (expand as needed)
        hospitals_db = {
            "Pakistan": {
                "Islamabad": ["Pakistan Institute of Medical Sciences (PIMS)", "Islamabad Mental Health Center"],
                "Lahore": ["Faisal Hospital Lahore", "Mental Health Institute Lahore"],
                "Karachi": ["Karachi Mental Health Hospital", "Aga Khan University Hospital"],
                "Default": ["National Institute of Mental Health, Pakistan"]
            },
            "USA": {
                "New York": ["NYC Health + Hospitals/Bellevue", "Mount Sinai Hospital"],
                "Los Angeles": ["UCLA Resnick Neuropsychiatric Hospital", "Cedars-Sinai Medical Center"],
                "Default": ["National Mental Health Center, USA"]
            }
        }

        recommendations = []

        if risk_level == "high":
            if country in hospitals_db:
                if city and city in hospitals_db[country]:
                    recommendations = hospitals_db[country][city]
                else:
                    recommendations = hospitals_db[country]["Default"]
            else:
                recommendations = ["Please consult the nearest mental health hospital in your area."]
        elif risk_level == "moderate":
            recommendations = ["Local Clinic", "Wellness Center", "Community Hospital"]
        else:
            recommendations = ["No hospital needed. Consider self-care and regular check-ups."]

        return recommendations

