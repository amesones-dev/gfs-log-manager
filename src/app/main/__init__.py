from flask import Blueprint


bp_name = 'main'
module = __name__
template_folder = 'templates'

# In Flask
# template_folder='templates'
# maps to OS path
# app/templates

bp = Blueprint(name=bp_name, import_name=module, template_folder=template_folder)

from app.main import routes