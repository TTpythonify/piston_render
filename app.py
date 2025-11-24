from flask import Flask, request, jsonify
import subprocess
import tempfile
import os

app = Flask(__name__)

# Linux-compatible commands
LANG_COMMANDS = {
    "python": ["python3", "main.py"],
    "javascript": ["node", "main.js"],
    "java": ["bash", "-c", "javac Main.java && java Main"],
    "c": ["bash", "-c", "gcc main.c -o main && ./main"],
    "cpp": ["bash", "-c", "g++ main.cpp -o main && ./main"]
}

# Filenames per language
LANG_FILENAMES = {
    "python": "main.py",
    "javascript": "main.js",
    "java": "Main.java",
    "c": "main.c",
    "cpp": "main.cpp"
}

@app.post("/execute")
def execute():
    data = request.get_json()
    language = data.get("language")
    code = data.get("code")

    if language not in LANG_COMMANDS:
        return jsonify({"error": "Unsupported language"}), 400

    filename = LANG_FILENAMES[language]

    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = os.path.join(tmpdir, filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(code)

        try:
            result = subprocess.run(
                LANG_COMMANDS[language],
                cwd=tmpdir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=5
            )
            return jsonify({
                "stdout": result.stdout,
                "stderr": result.stderr
            })
        except subprocess.TimeoutExpired:
            return jsonify({"error": "Timeout"}), 400
        except Exception as e:
            return jsonify({"error": str(e)}), 500

@app.get("/")
def home():
    return "Piston Render Version Running (Linux-Compatible)"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
