from flask import Flask
from config import BaseConfig
from os import path as p, mkdir as md

app = Flask(__name__)
app.config.from_object(BaseConfig)

from .database import db

# Verify if directory is created otherwise create it
path = p.join(app.config["BASE_FOLDER"],"uploaded_files")
if not p.exists(path): md(path)
path = p.join(path, "product")
if not p.exists(path): md(path)
path = p.join(path,"default")
if not p.exists(path): md(path)

from . import login_manager
from . import routes