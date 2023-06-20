from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return data, 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture.get("id") == id:
            return picture, 200
    return "", 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    if any(existing_picture.get("id") == new_picture.get("id") for existing_picture in data):
        return {"Message": f"picture with id {new_picture['id']} already present"}, 302

    data.append(new_picture)
    return new_picture, 201


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_information = request.json
    for picture in data:
        if picture.get("id") == id:
            picture.update(new_information)
            return picture, 200
    else:
        return {"message": f"picture with id {id} not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for picture in data:
        if str(picture.get("id")) == str(id):
            data.remove(picture)
            return '', 204
    else:
        return {"message": f"picture with id {id} not found"}, 404
