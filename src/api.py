import json
import sqlite3

from flask import Flask, g, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)

    def __init__(self, name):
        self.name = name

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(256), unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    project = db.relationship('Project',
                              backref=db.backref('routes', lazy='dynamic'))

    def __init__(self, domain):
        self.domain = domain


class Backend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    route = db.relationship('Route',
                            backref=db.backref('backends', lazy='dynamic'))

    def __init__(self, url):
        self.url = url

@app.route('/v1/<project>/mapping', methods=['GET'])
def all_mappings(project):
    return project
    pass

@app.route('/v1/<project_name>/mapping', methods=['PUT'])
def create_mapping(project_name):
    data = request.get_json(True)

    if 'domain' not in data or 'backends' not in data or not isinstance(data['backends'], list):
        return "Valid JSON but invalid format. Needs domain string and backends array"
    domain = data['domain']
    backend_urls = data['backends']

    project = Project.query.filter_by(name=project_name).first()
    if project is None:
        project = Project(project_name)
        db.session.add(project)

    route = Route.query.filter_by(domain=domain).first()
    if route is None:
        route = Route(domain)
        route.project = project
        db.session.add(route)

    for backend_url in backend_urls:
        # FIXME: Add validation for making sure these are valid
        backend = Backend(backend_url)
        backend.route = route
        db.session.add(backend)

    db.session.commit()
    return "", 200

@app.route('/v1/<project_name>/mapping/<domain>', methods=['DELETE'])
def delete_mapping(project_name, domain):
    project = Project.query.filter_by(name=project_name).first()
    if project is None:
        return "No such project", 400

    route = Route.query.filter_by(project=project, domain=domain).first()
    if route is None:
        return "No such domain", 400

    db.session.delete(route)
    db.session.commit()

    return "deleted", 200

@app.route('/v1/<project>/mapping/<host>', methods=['GET'])
def get_mapping(project, host):
    pass

if __name__ == '__main__':
    app.run(debug=True)
