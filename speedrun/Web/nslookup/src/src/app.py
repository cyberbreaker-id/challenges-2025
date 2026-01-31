from flask import Flask, request, jsonify, render_template
import subprocess
import base64

app = Flask(__name__)

BLACKLISTED_CHARS = ['|', '&', ';', '$', '(', ')', '\\', '>', '<', '\n', '\r', '\t', '*', '?', '[', ']', '{', '}', '"', "'", '%', '=', '~']

def is_safe_input(user_input):
    return not any(char in user_input for char in BLACKLISTED_CHARS)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/nslookup", methods=["POST"])
def nslookup():
    data = request.get_json()
    domain = data.get("domain", "") if data else ""

    if not is_safe_input(domain):
        return jsonify({"error": "Input contains blacklisted characters"}), 400

    try:
        result = subprocess.check_output(f"nslookup {domain}", shell=True, stderr=subprocess.STDOUT, timeout=3)
        output = result.decode()

        if "NXDOMAIN" in output or "***" in output or "can't find" in output.lower():
            return jsonify({"error": "Invalid or unresolvable domain"}), 500

        if base64.b64decode("Q0JDew==").decode() in output.upper():
            return jsonify({"error": "Output contains blacklisted string"}), 500

        return jsonify({"result": output})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Invalid or unresolvable domain"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5002, debug=False)

