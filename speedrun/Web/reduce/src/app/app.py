from flask import Flask, request, make_response
import pickle
import base64
import io
import pickletools

app = Flask(__name__)

def is_pickle_safe(pickled: bytes) -> bool:
    buf = io.StringIO()
    pickletools.dis(pickled, out=buf)
    disassembly = buf.getvalue()

    # No "reduce" :)
    if "REDUCE" in disassembly:
        return False
    return True


@app.route("/")
def index():
    cookie = request.cookies.get("session")
    if not cookie:
        resp = make_response("Welcome, guest! No session found.")
        default_session = {"username": "guest"}
        pickled = pickle.dumps(default_session)
        resp.set_cookie("session", base64.b64encode(pickled).decode())
        return resp

    try:
        decoded = base64.b64decode(cookie)

        if not is_pickle_safe(decoded):
            return "Nope!"

        data = pickle.loads(decoded)
        return f"Welcome back, {data.get('username', 'guest')}!"
    except Exception as e:
        return f"Error loading session: {e}"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
