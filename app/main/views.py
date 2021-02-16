from flask import render_template, redirect, url_for, abort, flash, \
    request, current_app, make_response
from flask_sqlalchemy import get_debug_queries
from . import main
# from .forms import 
from .. import db
from ..models import Permission, Role, User, Images

@main.route('/', methods['GET', 'POST'])
def index():
    return render_template('index.html') 
