
from flask import Flask, request, jsonify
from http import HTTPStatus
from connector.connector import Solver

app = Flask(__name__)

@app.route("/", methods = ['GET'])
def doc():
    app.logger.info("doc - Got request")
    with open("web/doc.html", "r") as f:
        return f.read()


@app.route("/<string:print_date>", methods = ['GET'])
def get_solution(print_date):
    solution = Solver(print_date).solve()
    # Flask doesn't like numpy types or Card;
    # this conversion might be better in the service
    solution = {int(k) : [c.content for c in v]for k, v in solution.items()}
    return jsonify(solution), HTTPStatus.OK


