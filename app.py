from flask import Flask, render_template, request
from trust_score import calculate_trust

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("shopsafe.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    url = request.form["url"]

    trust = calculate_trust(url)

    return render_template(
        "result.html",
        trust=trust
    )

if __name__ == "__main__":
    app.run(debug=True)