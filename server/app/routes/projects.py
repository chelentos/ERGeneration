from flask import request, jsonify
from flask_login import login_required, current_user

from app import app
from app.models.Project import Project
from app.models.Requirement import Requirement


@app.route("/api/projects", methods=["GET"])
@login_required
def projects():
  projects = Project.objects(parent=current_user.id).only('name')
  response_projects = list(map(lambda x: {
      "name": x.name,
      "erd": x.erd,
      "id": str(x.pk),
      "reqsNum": Requirement.objects(parent=x.id).count()
    }, projects))
  return {"projects": response_projects}

@app.route("/api/projects", methods=["POST"])
@login_required
def create_new_project():
  name = request.json['name']
  if name:
    Project(name=name, parent=current_user.id).save()
    return jsonify({"text": "Project created."}), 200
  return jsonify({"text": "Project name needed."}), 500

@app.route("/api/projects/<id>", methods=["DELETE"])
@login_required
def delete_project(id):
  if id:
    Project(pk=id).delete()
    return jsonify({"text": "Project deleted."}), 200
  return jsonify({"text": "Project id needed."}), 500