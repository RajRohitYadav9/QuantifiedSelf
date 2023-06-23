import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from matplotlib import pyplot as plt
from flask_restful import Resource, Api, fields, marshal_with, reqparse



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.abspath(os.getcwd()) + '/clientdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 


db = SQLAlchemy(app)


api=Api(app)

    

from controller import *
from api import *




if __name__ == '__main__':
  app.debug=True
  app.run(host="0.0.0.0", port=5000) 