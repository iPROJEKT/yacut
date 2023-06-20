from flask import Flask, render_template  
from flask_sqlalchemy import SQLAlchemy

from yacut import app

@app.route('/')
def index_view():
    return render_template('opinion.html')
