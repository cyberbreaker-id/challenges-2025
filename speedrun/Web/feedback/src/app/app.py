from flask import Flask, request
from mako.template import Template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def feedback():
    if request.method == "POST":
        fb = request.form.get("message", "")
        forbidden = ["<", ">", "os"]

        if any(c in fb for c in forbidden):
            return "Invalid input", 400

        if len(fb) > 50:
            return "Input too long", 400

        template = Template("Thank you for your feedback: %s" % fb)
        return template.render()

    return """
    <!DOCTYPE html>
    <html>
    <head><title>Feedback</title></head>
    <body>
      <h1>Feedback</h1>
      <form action="/" method="post">
        <textarea name="message" rows="5" cols="50" placeholder="Write your feedback..."></textarea><br>
        <button type="submit">Send</button>
      </form>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
