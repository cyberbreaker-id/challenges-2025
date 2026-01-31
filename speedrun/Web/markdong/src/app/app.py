from flask import Flask, request, render_template_string, make_response
from markupsafe import escape
import requests

app = Flask(__name__)

INDEX_HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8" />
    <title>TinyPaste</title>
    <style>
      body { font-family: system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; max-width: 780px; margin: 3rem auto; }
      textarea { width: 100%; height: 220px; font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace; }
      .tip { color: #666; font-size: 0.9rem; }
      .box { border: 1px solid #ddd; border-radius: 12px; padding: 1rem; }
      .header { display:flex; justify-content:space-between; align-items:center; }
      .header small { color:#888 }
      code { background:#f5f5f5; padding:2px 4px; border-radius: 6px; }
    </style>
  </head>
  <body>
    <div class="header">
      <h1>📝 TinyPaste</h1>
      <small>markdown-ish preview</small>
    </div>

    <form class="box" method="post" action="/preview">
      <p class="tip">Type your note below and hit <strong>Preview</strong>.</p>
      <textarea name="content">Hello **world**!

Try *italics*, **bold**, and `code`.</textarea>
      <p style="margin-top:1rem">
        <button type="submit">Preview</button>
      </p>
    </form>

    <p class="tip">Health: <a href="/healthz">/healthz</a></p>
  </body>
</html>
"""

BLACKLIST = ("self", "os", "import", "class", "_", "[", "]")

def is_blocked(s: str):
    ls = s.lower()
    for t in BLACKLIST:
        if t in ls:
            return t
    return None

@app.get("/")
def index():
    return INDEX_HTML

@app.post("/preview")
def preview():
    content = request.form.get("content", "")
    html = escape(content)
    resp = make_response(f"<pre>{html}</pre>")
    resp.headers["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'"
    return resp

@app.get("/fetch")
def fetch():
    url = request.args.get("url", "")
    if not (url.startswith("http://") or url.startswith("https://")):
        return "Only http(s) allowed", 400
    blocked = ["127.0.0.1", "localhost"]
    for b in blocked:
        if b in url:
            return "Blocked host", 400
    try:
        r = requests.get(url, timeout=3, allow_redirects=True)
        txt = r.text[:5000]
        resp = make_response(txt)
        resp.headers["Content-Type"] = "text/plain; charset=utf-8"
        return resp
    except Exception as e:
        return f"Fetch error: {e}", 502

def is_local():
    ip = request.remote_addr or ""
    return ip.startswith("127.") or ip == "::1"

@app.route("/admin/preview", methods=["GET", "POST"])
def admin_preview():
    if not is_local():
        return "Admins only.", 403
    if request.method == "GET":
        content = request.args.get("content")
        if not content:
            return (
                "<h3>Admin Preview</h3>"
                "<form method=post>"
                "<textarea name=content rows=10 cols=80>{{ now() }}</textarea><br>"
                "<button>Render</button>"
                "</form>"
            )
        bad = is_blocked(content)
        if bad:
            return f"Render error: {bad}", 400
        try:
            return render_template_string(content)
        except Exception as e:
            return f"Render error: {e}", 400
    content = request.form.get("content", "")
    bad = is_blocked(content)
    if bad:
        return f"Render error: {bad}", 400
    try:
        rendered = render_template_string(content)
        resp = make_response(rendered)
        resp.headers["Content-Security-Policy"] = "default-src 'none'; style-src 'unsafe-inline'"
        return resp
    except Exception as e:
        return f"Render error: {e}", 400

@app.get("/healthz")
def healthz():
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
