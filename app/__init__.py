from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flasgger import Swagger

db = SQLAlchemy()
api = Api()
swagger = Swagger()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    
    # Initialize Swagger
    swagger.init_app(app)

    # Import routes here to avoid circular imports
    from app import routes
    
    # Initialize routes
    routes.initialize_routes(api)
    
    # Initialize the API with the Flask app
    api.init_app(app)

    with app.app_context():
        db.create_all()

    return app