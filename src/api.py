#   Copyright 2013 Yuvi Panda <yuvipanda@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# FIXME: Extremely unoptimized SQL ahead.
import flask
from flask.ext.sqlalchemy import SQLAlchemy

app = flask.Flask(__name__)
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

@app.route('/v1/<project_name>/mapping', methods=['GET'])
def all_mappings(project_name):
    project = Project.query.filter_by(name=project_name).first()
    if project is None:
        return "No such project", 400

    data = {'project': project.name, 'routes': []}
    for route in project.routes:
        data['routes'].append({'domain': route.domain})

    return flask.jsonify(**data)


@app.route('/v1/<project_name>/mapping', methods=['PUT'])
def create_mapping(project_name):
    data = flask.request.get_json(True)

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

@app.route('/v1/<project_name>/mapping/<domain>', methods=['GET'])
def get_mapping(project_name, domain):
    project = Project.query.filter_by(name=project_name).first()
    if project is None:
        return "No such project", 400

    route = Route.query.filter_by(project=project, domain=domain).first()
    if route is None:
        return "No such domain", 400

    data = {'domain': route.domain, 'backends': []}
    for backend in route.backends:
        data['backends'].append(backend.url)

    return flask.jsonify(**data)

if __name__ == '__main__':
    app.run(debug=True)
