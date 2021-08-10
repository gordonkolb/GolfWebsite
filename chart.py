from flask import Flask, redirect, url_for, render_template, request
app = Flask(__name__)

@app.route('/')
def hello_world():
    return "<h1>Hello, World!</h1>"

@app.route("/form", methods=["POST", "GET"])
def form():
    if request.method=="POST":
        name = request.form["nm"]
        return redirect(url_for("name", nm=name))
    else:
        return render_template("form.html")

@app.route("/<nm>")
def name(nm):
    return f"<h1>{nm}</h1>"


if __name__ == "__main__":
   app.run()