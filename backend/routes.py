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
        return jsonify(data), 200

    return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id): 
    if data:
        for x in data:
            if x["id"] == id:
                return jsonify(x), 200
    return {"message": "Internal server error"}, 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    data2 = json.loads(request.data)
    if data:
        for x in data:
            if x["id"] == data2["id"]:
                return jsonify(Message=f"picture with id {data2['id']} already present"), 302

        data.append(data2)
        return {"id": data2["id"]}, 201


    return {"message": "Internal server error"}, 404

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    data2 = json.loads(request.data)
    if data:
        for i in range(len(data)):
            if data[i]["id"] == data2["id"]:
                data[i] = data2
                return jsonify(Message=f"OK"), 200

    return {"message": "picture not found"}, 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for i in range(len(data)):
            if data[i]["id"] == id:
                data.pop(i)
                return jsonify(Message=f"OK"), 204

    return {"message": "picture not found"}, 404
