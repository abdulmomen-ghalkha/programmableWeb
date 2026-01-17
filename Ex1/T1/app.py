from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "This file for submission for the first exercise"

@app.route("/add/<float:number_1>/<float:number_2>/")
def plus(number_1, number_2):
    return f"number_1 + number_2 = {number_1 + number_2}"


@app.route("/sub/<float:number_1>/<float:number_2>/")
def minus(number_1, number_2):
    return f"number_1 + number_2 = {number_1 - number_2}"

@app.route("/mul/<float:number_1>/<float:number_2>/")
def mult(number_1, number_2):
    return f"number_1 * number_2 = {number_1 * number_2}"

@app.route("/div/<float:number_1>/<float:number_2>/")
def div(number_1, number_2):
    if number_2 == 0: 
        return "NaN"
    return f"number_1 / number_2 = {(number_1 / number_2):.3f}"

@app.route("/hello/<name>/")
def hello(name):
    return f"Hello {name}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)