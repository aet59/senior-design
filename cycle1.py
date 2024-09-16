from flask import Flask

app = Flask(__name__)

@app.route("/")

def frontpage():
    return "CYCLE 1, PULLING UP THE WEB"

app.run(host="0.0.0.0", port=80)
