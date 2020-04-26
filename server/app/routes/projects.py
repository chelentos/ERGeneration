from flask import request, jsonify
from flask_login import login_required, current_user

from app import app
from app.models.Project import Project
from app.models.ER import ER
from app.models.Requirement import Requirement

from nlp.classify import classifyReqs
from nlp.er_generation import getErFromText, getErFromERSents, exportXML

from app.tt_generation import generateTT

@app.route("/api/projects", methods=["GET"])
@login_required
def projects():
  projects = Project.objects(parent=current_user.id).only('name')
  response_projects = list(map(lambda x: {
      "name": x.name,
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

@app.route("/api/projects/<id>", methods=["GET"])
@login_required
def get_project(id):
  if id:
    project = Project.objects(pk=id).first()
    requirements = Requirement.objects(parent=id)
    ers = ER.objects(parent=id)
    return jsonify({"project": getResponseProject(project, requirements, ers)}), 200
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/<id>", methods=["DELETE"])
@login_required
def delete_project(id):
  if id:
    Project(pk=id).delete()
    return jsonify({"text": "Project deleted."}), 200
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/<id>/reqs", methods=["POST"])
@login_required
def load_reqs(id):
  if id:
    project = Project.objects(pk=id).first()
    if project:
      classifiedReqs = classifyReqs(request.json['reqs'])
      for req in classifiedReqs:
        Requirement(text=req['text'],
                    req_type=req['type'],
                    parent=id).save()
      requirements = Requirement.objects(parent=id)
      return jsonify({"reqs": getResponseReqs(requirements)}), 200
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/<id>/reqs", methods=["PUT"])
@login_required
def update_req(id):
  if id:
    project = Project.objects(pk=id).first()
    if project:
      success = Requirement(pk=request.json['req']['id']).update(
        text = request.json['req']['text'],
        req_type = request.json['req']['type'],
        parent = id
      )
      if success:
        return jsonify({"text": "Req was updated"}), 200
      else:
        return jsonify({"text": "Req was not updated"}), 500
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/<project_id>/reqs/<req_id>", methods=["DELETE"])
@login_required
def delete_req(project_id, req_id):
  if req_id:
    Requirement(pk=req_id).delete()
    return jsonify({"text": "Requirement deleted."}), 200
  return jsonify({"text": "Requirement id needed."}), 500

@app.route("/api/projects/<project_id>/generate-tt", methods=["POST"])
@login_required
def generate_TTs(project_id):
  if project_id:
    requirements = request.json['reqs']
    ttLink = generateTT(requirements)
    return jsonify({"text": "TT generated.", "ttLink": ttLink}), 200
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/<project_id>/generate-ersents", methods=["POST"])
@login_required
def generate_ERSents(project_id):
  if project_id:
    text = request.json['text']
    if text:
      ERSents = getErFromText(text)
      return jsonify({"text": "ERSents generated.", "er": ERSents}), 200
    else:
      return jsonify({"text": "No text."}), 500
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/generate-er", methods=["POST"])
@login_required
def generate_ER():
  sents = request.json['sents']
  if sents:
    er = getErFromERSents(sents)
    return jsonify({"text": "ER generated.", "er": er}), 200
  else:
    return jsonify({"text": "No text."}), 500

@app.route("/api/projects/<project_id>/save-er", methods=["POST"])
@login_required
def save_ER(project_id):
  if project_id:
    er = request.json['er']
    if er:
      ER(name=er['name'], erd=er['erd'], parent=project_id).save()
      return jsonify({"text": "ER generated."}), 200
    else:
      return jsonify({"text": "No er."}), 500
  return jsonify({"text": "Project id needed."}), 500

@app.route("/api/projects/xml_export", methods=["POST"])
@login_required
def get_XML():
  er = request.json['er']
  if er:
    return jsonify({"text": "TT generated.", "xmlLink": exportXML(er)}), 200
  else:
    return jsonify({"text": "No er."}), 500

def getResponseReqs(reqs):
  return list(map(lambda x: {
        "text": x.text,
        "type": x.req_type,
        "id": str(x.pk),
        "createdAt": x.id.generation_time
      }, reqs))

def getResponseErs(ers):
  return list(map(lambda x: {
        "name": x.name,
        "erd": x.erd,
        "createdAt": x.id.generation_time
      }, ers))

def getResponseProject(project, reqs, ers):
  rProject = {}
  rProject['id'] = str(project.id)
  rProject['name'] = project.name
  rProject['reqs'] = getResponseReqs(reqs)
  rProject['ers'] = getResponseErs(ers)
  return rProject