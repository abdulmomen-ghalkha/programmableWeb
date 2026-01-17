import math
from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def index():
    return "This file for submission for the first exercise"

@app.route("/trig/<func>/")

def trig(func):
    try:
        angle = float(request.args["angle"])

        unit = request.args.get("unit", "radian")

        if unit == "degree":
            angle = math.radians(angle)
        elif unit == "radian":
            pass
        else:
            return "Invalid query parameter value(s)", 400
        result = 0
        if func == "sin":
            result = math.sin(angle)
        elif func == "cos":
            result = math.cos(angle)
        elif func == "tan":
            result = math.tan(angle)
        else:
            return "Operation not found", 404
        return str(result)
    except KeyError:
        return "Missing query parameter: angle", 400
    except ValueError:
        return "Invalid query parameter value(s)", 400
