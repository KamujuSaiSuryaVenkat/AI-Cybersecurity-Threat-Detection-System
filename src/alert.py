def generate_alert(prediction):
    if prediction == 1:
        return {
            "severity": "HIGH",
            "message": "🚨 Possible Intrusion Detected",
            "action": "Block IP / Investigate"
        }
    else:
        return {
            "severity": "LOW",
            "message": "Normal Activity",
            "action": "No action needed"
        }