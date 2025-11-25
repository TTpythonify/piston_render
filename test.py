import requests
import json
import traceback

url = "http://127.0.0.1:8000/execute"

java_code = """
public class Test {
    public static void main(String[] args) {
        System.out.println("Java is working!");
    }
}
"""

payload = {
    "language": "java",
    "code": java_code
}

print("=== Sending request ===")

try:
    response = requests.post(url, json=payload)

    print("\n=== Response Info ===")
    print("Status Code:", response.status_code)
    print("Raw Text:", response.text)

    print("\n=== Parsed JSON (if valid) ===")
    try:
        data = response.json()
        print(json.dumps(data, indent=4))

        # Print stderr if included
        if isinstance(data, dict) and "stderr" in data:
            print("\n=== STDERR from server ===")
            print(data["stderr"])

    except json.JSONDecodeError:
        print("❌ Response was not valid JSON")

except Exception as e:
    print("\n=== Exception occurred ===")
    print(type(e).__name__, str(e))
    print("\n=== Full Traceback ===")
    traceback.print_exc()


""""
=== Sending request ===

=== Response Info ===
Status Code: 200
Raw Text: {"stderr":"/bin/bash: line 1: javac: command not found\n","stdout":""}


=== Parsed JSON (if valid) ===
{
    "stderr": "/bin/bash: line 1: javac: command not found\n",
    "stdout": ""
}

=== STDERR from server ===
/bin/bash: line 1: javac: command not found
}
"""