import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from exceptions import APIError, APIPaginationError
from models import Magazine
from schemas import MagazineSchema
from utils import build_link_header, validate_per_page

app = Flask(__name__)
db = SQLAlchemy(app)
ma = Marshmallow(app)

# app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")


@app.route("/magazines")
def magazines():
    # process query parameters
    page = request.args.get("page", 1, type=int)
    per_page = validate_per_page(request.args.get("per-page", 100, type=int))

    # query
    magazines = Magazine.query.paginate(page, per_page) 

    # map with schema
    magazine_schema = MagazineSchema()
    magazines_dumped = magazine_schema.dump(magazines.items, many=True)    

    # combined results with pagination
    results = {
        "results": magazines_dumped,
        "pagination":
            {
                "count": magazines.total,
                "page": page,
                "per_page": per_page,
                "pages": magazines.pages,
            },
    }
    
    # paginated link headers
    base_url = "https://api.mysite.org/magazines"
    link_header = build_link_header(
        query=magazines, base_url=base_url, per_page=per_page
    )
    return jsonify(results), 200, link_header


@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    # credit: https://medium.com/datasparq-technology/flask-api-exception-handling-with-custom-http-response-codes-c51a82a51a0f
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors
    app.logger.error("{}: {}".format(err.description, response["message"]))
    return jsonify(response), err.code