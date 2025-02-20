"""Initialization of app object"""

import os

from flask import Flask, abort, request
from flask_cors import CORS

from app.article.routes import article_ns
from app.batch_status.routes import batch_status_ns
from app.brand.routes import brand_ns
from app.enrichment_simweb.routes import enrichment_sim_web_ns
from app.extensions import api, db, migrate
from app.main import main as main_blueprint
from app.publisher.routes import publisher_ns
from app.sentiment.routes import sentiment_ns
from config import DevelopmentConfig, ProductionConfig


def create_app():
    """
    Main function responsible for initializing app object
    returns: Flask App Object
    """

    app = Flask(__name__, static_url_path="/static", static_folder="static")
    CORS(app, origins="*")

    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    if os.getenv("FLASK_ENV") == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # print("DB : ", app.config['SQLALCHEMY_DATABASE_URI'])
    # Register Blueprints only for the core endpoint
    app.register_blueprint(main_blueprint)

    # # Register Namespaces
    api.init_app(app)
    api.add_namespace(publisher_ns, path="/publisher")
    api.add_namespace(brand_ns, path="/brand")
    api.add_namespace(enrichment_sim_web_ns, path="/enrichmentsimweb")
    api.add_namespace(article_ns, path="/article")
    api.add_namespace(sentiment_ns, path="/sentiment")
    api.add_namespace(batch_status_ns, path="/batchstatus")

    db.init_app(app)

    @app.cli.command("init-db")
    def init_db():
        """Create database tables from SQLAlchemy models."""
        db.create_all()
        print("Initialized the database.")

    migrate.init_app(app, db)

    allowed_ips = {
        "44.220.242.243",  # company-vpc-public-subnet-nat-ip
        "127.0.0.1",  # internal localhost access
        "99.231.69.240",
    }

    @app.before_request
    def limit_remote_addr():
        client_ip = request.remote_addr
        if client_ip not in allowed_ips:
            abort(403)  # Forbidden

    return app
