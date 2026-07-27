import json
import requests

def get_threat_intel(ip):
    # Simulated IP reputation check (Mock API response)
    return {
        "ip": ip,
        "is_tor_exit_node": True,
        "abuse_confidence_score": 98,
        "country": "NL"
    }

def analyze_alert(alert, intel):
    prompt = f"""
You are an expert Security Operations Center (SOC) Lead Analyst.
Analyze the following security incident and threat intelligence, then respond ONLY in valid JSON.

[ALERT DATA]:
{json.dumps(alert, indent=2)}

[THREAT INTEL]:
{json.dumps(intel, indent=2)}

Provide your assessment in this exact JSON structure:
{{
  "severity_rating": "<Low | Medium | High | Critical>",
  "risk_score_1_to_10": <number>,
  "mitre_attack": {{
    "tactic": "<e.g. Credential Access>",
    "technique_id": "<e.g. T1110.001>",
    "technique_name": "<e.g. Password Guessing>"
  }},
  "incident_summary": "<Brief 2-3 sentence executive summary>",
  "recommended_actions": [
    "<Action 1>",
    "<Action 2>",
    "<Action 3>"
  ]
}}
"""

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    try:
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        return json.loads(response.json()["response"])
    except Exception as e:
        return {"error": f"Failed to reach Ollama: {str(e)}"}

if __name__ == "__main__":
    print("Reading alert file...")
    with open("alert.json", "r") as f:
        alert_data = json.load(f)

    print("Fetching threat intelligence...")
    intel_data = get_threat_intel(alert_data["source_ip"])

    print("Analyzing alert with local AI engine...")
    result = analyze_alert(alert_data, intel_data)

    print("\n================ AI SOC TRIAGE REPORT ================")
    print(json.dumps(result, indent=2))