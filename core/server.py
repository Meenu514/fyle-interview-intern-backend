from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis import assignments, principals
from core.libs import helpers
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException
from flask import Flask
from core.apis.principals import principal_teacher_resources
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure your app (e.g., database settings)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'your-database-url'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)  # This line is critical

    '''# Register blueprints
    from core.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)'''

    return app
app.register_blueprint(assignments.student_assignments_resources, url_prefix='/student')
app.register_blueprint(assignments.teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(assignments.principal_assignments_resources, url_prefix='/principal')
app.register_blueprint(principals.principal_teacher_resources, url_prefix='/principal')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code

    raise err
