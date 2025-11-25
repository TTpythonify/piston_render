import requests
import json

# Your Render Piston API URL
url = "https://piston-render.onrender.com/execute"

# Code you want to run
payload = {
    "language": "python",
    "code": "print(2+3)"
}

# Send POST request
response = requests.post(url, json=payload)

# Parse JSON response
result = response.json()

print("STDOUT:")
print(result.get("stdout"))

print("STDERR:")
print(result.get("stderr"))
