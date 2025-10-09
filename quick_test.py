"""
Quick test to verify webhook works locally
"""
import requests
import json

# Test payload that simulates what VAPI sends
payload = {
    "message": {
        "type": "tool-calls",
        "toolCalls": [{
            "type": "function",
            "function": {
                "name": "Add_todo",
                "arguments": json.dumps({"todo": "Buy milk from test"})
            }
        }]
    },
    "call": {
        "id": "test_call",
        "customer": {
            "number": "+1234567890"
        }
    }
}

# Send to local server
response = requests.post(
    "http://localhost:8000/api/v1/vapi/webhook",
    json=payload
)

print("Status Code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))
