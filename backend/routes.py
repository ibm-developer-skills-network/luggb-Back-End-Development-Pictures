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
    if data:
        resp = make_response(data)
        resp.status_code = 200
    else:
        resp = make_response({"message": "Internal server error"})
        resp.status_code = 500
    return resp

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture["id"] == id:
            return picture
    return {"message": "picture not found"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_picture = request.json
    new_picture_id = new_picture["id"]
    if not new_picture:
        return {"message": "Invalid input parameter"}, 422
    for picture in data:
        if picture["id"] == new_picture_id:
            return {"Message": f"picture with id {picture['id']} already present"}, 302
    try:
        data.append(new_picture)
    except NameError:
        return {"message": "Picture not defined"}, 500
    for picture in data:
        if picture["id"] == new_picture_id:
            return picture, 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    for i in range(len(data)):
        if data[i]["id"] == id:
            data[i] = request.json
            return data[i], 201

    return {"message": f"picture with {id} not found!"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    for index, picture in enumerate(data):
        if picture["id"] == id:
            data.remove(data[index])
            return {"message": f"picture {id} removed"}, 204
    return {"message": "picture not found"}, 404

