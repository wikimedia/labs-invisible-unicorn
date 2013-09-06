import json
import sqlite3

from flask import Flask, g, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), unique=True)

    def __init__(self, name):
        this.name = name

class Route(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(256), unique=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))



class Backend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(256))
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))

@app.route('/v1/<project>/mapping', methods=['GET'])
def all_mappings(project):
    return project
    pass

@app.route('/v1/<project>/mapping', methods=['PUT'])
def create_mapping(project):
    return project
    pass

@app.route('/v1/<project>/mapping/<host>', methods=['DELETE'])
def delete_mapping(project, host):
    return project + host
    pass

@app.route('/v1/<project>/mapping/<host>', methods=['GET'])
def get_mapping(project, host):
    return project + host
    pass

@app.route('/v1/<project>/mapping/<host>', methods=['POST'])
def update_mapping(project, host):
    return project + host
    pass

if __name__ == '__main__':
    app.run(debug=True)
