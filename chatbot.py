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

    def recommend_hospital(self, risk_level):
        high_risk = ["City General Hospital", "Mental Health Center A", "Regional Hospital B"]
        moderate_risk = ["Clinic X", "Wellness Center Y", "Community Hospital Z"]
        if risk_level == "high":
            return high_risk
        elif risk_level == "moderate":
            return moderate_risk
        else:
            return []
