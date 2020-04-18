from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    message = "! Jai Mahakal !"
    return render_template("homepage.html",message=message)

if __name__ == "__main__":
    app.run()
