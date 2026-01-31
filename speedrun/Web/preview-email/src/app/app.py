from flask import Flask, request, render_template_string, abort
from email.utils import parseaddr
from datetime import date

app = Flask(__name__)

@app.route("/preview_invoice", methods=["GET"])
def preview_invoice():
    email = request.args.get("email", "")

    forbidden_substrings = [".", "[", "]", "+", "join", "mro", "base", "os", "popen", "subprocess", "builtins", "import" "{{", "}}"]

    if any(sub in email for sub in forbidden_substrings):
        abort(403)

    if parseaddr(email)[1] != email or "@" not in email:
        return "Invalid email", 400

    tpl = (
        "<h2>Invoice - 1</h2>"
        "<p>Hi " + email + ",</p>"
        "<p>Your total due is <strong>1 €</strong>.</p>"
        "<p>Regards,<br>Accounts Team</p>"
    )

    html = render_template_string(tpl)

    return html, 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
