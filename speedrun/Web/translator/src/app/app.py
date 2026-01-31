from flask import Flask, request, render_template
import js2py

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    code = ""
    if request.method == "POST":
        code = request.form.get("code", "")
        try:
            output = js2py.eval_js(code)
            result = repr(output)
        except Exception as e:
            result = f"Error: {repr(e)}"
    return render_template("index.html", code=code)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)