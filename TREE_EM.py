import os
import sys
import click

from app import create_app, db
# from app.models import User, Permission, Role, Images

# Flask Coverage

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

#@app.shell_context_processor
# def make_shell_context():
#     return dict(db=db, User=User, Permission=Permission, Role=Role)

